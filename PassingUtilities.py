import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def createPassingList(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    passing = list()
    currentPlayer = ""
    for event in data:
        if event["type"]["name"]=="Pass":
            if currentPlayer != event["player"]["name"]:
                currentPlayer = event["player"]["name"]
        elif event["type"]["name"]=="Ball Receipt*":
            newPlayer = event["player"]["name"]
            if len(passing)==0 or not any(d.get('from', None) == currentPlayer and d.get('to', None) == newPlayer for d in passing):
                passing.append({"from":currentPlayer,"to":newPlayer,"passes":1})
                currentPlayer = newPlayer
            else:
                for entry in passing:
                    if entry["from"] == currentPlayer and entry["to"] == newPlayer:
                        entry["passes"] = entry["passes"] + 1
                        currentPlayer = newPlayer
    return passing

def createAdjacencyAndDict(passing):
    libPlayers = dict()
    numNodes = 0
    for entry in passing:
        if entry["from"] not in libPlayers:
            libPlayers.update({entry["from"]:numNodes})
            numNodes = numNodes + 1
        if entry["to"] not in libPlayers:
            libPlayers.update({entry["to"]:numNodes})
            numNodes = numNodes + 1

    A = np.zeros([numNodes, numNodes])
    for entry in passing:
        A[libPlayers[entry["from"]], libPlayers[entry["to"]]] = entry["passes"]
    return A, libPlayers

    
