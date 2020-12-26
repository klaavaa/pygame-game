from pathfinding_algs.node import SimpleNode


def get_neighbors(x, y, cost, corners):
    if corners:
        return SimpleNode(x - 1, y, cost + 1), SimpleNode(x + 1, y, cost + 1), SimpleNode(x, y - 1, cost + 1), SimpleNode(x, y + 1, cost + 1), SimpleNode(x - 1, y - 1, cost + 1),\
               SimpleNode(x + 1, y - 1, cost + 1), SimpleNode(x - 1, y + 1, cost + 1), SimpleNode(x + 1, y + 1, cost + 1)

    if not corners:
        return SimpleNode(x - 1, y, cost + 1), SimpleNode(x + 1, y, cost + 1), SimpleNode(x, y - 1, cost + 1), SimpleNode(x, y + 1,cost + 1)




def bfs(range, x, y, move_corners, object_list):
    start_node = SimpleNode(x, y, 0)
    path = [start_node]
    queue = [start_node]
    visited = [start_node]
    while len(queue) > 0:
        v = queue[0]
        queue.pop(0)
        for i in get_neighbors(v.x, v.y, v.cost, move_corners):
            skip_node = False
            for index, node in enumerate(visited):

                if node.x == i.x and node.y == i.y:
                    skip_node = True

            if i.cost > range:
                skip_node = True

            if object_list[i.y][i.x] == 1:
                skip_node = True
            for obj in object_list:
                if obj[0] == i.x and obj[1] == i.y:
                    skip_node = True

            if not skip_node:
                visited.append(i)
                queue.append(i)
                path.append(i)

    return path



