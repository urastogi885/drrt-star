from math import sqrt


class Node:
    # Initialize
    def __init__(self, env, parent=None):
        self.env = env
        self.parent = parent
        self.distance = 0
        if parent != None:
            self.costToCome = parent.costToCome + 1
        else:
            self.costToCome = 0

    def updateDistance(self, i):
        self.distance = sqrt((self.env[0][0] - i[0][0]) ** 2 + (self.env[0][1] - i[0][1]) ** 2 + (self.env[1][0] - i[1][0]) ** 2 + (
                    self.env[1][1] - i[1][1]) ** 2)

    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return reversed(p)
