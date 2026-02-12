
# TODO (Part 5):
# Implement Adaptive A*
## Adaptive A* finds the shortest paths with possibly different start states but the SAME goal state
## Action costs can increase by arbitrary amounts between A* searches

import heapq, math

# Node class
class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.g = math.inf
        self.h = 0
        self.parent = None
        self.search = 0

    def f(self):
        return self.g + self.h

# Manhattan distance
def manhattan(n: Node, goal: Node) -> int:
    return abs(n.r - goal.r) + abs(n.c - goal.c)

# Knowledge block
def neighbors_from_knowledge(knowledge, n: Node):
    rows = len(knowledge)
    cols = len(knowledge[0])

    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = n.r + dr, n.c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if knowledge[nr][nc] != '#':
                yield nr, nc

def adaptive_astar_on_knowledge(knowledge, start_rc, goal_rc, h_vals, tie_breaker = "small_g"):
    ## Adaptive A* on knowledge grid
    ##Returns (path, expanded_count, closed_set_g_values)

    rows = len(knowledge)
    cols = len(knowledge[0])

    (sr, sc) = start_rc
    (gr, gc) = goal_rc

    # if knowledge thinks start/goal blocked, no path
    if knowledge[sr][sc] == '#' or knowledge[gr][gc] == '#':
        return None, {}

    start = Node(sr, sc)
    goal = Node(gr, gc)

    # goal = 0, heuristic = 
    start.g = 0
    start.h = h_vals.get((sr, sc), manhattan(start, goal))

    open_heap = []
    push_id = 0
    expanded = 0

    def push(n: Node):
        nonlocal push_id
        # small_g: tie prefers smaller g
        # large_g: tie prefers larger g (use -g)
        tie = n.g if tie_breaker == "small_g" else -n.g
        heapq.heappush(open_heap, (n.f(), tie, push_id, n))
        push_id += 1

    # best g found map, best parent
    # store g-values of expanded nodes to be adapted later into the algorithm
    best_g = {(sr, sc): 0}
    parent = {}
    closed = {}

    push(start)

    while open_heap:
        _, _, _, cur = heapq.heappop(open_heap)
        if best_g.get((cur.r, cur.c), math.inf) != cur.g:
            continue
        expanded += 1
    closed[(cur.r, cur.c)] = cur.g # add to closed list

    if (cur.r, cur.c) == (gr, gc):
            # rebuild path
            path = []
            at = (gr, gc)
            while at != (sr, sc):
                path.append(at)
                at = parent[at]
            path.reverse()
            return path, expanded, closed
    
    for nr, nc in neighbors_from_knowledge(knowledge, cur):
        ng = cur.g + 1
        if ng < best_g.get((nr, nc), math.inf):
            best_g[(nr, nc)] = ng
            parent[(nr, nc)] = (cur.r, cur.c)

            nxt = Node(nr, nc)
            nxt.g = ng
            nxt.h = h_vals.get((nr, nc), abs(nr - gr) + abs(nc - gc))
            push(nxt)

    return None, expanded, closed

def adaptive_astar(true_grid, knowledge, start, goal, tie_breaker = "small_g"):

    (sr, sc) = start
    (gr, gc) = goal

    # start/goal must be unblocked in the grid
    if true_grid.grid[sr][sc] == '#' or true_grid.grid[gr][gc] == '#':
        return None
    
    h_val_list = {} # stores all adaptive h values
    cur = (sr, sc)
    moves = 0
    replans = 0
    total_expanded = 0

    while cur != (gr, gc):
        replans += 1
        path, expanded, g_values = adaptive_astar_on_knowledge(knowledge, cur, (gr, gc), h_val_list, tie_breaker = tie_breaker)
        total_expanded = total_expanded

        if path is None: return None  # no presumed-unblocked path exists

        # Adaptive A* updates the heuristic values with h(s) = g(s_goal) - g(s)
        s_goal = g_values.get((gr, gc), None)
        if s_goal is not None:
            for state, g_s in g_values.items():
                h_val_list[state] = s_goal - g_s

        # Same as in Repeated A* algorithm
        # Follow planned path until it breaks or goal reached
        for step in path:
            # If the TRUE grid has a block here, we discovered our assumption was wrong:
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
        "expanded": total_expanded, "moves": moves, "replans": replans
    }



