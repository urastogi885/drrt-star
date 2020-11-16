import numpy as np
from mapUtils import readMap
from math import sqrt, atan2, sin, cos

map = readMap('map.txt')

np.random.seed(100)


def getDistance(pointOne, pointTwo):
    return sqrt((pointOne[0] - pointTwo[0]) ** 2 + (pointOne[1] - pointTwo[1]) ** 2)


def checkEdge(pointOne, pointTwo):
    angle = atan2(pointTwo[1] - pointOne[1], pointTwo[0] - pointOne[0])
    distance = int(getDistance(pointOne, pointTwo))
    x, y = pointOne[0], pointOne[1]
    for _ in range(distance):
        x += cos(angle)
        y += sin(angle)
        if map[int(y)][int(x)] == 1:
            return False
    return True


def generateRoadMap(pointsCount, conectionLength, fixedPoints=[]):
    vertices = []
    edges = []
    while len(vertices) != pointsCount:
        x, y = np.random.randint(0, len(map[0])), np.random.randint(0, len(map))
        if map[y][x] == 0:
            vertices.append([x, y])
    for point in fixedPoints:
        if map[point[0]][point[1]] == 0:
            vertices.append([x, y])

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if getDistance(vertices[i], vertices[j]) < conectionLength:
                if checkEdge(vertices[i], vertices[j]):
                    edges.append([i, j])

    return vertices, edges
