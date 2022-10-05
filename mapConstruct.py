# import os, sys
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:   
#     sys.exit("please declare environment variable 'SUMO_HOME'")
import sumolib
net=sumolib.net.readNet('map3.net.xml')
print(net.getNode('NodeID').getCoord())
nextNodeID = net.getEdge('EdgeID').getToNode().getID()
