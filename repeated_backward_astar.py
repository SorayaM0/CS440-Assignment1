
# TODO (Part 3):
# Implement Repeated Backward A*

# Moves from the target TOWARDS the current cell

import heapq, math

class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.g = math.inf
        self.h = 0
        self.parent = None

    def f(self):
        return self.g + self.h

def manhattan(n: Node, goal: Node) -> int:
    return abs(n.r - goal.r) + abs(n.c - goal.c)

def neighbors_from_knowledge(knowledge, n: Node):
    rows = len(knowledge)
    cols = len(knowledge[0])

    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = n.r + dr, n.c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if knowledge[nr][nc] != '#':
                yield nr, nc

def backward_astar_on_knowledge(knowledge, start_rc, goal_rc, tie_breaker="small_g"):
    ## A* search where start = goal/target, goal = agent cell (start) --> backwards
    ## Returns (path_as_list_of_rc, expanded_count) or (None, expanded_count).

    (sr, sc) = start_rc # target
    (gr, gc) = goal_rc # start

    if knowledge[sr][sc] == '#' or knowledge[gr][gc] == '#':
        return None, 0
    
    start = Node(sr, sc)
    goal = Node(gr, gc)

    start.g = 0
    start.h = manhattan(start, goal)

    open_heap = []
    push_id = 0
    expanded = 0

    def push(n: Node):
        nonlocal push_id
        tie = n.g if tie_breaker == "small_g" else -n.g
        heapq.heappush(open_heap, (n.f(), tie, push_id, n))
        push_id += 1

    best_g = {(sr, sc): 0}
    parent = {}
    push(start)

    while open_heap:
        _, _, _, cur = heapq.heappop(open_heap)

        if best_g.get((cur.r, cur.c), math.inf)!= cur.g:
            continue
            
        expanded += 1

        if (cur.r, cur.c) == (gr, gc):
            path = []
            at = (gr, gc)
            while at != (sr, sc):
                path.append(at)
                at = parent[at]

            path.reverse()
            # returns reverse order for backware a*
            return path[1:], expanded

        for nr, nc in neighbors_from_knowledge(knowledge, cur):
            ng = cur.g + 1
            if ng < best_g.get((nr, nc), math.inf):
                best_g[(nr, nc)] = ng
                parent[(nr, nc)] = (cur.r, cur.c)

                nxt = Node(nr, nc)
                nxt.g = ng
                nxt.h = abs(nr - gr) + abs(nc - gc)
                push(nxt)
    return None, expanded

def repeated_backward_astar(true_grid, knowledge, start, goal, tie_breaker="small_g"):

    # initialize start, goal, grid (same as repeated forward a star)
    (sr, sc) = start
    (gr, gc) = goal

    # start/goal must be unblocked in the TRUE grid
    if true_grid.grid[sr][sc] == '#' or true_grid.grid[gr][gc] == '#':
        return None

    # initialize: agent knows neighbors of start (optional but helpful)
    for (r, c), val in true_grid.sense_neighbors(sr, sc).items():
        knowledge[r][c] = val

    cur = (sr, sc)
    moves = 0
    replans = 0
    total_expanded = 0

    while cur != (gr, gc):

        replans += 1

        path, expanded = backward_astar_on_knowledge(knowledge, (gr, gc), cur, tie_breaker=tie_breaker)
        total_expanded += expanded

        if path is None:
            return None

        
        for step in path:
            if true_grid.grid[step[0]][step[1]] == '#':
                knowledge[step[0]][step[1]] = '#'
                break
            # Move one step
            cur = step
            moves += 1

            # Sense neighbors in TRUE grid, update knowledge
            sensed = true_grid.sense_neighbors(cur[0], cur[1])
            for (r, c), val in sensed.items():
                knowledge[r][c] = val

            if cur == (gr, gc):
                return {
                    "expanded": total_expanded,
                    "moves": moves,
                    "replans": replans
                }
            
    return {
        "expanded": total_expanded,
        "moves": moves,
        "replans": replans
    }