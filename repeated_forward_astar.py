import heapq
import math

class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.g = math.inf
        self.h = 0
        self.parent = None
        self.search = 0  # counter value when last initialized

    def f(self):
        return self.g + self.h

def manhattan(n: Node, goal: Node) -> int:
    return abs(n.r - goal.r) + abs(n.c - goal.c)

def neighbors(gridworld, n: Node):
    # 4-neighbors; treat '#' as blocked
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = n.r + dr, n.c + dc
        if 0 <= nr < gridworld.rows and 0 <= nc < gridworld.cols:
            if gridworld.grid[nr][nc] != '#':
                yield nr, nc

def compute_path(start: Node, goal: Node, gridworld, nodes, counter: int, tie_breaker: str):
    """
    Returns: (found_path_bool, expanded_count)
    """
    open_heap = []
    in_open = set()
    expanded = 0
    push_id = 0  # strictly increasing to avoid Node comparisons in heap

    def push(n: Node):
        nonlocal push_id
        # tie-breaking:
        # small_g => prefer smaller g when f ties
        # large_g => prefer larger g when f ties  (implemented via -g)
        if tie_breaker == "small_g":
            tie = n.g
        else:
            tie = -n.g

        heapq.heappush(open_heap, (n.f(), tie, push_id, n))
        in_open.add((n.r, n.c))
        push_id += 1

    push(start)

    # While OPEN not empty and g(goal) > min f in OPEN
    while open_heap and goal.g > open_heap[0][0]:
        _, _, _, s = heapq.heappop(open_heap)
        if (s.r, s.c) not in in_open:
            continue
        in_open.remove((s.r, s.c))

        expanded += 1

        for nr, nc in neighbors(gridworld, s):
            succ = nodes[nr][nc]

            if succ.search < counter:
                succ.g = math.inf
                succ.search = counter
                succ.parent = None

            # cost is 1 per move
            if succ.g > s.g + 1:
                succ.g = s.g + 1
                succ.parent = s

                # update priority: easiest way is push again (lazy)
                push(succ)

    return (goal.g < math.inf), expanded

def repeated_forward_astar(gridworld, start, goal, tie_breaker="small_g"):
    """
    For now: uses the full gridworld as known (good for testing).
    Returns expanded node count, or None if no path.
    """
    rows, cols = gridworld.rows, gridworld.cols
    nodes = [[Node(r, c) for c in range(cols)] for r in range(rows)]

    sr, sc = start
    gr, gc = goal
    sstart = nodes[sr][sc]
    sgoal = nodes[gr][gc]

    # Safety: start/goal must not be blocked
    if gridworld.grid[sr][sc] == '#' or gridworld.grid[gr][gc] == '#':
        return None

    counter = 0
    total_expanded = 0

    while (sstart.r, sstart.c) != (sgoal.r, sgoal.c):
        counter += 1

        # init start/goal for this search
        sstart.g = 0
        sstart.search = counter
        sstart.parent = None

        sgoal.g = math.inf
        sgoal.search = counter
        sgoal.parent = None

        # set heuristics for all nodes (simple + correct)
        for r in range(rows):
            for c in range(cols):
                nodes[r][c].h = manhattan(nodes[r][c], sgoal)

        found, expanded = compute_path(sstart, sgoal, gridworld, nodes, counter, tie_breaker)
        total_expanded += expanded

        if not found:
            return None

        # rebuild path and move one step
        path = []
        cur = sgoal
        while cur and cur != sstart:
            path.append(cur)
            cur = cur.parent
        path.reverse()

        if not path:
            break

        # move agent one step along planned path
        sstart = path[0]

    return total_expanded
