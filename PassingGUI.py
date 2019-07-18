import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from tkinter import simpledialog
import WebWebUtilities
import json

class AnalysisApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)  # Initialize
        self.geometry('900x350+300+300')

        # Initialize data folder

        self.defaultFolder = []
        self.infoList = []
        self.data = dict()

        #  MENUBAR
        self.filterArray = ['By Competition', 'By Team', 'By Player', 'By Match', 'By Match File']
        self.filterOptions = tk.StringVar()
        self.filterOptions.set(self.filterArray[0])  # default value
        self.filterMenu = tk.OptionMenu(self, self.filterOptions, *self.filterArray, command=self.ClearAll)
        self.filterLabel = tk.Label(self, text="Filter Options")

        self.buttonVisualize = tk.Button(self, text="Visualize with WebWeb", command=self.OnVisualize, width='20')
        self.buttonQuit = tk.Button(self, text="Quit", command=self.OnQuit, width='20')
        self.buttonGetItems = tk.Button(self, text="Load Items", command=self.GetItems, width='15')
        self.buttonFolder = tk.Button(self, text="Change Data Folder", command=self.GetFolder, width='15')
        self.buttonClearItems = tk.Button(self, text="Clear Items", command=self.ClearItems, width='15')
        self.buttonSelect = tk.Button(self, text="Select Highlighted", command=self.SelectItems, width='15')

        self.availableItemsLabel = tk.Label(self, text="Items Available")
        self.availableItemsList = tk.Listbox(self, selectmode=tk.MULTIPLE, height=10, width=40)
        self.availableItemsScrollbar = tk.Scrollbar(self, command=self.availableItemsList.yview)
        self.availableItemsList['yscrollcommand'] = self.availableItemsScrollbar.set

        self.visualizeItemsLabel = tk.Label(self, text="Items to Visualize")
        self.visualizeItemsList = tk.Listbox(self, height=10, width=40)
        self.visualizeItemsScrollbar = tk.Scrollbar(self, command=self.visualizeItemsList.yview)
        self.visualizeItemsList['yscrollcommand'] = self.visualizeItemsScrollbar.set

        # Column 0
        self.filterLabel.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.filterMenu.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        self.buttonVisualize.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        self.buttonQuit.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

        # Column 1
        self.availableItemsLabel.grid(row=0, column=1, padx=10, pady=10)
        self.availableItemsList.grid(row=1, column=1, columnspan=1, rowspan=2, sticky='nsew', pady=10)
        self.buttonGetItems.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

        # Column 2
        self.availableItemsScrollbar.grid(row=1, column=2, rowspan=2, sticky='nsew')

        # Column 3
        self.buttonFolder.grid(row=3, column=3, columnspan=1, padx=10, pady=10)
        self.buttonSelect.grid(row=1, column=3, padx=10, pady=10)

        # Column 4
        self.visualizeItemsLabel.grid(row=0, column=4, padx=10, pady=10)
        self.visualizeItemsList.grid(row=1, column=4, columnspan=1, rowspan=2, sticky='nsew')
        self.buttonClearItems.grid(row=3, column=4, columnspan=1, padx=10, pady=10)

        # Column 5
        self.visualizeItemsScrollbar.grid(row=1, column=5, rowspan=2, sticky='nsew')


    def OnVisualize(self):
        if len(self.infoList) == 0:
            messagebox.showinfo("Window", "Please Select an Item!")
        else:
            title = simpledialog.askstring("Input", "What is the visualization title?")
            WebWebUtilities.visualizePassingNetworks(title, self.infoList)


    def GetItems(self):
        filterChoice = self.filterOptions.get()
        if self.defaultFolder == []:
            self.GetFolder()

        if filterChoice == "By Competition":
            self.LoadCompetitions()

        elif filterChoice == "By Team":
            self.LoadTeams()

        elif filterChoice == "By Player":
            messagebox.showinfo("Window", "Not Implemented Yet!")

        elif filterChoice == "By Match":
            self.LoadMatches()

        elif filterChoice == "By Match File":
            messagebox.showinfo("Window", "Not Implemented Yet!")
            # options = {}
            # options['initialdir'] = self.defaultFolder
            # filenames = filedialog.askopenfilenames(**options)
            #
            # duplicate = 0
            # #check for duplicate filenames
            # for i in range(len(self.infoList)):
            #     for j in range(len(filenames)):
            #         if self.infoList[i] == filenames[j]:
            #             duplicate = 1
            #             break
            # if duplicate:
            #     print('Duplicate files!!')
            # elif filenames == "":
            #     print('You did not select a file!!')
            # else:
            #     for i in range(len(filenames)):
            #         self.availableItemsList.insert('end', filenames[i])
            #         self.infoList.append({filenames[i]:"test"})


    def GetFolder(self):
        # Need to check for folders and files
        dirname = filedialog.askdirectory(title='Please select a directory')
        dirList = os.listdir(dirname)
        if 'events' in dirList and 'matches' in dirList and 'lineups' in dirList and 'competitions.json' in dirList:
            self.defaultFolder = dirname
        else:
            messagebox.showinfo("Window", "Please Select a folder containing events, lineups, and matches subfolders and competition.json!")

    def SelectItems(self):
        matchFileList = list()
        filterChoice = self.filterOptions.get()
        if filterChoice == "By Competition":
            indices = self.availableItemsList.curselection()
            for index in indices:
                value = self.availableItemsList.get(index)
                if value not in self.visualizeItemsList.get(0, tk.END):
                    self.visualizeItemsList.insert(tk.END, value)

                    matchFileList.append(self.defaultFolder + "/matches/" +
                    str(self.data[self.availableItemsList.get(index)][0]) + "/"
                    + str(self.data[self.availableItemsList.get(index)][1]) + ".json")
            for matchFile in matchFileList:
                self.infoList.extend(self.GetCompetitionMatchFileList(matchFile))

        elif filterChoice == "By Team":
            indices = self.availableItemsList.curselection()
            for index in indices:
                value = self.availableItemsList.get(index)
                if value not in self.visualizeItemsList.get(0, tk.END):
                    self.visualizeItemsList.insert(tk.END, value)
                    # iterate through folders and files
                    dirList = os.listdir(self.defaultFolder + "/matches/")
                    for folder in dirList:
                        fileList = os.listdir(self.defaultFolder + "/matches/" + folder)

                        for file in fileList:
                            filename = self.defaultFolder + "/matches/" + folder + "/" + file
                            with open(filename) as json_file:
                                data = json.load(json_file)
                            for item in data:
                                if item["home_team"]["home_team_name"] == value or item["away_team"]["away_team_name"] == value:
                                    listItem = item["home_team"]["home_team_name"] + " vs. " + item["away_team"]["away_team_name"] + " " + item["match_date"]
                                    self.infoList.append([self.defaultFolder + "/events/" + str(item["match_id"]) + ".json", listItem])

        elif filterChoice == "By Match":
            indices = self.availableItemsList.curselection()
            for index in indices:
                value = self.availableItemsList.get(index)
                if value not in self.visualizeItemsList.get(0, tk.END):
                    self.visualizeItemsList.insert(tk.END, value)
                    self.infoList.append([self.defaultFolder + "/events/" + str(self.data[self.availableItemsList.get(index)]) + ".json", value])

        elif filterChoice == "By File":
            print('4')

    def ClearItems(self):
        self.infoList = []
        self.visualizeItemsList.delete(0, tk.END)


    def ClearAll(self, event):
        self.infoList = []
        self.visualizeItemsList.delete(0, tk.END)
        self.availableItemsList.delete(0, tk.END)
        self.data.clear()

    def LoadCompetitions(self):
        filename = self.defaultFolder + "/competitions.json"
        with open(filename) as json_file:
            data = json.load(json_file)
        for item in data:
            listItem = item["competition_name"] + " " + item["season_name"]
            if listItem not in self.availableItemsList.get(0, tk.END):
                self.availableItemsList.insert(tk.END, listItem)
                self.data.update({listItem:[item["competition_id"],item["season_id"]]})

    def LoadTeams(self):
        dirList = os.listdir(self.defaultFolder + "/matches/")
        for folder in dirList:
            fileList = os.listdir(self.defaultFolder + "/matches/" + folder)

            for file in fileList:
                filename = self.defaultFolder + "/matches/" + folder + "/" + file
                with open(filename) as json_file:
                    data = json.load(json_file)

                for item in data:
                    homeTeam = item["home_team"]["home_team_name"]
                    awayTeam = item["away_team"]["away_team_name"]
                    if homeTeam not in self.availableItemsList.get(0, tk.END):
                        self.availableItemsList.insert(tk.END, homeTeam)
                        self.data.update({homeTeam:item["home_team"]["home_team_id"]})
                    if awayTeam not in self.availableItemsList.get(0, tk.END):
                        self.availableItemsList.insert(tk.END, awayTeam)
                        self.data.update({awayTeam:item["away_team"]["away_team_id"]})

    def LoadMatches(self):
        dirList = os.listdir(self.defaultFolder + "/matches/")
        for folder in dirList:
            fileList = os.listdir(self.defaultFolder + "/matches/" + folder)

            for file in fileList:
                filename = self.defaultFolder + "/matches/" + folder + "/" + file
                with open(filename) as json_file:
                    data = json.load(json_file)

                for item in data:
                    listItem = item["home_team"]["home_team_name"] + " vs. " + item["away_team"]["away_team_name"] + " " + item["match_date"]
                    if listItem not in self.availableItemsList.get(0, tk.END):
                        self.availableItemsList.insert(tk.END, listItem)
                        self.data.update({listItem:item["match_id"]})

    def GetCompetitionMatchFileList(self, competitionMatchesFile):
        matchFileList = list()
        filename = competitionMatchesFile
        with open(filename) as json_file:
            data = json.load(json_file)
        for item in data:
            info = item["home_team"]["home_team_name"] + " vs. " + item["away_team"]["away_team_name"] + " " + item["match_date"]
            matchFileList.append([self.defaultFolder + "/events/" + str(item["match_id"]) + ".json", info])
        return matchFileList

    def OnQuit(self):
        self.destroy()
