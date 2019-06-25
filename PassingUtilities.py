import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import traceback

def createPassingListAndLib(filename):
    with open(filename) as json_file:
        try:
            data = json.load(json_file)
        except:
            with open(filename, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                except Exception as e:
                    print(e)
                    print(filename)
                    return list()

    passing = list()
    libPlayers = dict()
    numNodes = 0
    currentPlayer = ""

    # Initialize player dictionary
    for event in data:
        if event["type"]["name"] == "Starting XI":
            for player in event["tactics"]["lineup"]:
                if player["player"]["name"] not in libPlayers:
                    libPlayers.update({player["player"]["name"]:{'value':numNodes, 'location':list(), 'team':event["team"]["name"]}})
                    numNodes = numNodes + 1
        elif event["type"]["name"] == "Substitution":
            name = event["substitution"]["replacement"]["name"]
            if name not in libPlayers:
                libPlayers.update({name:{'value':numNodes, 'location':list(), 'team':event["team"]["name"]}})
                numNodes = numNodes + 1

    # Generate passing data
    for event in data:
        if event["type"]["name"]=="Pass":
            if currentPlayer != event["player"]["name"]:
                currentPlayer = event["player"]["name"]
            libPlayers[currentPlayer]["location"].append(event["location"])

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

            libPlayers[currentPlayer]["location"].append(event["location"])

    return passing, libPlayers

def createAdjacencyMatrix(passing, libPlayers):
    n = len(libPlayers)
    A = np.zeros([n, n])
    # use the passing list and the dictionary to create the weighted adjacency matrix
    for entry in passing:
        A[libPlayers[entry["from"]]["value"], libPlayers[entry["to"]]["value"]] = entry["passes"]
    return A
