from webweb import Web
import webweb
import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import PassingUtilities

def visualizePassingNetworks(visTitle, visInfoList):
    # instantiate webweb
    web = Web(title=visTitle)

    for item in visInfoList:

        passing = PassingUtilities.createPassingList(item[0])
        A, libPlayers = PassingUtilities.createAdjacencyAndDict(passing)
        displayInfo = createMetaDataNames(libPlayers)

        web.networks.__dict__[item[1]] = webweb.webweb.Network(adjacency=A, metadata=displayInfo)

    # web = Web(title='World Cup Soccer Data', adjacency=A, display=displayInfo)
    web.display.charge = 500
    web.display.linkLength = 200
    web.display.linkStrength = 0.5
    web.display.gravity = .1
    web.display.colorBy = 'strength'
    web.display.scaleLinkWidth = True
    web.display.sizeBy = 'strength'
    web.display.showNodeNames = False
    web.display.showLegend = True
    #web.display.hideMenu = True
    #web.display.attachWebwebToElementWithId = 'test-vis'
    web.show()

def createMetaDataNames(libPlayers):
    displayInfo = dict()
    nodeInfo = arr = [0 for i in range(len(libPlayers))]
    for name, number in libPlayers.items():
        nodeInfo[number] = name
    displayInfo.update({'name':{'values':nodeInfo}})
    return displayInfo
