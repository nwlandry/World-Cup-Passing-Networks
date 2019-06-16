from webweb import Web
import webweb
import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import PassingUtilities

filename = "19714.json"

passing = PassingUtilities.createPassingList(filename)

A, libPlayers = PassingUtilities.createAdjacencyAndDict(passing)


displayInfo = dict()
nodeInfo = arr = [0 for i in range(len(libPlayers))]
for name, number in libPlayers.items():
    nodeInfo[number] = name
displayInfo.update({'name':{'values':nodeInfo}})

# instantiate webweb and show the result

# plt.figure()
# plt.spy(A)
# plt.show()

# plt.figure()
# plt.hist(np.sum(A, axis=0))
# plt.show()

displayInfo = dict()
nodeInfo = dict()
for name, number in libPlayers.items():
    nodeInfo[number]={'name':name}
displayInfo.update({"nodes":nodeInfo})


web = Web(title='World Cup Soccer Data', adjacency=A, display=displayInfo)
web.display.charge = 500
web.display.linkLength = 200
web.display.linkStrength = 0.5
web.display.gravity = .1
web.display.colorBy = 'strength'
web.display.scaleLinkWidth = True
web.display.sizeBy = 'strength'
web.display.showNodeNames = True
web.display.showLegend = True
#web.display.hideMenu = True
#web.display.attachWebwebToElementWithId = 'test-vis'
web.show()
