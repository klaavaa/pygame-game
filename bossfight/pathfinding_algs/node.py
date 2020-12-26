class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fcost = 0
        self.gcost = 0
        self.hcost = 0
        self.child = None
        self.parent = None


class SimpleNode:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost