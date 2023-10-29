import numpy as np
from interior import *
import copy

def addBinaryValue(binList, bVal, rVal, min, max):
    if max == min:
        binList.insert(min, (bVal, rVal))
        return True # Success
    elif max < min:
        return False # Failure
    checkLocation = (max-min)//2 + min
    checkVal = binList[checkLocation][0]
    if bVal > checkVal:
        return addBinaryValue(binList, bVal, rVal, checkLocation + 1, max)
    elif bVal < checkVal:
        return addBinaryValue(binList, bVal, rVal, min, checkLocation)
    else:
        return addBinaryValue(binList, bVal, rVal, checkLocation, checkLocation)


def pathFindingAlgorithm(nodeSpace, startNode, endNode):
    nodeList = nodeSpace.get_nodes()
    unvisitedNodes = [(0,startNode)]
    unvisitedDistDict = {startNode: 0}
    parentList = {}
    visitedList = []

    finalDist = 0

    loopBool = True
    while loopBool:
        if len(unvisitedNodes) == 0:
            print("Ran out of nodes")
            break
        curNodeInfo = unvisitedNodes[0]
        visitedList.append(unvisitedNodes.pop(0)[1])
        curNodeDist = curNodeInfo[0]
        curNodeName = curNodeInfo[1]
        if curNodeName == endNode:
            print("Done! Distance is", curNodeDist)
            finalDist = curNodeDist
            break
        curNodeConnections = nodeList[curNodeInfo[1]].get_connections()
        for connectionName, connectionData in curNodeConnections.items():
            if connectionName in visitedList:
                continue
            newConDist = connectionData['distance'] + curNodeDist
            if connectionName in unvisitedDistDict:
                oldDistance = unvisitedDistDict[connectionName]
                if oldDistance > newConDist:
                    parentList[connectionName] = curNodeName
                    unvisitedDistDict[connectionName] = newConDist
                    unvisitedNodes.remove((oldDistance, connectionName))
                    addBinaryValue(unvisitedNodes, newConDist, connectionName, 0, len(unvisitedNodes))
            else:
                parentList[connectionName] = curNodeName
                unvisitedDistDict[connectionName] = newConDist
                addBinaryValue(unvisitedNodes, newConDist, connectionName, 0, len(unvisitedNodes))
    finalNodeList = [endNode]
    nextNode = endNode
    while True:
        nextNode = parentList[nextNode]
        finalNodeList.insert(0, nextNode)
        if nextNode == startNode:
            break
    return (finalNodeList, finalDist)
        

def quickCon(space, a, b):
    space.add_connection(a,b)


testSpace2 = Space()
for k in range(2):
    for i in range(100):
        for j in range(100):
            if i == 33 and j == 66:
                testSpace2.add_node(str(i) + "," + str(j)+','+str(k), {'x':i,'y':j,'z':k,'type':NodeType.ELEVATOR,'mult':1.5})
            else:
                if i*j % 7 == 5:
                    testSpace2.add_node(str(i) + "," + str(j)+','+str(k), {'x':i,'y':j,'z':k, 'type':NodeType.OTHER}) #(70-np.sqrt((i-50)**2+(j-50)**2))/50
                else:
                    testSpace2.add_node(str(i) + "," + str(j)+','+str(k), {'x':i,'y':j,'z':k, 'type':NodeType.HALLWAY}) #(70-np.sqrt((i-50)**2+(j-50)**2))/50


    for i in range(100):
        for j in range(100):
            if i > 0:
                quickCon(testSpace2,str(i-1)+','+str(j)+','+str(k),str(i)+','+str(j)+','+str(k))
            if j > 0:
                quickCon(testSpace2,str(i)+','+str(j-1)+','+str(k),str(i)+','+str(j)+','+str(k))

if __name__ == 'main':
    quickCon(testSpace2, '33,66,0','33,66,1')
    quickCon(testSpace2, '98,3,0','98,3,1')

    #path = pathFindingAlgorithm(testSpace2, "0,0,0", "99,99,1")
    #testSpace2.plot_space_highlight(path[0])

    testSpace3 = blacklistedSpaceCopy(testSpace2, [NodeType.OTHER])
    path2 = pathFindingAlgorithm(testSpace3, "0,0,0", "99,99,1")
    testSpace3.plot_space_highlight(path2[0])