from webweb import Web
import webweb
import json
import numpy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import PassingUtilities
import WebWebUtilities

filenames = ["19714.json","22921.json","22924.json","22943.json"]

# instantiate webweb
web = Web(title="World Cup Soccer Data")

for name in filenames:
    passing = PassingUtilities.createPassingList(name)
    A, libPlayers = PassingUtilities.createAdjacencyAndDict(passing)
    displayInfo = WebWebUtilities.createMetaDataNames(libPlayers)

    web.networks.__dict__[name] = webweb.webweb.Network(adjacency=A, metadata=displayInfo)

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




# plt.figure()
# plt.spy(A)
# plt.show()

# plt.figure()
# plt.hist(np.sum(A, axis=0))
# plt.show()

# displayInfo = dict()
# nodeInfo = dict()
# for name, number in libPlayers.items():
#     nodeInfo[number]={'name':name}
# displayInfo.update({"nodes":nodeInfo})
