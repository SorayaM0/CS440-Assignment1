import heapq
import math

def manhattan_rc(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors_from_knowledge(knowledge, r, c):
    rows = len(knowledge)
    cols = len(knowledge[0])
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and knowledge[nr][nc] != '#':
            yield nr, nc

def adaptive_astar_on_knowledge(knowledge, start_rc, goal_rc, h_vals, tie_breaker="large_g"):
    """
    Returns (path, expanded, closed_g)
    path: list of rc from next step after start to goal (excludes start)
    closed_g: dict of expanded nodes -> g
    """
    sr, sc = start_rc
    gr, gc = goal_rc

    if knowledge[sr][sc] == '#' or knowledge[gr][gc] == '#':
        return None, 0, {}

    best_g = {(sr, sc): 0}
    parent = {}
    closed_g = {}
    expanded = 0

    open_heap = []
    push_id = 0

    def push(rc, g):
        nonlocal push_id
        # use adaptive h if available, else manhattan
        h = h_vals.get(rc, manhattan_rc(rc, goal_rc))
        f = g + h
        tie = g if tie_breaker == "small_g" else -g
        heapq.heappush(open_heap, (f, tie, push_id, rc))
        push_id += 1

    push((sr, sc), 0)

    while open_heap:
        _, _, _, (r, c) = heapq.heappop(open_heap)

        # skip if already expanded
        if (r, c) in closed_g:
            continue

        cur_g = best_g.get((r, c), math.inf)
        expanded += 1
        closed_g[(r, c)] = cur_g

        if (r, c) == (gr, gc):
            path = []
            at = (gr, gc)
            while at != (sr, sc):
                path.append(at)
                at = parent[at]
            path.reverse()
            return path, expanded, closed_g

        for nr, nc in neighbors_from_knowledge(knowledge, r, c):
            ng = cur_g + 1
            if ng < best_g.get((nr, nc), math.inf):
                best_g[(nr, nc)] = ng
                parent[(nr, nc)] = (r, c)
                push((nr, nc), ng)

    return None, expanded, closed_g

def adaptive_astar(true_grid, knowledge, start, goal, tie_breaker="large_g"):
    sr, sc = start
    gr, gc = goal

    if true_grid.grid[sr][sc] == '#' or true_grid.grid[gr][gc] == '#':
        return None

    # seed knowledge with what agent can sense at start
    for (r, c), val in true_grid.sense_neighbors(sr, sc).items():
        knowledge[r][c] = val

    h_vals = {}
    cur = (sr, sc)
    moves = 0
    replans = 0
    total_expanded = 0

    while cur != (gr, gc):
        replans += 1

        path, expanded, closed_g = adaptive_astar_on_knowledge(
            knowledge, cur, (gr, gc), h_vals, tie_breaker=tie_breaker
        )
        total_expanded += expanded

        if path is None:
            return None

        # update adaptive heuristics: h(s) = g(goal) - g(s)
        g_goal = closed_g.get((gr, gc))
        if g_goal is not None:
            for s, g_s in closed_g.items():
                h_vals[s] = g_goal - g_s

        # move along planned path, discovering blocks as we go
        for step in path:
            if true_grid.grid[step[0]][step[1]] == '#':
                knowledge[step[0]][step[1]] = '#'
                break

            cur = step
            moves += 1

            sensed = true_grid.sense_neighbors(cur[0], cur[1])
            for (r, c), val in sensed.items():
                knowledge[r][c] = val

            if cur == (gr, gc):
                return {"expanded": total_expanded, "moves": moves, "replans": replans}

    return {"expanded": total_expanded, "moves": moves, "replans": replans}
