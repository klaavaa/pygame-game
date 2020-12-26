from math import sqrt
from pathfinding_algs.node import Node

def astar(start, end, objects):
    startnode = Node(start[0], start[1])
    endnode = Node(end[0], end[1])

    if objects[endnode.y][endnode.x] == 1:
        return None


    openlist = []
    closedlist = []
    path = []
    openlist.append(startnode)
    while len(openlist) > 0:
        current = 0
        fcost = 99999
        for node in openlist:
            if node.fcost < fcost:
                fcost = node.fcost
                current = node

        openlist.remove(current)
        closedlist.append(current)
        if current.x == endnode.x and current.y == endnode.y:
            parent = current.parent
            path.append(current)
            while parent is not None:
                path.append(parent)
                parent = parent.parent
            return path
        current.child = [Node(current.x - 1, current.y), Node(current.x + 1, current.y), Node(current.x, current.y + 1), Node(current.x, current.y - 1)]
                  #     Node(current.x - 1, current.y - 1), Node(current.x - 1, current.y + 1), Node(current.x + 1, current.y + 1), Node(current.x + 1, current.y - 1)]

        for i in current.child:
            skip = False
            if objects[i.y][i.x] == 1:
                continue
            for l in closedlist:
                if i.x == l.x and i.y == l.y:
                    skip = True

            if not skip:
                for l in openlist:
                    if i.x == l.x and i.y == l.y:
                        if l.fcost < i.fcost:
                            skip = True

            if not skip:
                if i not in openlist:
                    i.parent = current
                    i.gcost = current.gcost + sqrt((abs(current.x - i.x) + abs(current.y - i.y))* 10)
                    i.hcost = max(abs(i.x - endnode.x), abs(i.y - endnode.y)) * 10
                    i.fcost = i.gcost + i.hcost
                    openlist.append(i)
    return None