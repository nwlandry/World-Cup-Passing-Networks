from webweb import Web
import webweb
import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import PassingUtilities
import random

def visualizePassingNetworks(visTitle, visInfoList):
    # Visualization Parameters
    width = 800
    height = 480
    padding = 50

    #field dimensions in yards
    fieldLength = 120
    fieldWidth = 75
    # instantiate webweb
    web = Web(title=visTitle)

    for item in visInfoList:
        passing, libPlayers = PassingUtilities.createPassingListAndLib(item[0])
        if len(passing) != 0:
            A = PassingUtilities.createAdjacencyMatrix(passing, libPlayers)
            displayInfo = createMetaData(libPlayers, width, height, padding, fieldLength, fieldWidth)

            web.networks.__dict__[item[1]] = webweb.webweb.Network(adjacency=A, metadata=displayInfo)

    web.display.charge = 500
    web.display.linkLength = 200
    web.display.linkStrength = 0.5
    web.display.gravity = .1
    web.display.radius = 10
    web.display.scaleLinkOpacity = True
    web.display.colorBy = 'team'
    web.display.scaleLinkWidth = True
    web.display.sizeBy = 'strength'
    web.display.showNodeNames = True
    web.display.showLegend = True
    web.display.colorPalette = 'Dark2'
    web.display.freezeNodeMovement = True
    web.display.width = width
    web.display.height = height
    web.display.attachWebwebToElementWithId = 'soccer-vis'
    web.show()

def createMetaData(libPlayers, width, height, pad, fieldLength, fieldWidth):
    displayInfo = dict()

    # Scaling the location data so that it fits in the visualization window
    xScale = (width - 2*pad)/fieldLength
    yScale = (height - 2*pad)/fieldWidth

    # initialize lists for the metadata dict
    nodeName = [0 for i in range(len(libPlayers))]
    nodeX = [0 for i in range(len(libPlayers))]
    nodeY = [0 for i in range(len(libPlayers))]
    teamName = [0 for i in range(len(libPlayers))]

    defaultTeamName = ""
    for name, data in libPlayers.items():
        if defaultTeamName == "":
            defaultTeamName = data["team"]
        nodeName[data["value"]] = name

        location = [sum(col) / float(len(col)) for col in zip(*data["location"])]
        # if no one passes to the player, the location with be empty, so assign a random position to it
        if location == []:
            location = [fieldLength*random.random(), fieldWidth*random.random()]

        # use this to position different teams at different ends of the field.
        if data["team"] == defaultTeamName:
            nodeX[data["value"]] = pad + xScale*location[0]
            nodeY[data["value"]] = yScale*(location[1]-fieldWidth/2) + height/2
        else:
            nodeX[data["value"]] = width - pad - xScale*location[0]
            nodeY[data["value"]] = -yScale*(location[1]-fieldWidth/2) + height/2


        teamName[data["value"]] = data["team"]

        displayInfo.update({'name':{'values':nodeName},'x':{'values':nodeX},'y':{'values':nodeY},'team':{'values':teamName}})
    return displayInfo
