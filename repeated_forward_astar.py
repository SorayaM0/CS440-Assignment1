
# TODO (Part 2):
# Implement Repeated Forward A*

import heapq, math

class Node:
    def __init__(self, position, g, h, parent=None, tie_breaker="large_g"):
        self.position = position
        self.g = math.inf
        self.h = 0
        self.parent = parent # parent (previous) node
        self.search = 0
        self.tie_breaker = tie_breaker

    def f(self):
        return self.g + self.h # f = g + h
        
def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def get_neighbors(gridworld, row, col):
    neighbors = []
    # simulate down, up, right, and left with coordinates
    for dir_row, dir_col in [(1,0), (-1,0), (0,1), (0,-1)]:
        new_row, new_col = row + dir_row, col + dir_col
        if 0 <= new_row < gridworld.rows and 0 <= new_col < gridworld.cols:
            if gridworld.grid[new_row][new_col] != '#':
                neighbors.append((new_row, new_col))
    return neighbors

# Implement Compute Path from pseudocode in Assignment 1
def compute_path(start, goal, grid, nodes, counter, tie_breaker, expanded):
    open_list = []

    def push(n):
        # small g
        if tie_breaker == "small_g":
            priority = (n.f(), n.g)
        # large g
        else: priority = (n.f(), -n.g)
        heapq.heappush(open_list, (priority, n))
    push(start)

    while open_list and goal.g > open_list[0][1].f():
        _, s = heapq.heappop(open_list)
        expanded += 1

        for succ in get_neighbors(s, grid, nodes): 
            if succ.search < counter:
                succ.g = math.inf
                succ.search = counter

            if succ.g > s.g + 1:
                succ.g = s.g + 1
                succ.parent = s
            
            open_list = [(p, n) for (p, n) in open_list if n != succ]
            heapq.heapify(open_list)

            push(succ)

    return expanded


# Repeated forward A* implementation
def repeated_forward_astar(gridworld, start, goal, tie_breaker = "small_g"):
    grid = gridworld.grid
    rows, cols = gridworld.rows, gridworld.cols

    nodes = [[Node(r, c) for c in range(cols)] for r in range(rows)]
    sstart = nodes[start[0]][start[1]]
    sgoal = nodes[goal[0]][goal[1]]

    counter = 0
    expanded_nodes = 0

    # initialize search values
    for row in nodes:
        for node in row:
            node.search = 0

    # MAIN LOOP
    while (sstart.r, sstart.c) != (sgoal.r, sgoal.c):
        counter += 1

        sstart.g = 0
        sstart.search = counter
        sgoal.g = math.inf
        sgoal.search = counter

        # update heuristic + reset parents
        for row in nodes:
            for node in row:
                node.h = manhattan_distance(node, sgoal)
                node.parent = None

        expanded_nodes = compute_path(
            sstart, sgoal, grid, nodes, counter, tie_breaker, expanded_nodes
        )

        if sgoal.parent is None:
            return None
        path = []
        cur = sgoal
        while cur != sstart:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        sstart = path[0]

    return expanded_nodes