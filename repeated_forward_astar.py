import heapq
import math

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

def astar_on_knowledge(knowledge, start_rc, goal_rc, tie_breaker="small_g"):
    """
    A* on the agent's knowledge grid.
    Returns (path_as_list_of_rc, expanded_count) or (None, expanded_count).
    """
    rows = len(knowledge)
    cols = len(knowledge[0])

    (sr, sc) = start_rc
    (gr, gc) = goal_rc

    # if knowledge thinks start/goal blocked, no path
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
        # small_g: tie prefers smaller g
        # large_g: tie prefers larger g (use -g)
        tie = n.g if tie_breaker == "small_g" else -n.g
        heapq.heappush(open_heap, (n.f(), tie, push_id, n))
        push_id += 1

    # best g found map + parent map (simpler than storing Node grid)
    best_g = {(sr, sc): 0}
    parent = {}

    push(start)

    while open_heap:
        _, _, _, cur = heapq.heappop(open_heap)

        # stale check
        if best_g.get((cur.r, cur.c), math.inf) != cur.g:
            continue

        expanded += 1

        if (cur.r, cur.c) == (gr, gc):
            # rebuild path
            path = []
            at = (gr, gc)
            while at != (sr, sc):
                path.append(at)
                at = parent[at]
            path.reverse()
            return path, expanded

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

def repeated_forward_astar(true_grid, knowledge, start, goal, tie_breaker="small_g"):
    """
    TRUE Repeated Forward A* with discovery.
    - Plans with A* on knowledge.
    - Moves step-by-step.
    - After each move, senses 4-neighbors in the TRUE grid and updates knowledge.
    Returns dict with stats or None if unreachable.
    """
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

        path, expanded = astar_on_knowledge(knowledge, cur, (gr, gc), tie_breaker=tie_breaker)
        total_expanded += expanded

        if path is None:
            # no presumed-unblocked path exists
            return None

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

            # If next steps in remaining path are now known blocked in knowledge, break to replan
            # (simple check: if any upcoming step is known '#', replan)
            # We'll let the loop continue unless we want faster detection; this is enough for correctness.

    return {
        "expanded": total_expanded,
        "moves": moves,
        "replans": replans
    }
