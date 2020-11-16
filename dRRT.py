from PRM import generateRoadMap
from math import sqrt
import numpy as np

fixed_nodes = [[60, 38], [51, 47], [50, 33], [51, 71], [69, 72], [36, 38], [19, 61], [5, 93], [5, 93], [26, 95],
               [82, 96], [55, 97], [49, 16], [83, 37], [4, 5], [6, 22], [10, 37], [26, 34], [24, 10], [47, 5], [27, 3],
               [46, 30], [68, 3], [70, 20], [70, 32], [92, 6], [93, 27], [7, 61], [5, 79], [24, 73], [47, 64], [36, 60],
               [71, 59], [89, 59], [91, 78], [70, 87], [47, 89]]

vertices, edges = generateRoadMap(0, 20, fixed_nodes)

GHat = []
for i in vertices:
    for j in vertices:
        GHat.append([i, j])

E_Hat = []
for i in range(len(GHat)):
    for j in range(len(GHat)):

        if GHat[i] == GHat[j]:
            pass
        elif GHat[i][0] != GHat[j][0]:
            index1 = vertices.index(GHat[i][0])
            index2 = vertices.index(GHat[j][0])
            if [index1, index2] in edges or [index2, index1] in edges:
                E_Hat.append([i, j])
        elif GHat[i][1] != GHat[j][1]:
            index1 = vertices.index(GHat[i][1])
            index2 = vertices.index(GHat[j][1])
            if [index1, index2] in edges or [index2, index1] in edges:
                E_Hat.append([i, j])
        else:
            index1 = vertices.index(GHat[i][0])
            index2 = vertices.index(GHat[j][0])
            index3 = vertices.index(GHat[i][1])
            index4 = vertices.index(GHat[j][1])
            if ([index1, index2] in edges or [index2, index1] in edges) and (
                    [index3, index4] in edges or [index4, index3] in edges):
                E_Hat.append([i, j])

start1 = [24, 10]
start2 = [70, 87]
end1 = [70, 20]
end2 = [24, 73]

start = [start1,start2]
end = [end1, end2]


def getNearestNode(node, graph):
    nearesNode = [[], 99999]
    for i in graph:
        distance = sqrt((node[0][0]-i[0][0])**2+(node[0][1]-i[0][1])**2+(node[1][0]-i[1][0])**2+(node[1][1]-i[1][1])**2)
        if distance < nearesNode[1]:
            nearesNode[0] = i
            nearesNode[1] = distance
    return nearesNode[0]

def getNeighbour(node, nearestNode):
    global GHat
    neighboursIndexList = []
    index = GHat.index(node)
    for i in E_Hat:
        if index in i:
            for point in i:
                if point != index:
                    neighboursIndexList.append(point)

    neighboursList = []
    for index in neighboursIndexList:
        neighboursList.append(GHat[index])
    newNode = getNearestNode(nearestNode, neighboursList)
    return newNode



Tree = [start]
for i in range(10000):
    print(i)
    point = GHat[np.random.randint(0, len(GHat))]
    nearestNode = getNearestNode(point, Tree)
    newNode = getNeighbour(nearestNode, point)
    if newNode not in Tree:
        Tree.append(newNode)

print(getNearestNode(end, Tree))