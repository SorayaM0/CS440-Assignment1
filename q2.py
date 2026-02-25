import argparse
import heapq
import json
import math
from typing import List
import time

class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.g = math.inf
        self.h = 0

    def f(self):
        return self.g + self.h

def manhattan(n: Node, goal: Node) -> int:
    return abs(n.r - goal.r) + abs(n.c - goal.c)


def neighbors_from_knowledge(
    knowledge: List[List[str]],
    node: Node
):
    rows = len(knowledge)
    cols = len(knowledge[0])

    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = node.r + dr, node.c + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if knowledge[nr][nc] != "#":
                yield nr, nc

def astar_on_knowledge(knowledge, start, goal, tie_breaker="small_g"):

    sr = start[0]
    sc = start[1]
    gr = goal[0]
    gc = goal[1]

    if knowledge[sr][sc] == "#" or knowledge[gr][gc] == "#":
        return None, 0

    start_node = Node(sr, sc)
    goal_node = Node(gr, gc)

    start_node.g = 0
    start_node.h = manhattan(start_node, goal_node)

    open_heap = []
    push_id = 0
    expanded = 0

    best_g = {}
    best_g[(sr, sc)] = 0

    parent = {}

    def push(node):
        nonlocal push_id

        if tie_breaker == "small_g":
            tie = node.g
        else:
            tie = -node.g

        heapq.heappush(open_heap, (node.f(), tie, push_id, node))
        push_id += 1

    push(start_node)

    while len(open_heap) > 0:
        item = heapq.heappop(open_heap)
        cur = item[3]

        if best_g.get((cur.r, cur.c), math.inf) != cur.g:
            continue

        expanded += 1

        if cur.r == gr and cur.c == gc:
            path = []
            at = (gr, gc)

            while at != (sr, sc):
                path.append(at)
                at = parent[at]

            path.reverse()
            return path, expanded

        for neighbor in neighbors_from_knowledge(knowledge, cur):
            nr = neighbor[0]
            nc = neighbor[1]

            new_g = cur.g + 1

            if new_g < best_g.get((nr, nc), math.inf):
                best_g[(nr, nc)] = new_g
                parent[(nr, nc)] = (cur.r, cur.c)

                next_node = Node(nr, nc)
                next_node.g = new_g
                next_node.h = abs(nr - gr) + abs(nc - gc)

                push(next_node)

    return None, expanded

def repeated_forward_astar(true_grid, knowledge, start, goal, tie_breaker):

    start_time = time.perf_counter()

    sr = start[0]
    sc = start[1]
    gr = goal[0]
    gc = goal[1]

    if true_grid[sr][sc] == "#" or true_grid[gr][gc] == "#":
        return {
            "found": False,
            "path_length": -1,
            "expanded": 0,
            "replans": 0,
            "runtime_ms": 0
        }

    current = start
    moves = 0
    replans = 0
    total_expanded = 0

    while current != goal:

        replans += 1

        path, expanded = astar_on_knowledge(
            knowledge,
            current,
            goal,
            tie_breaker
        )

        total_expanded += expanded

        if path is None:
            runtime = (time.perf_counter() - start_time) * 1000
            return {
                "found": False,
                "path_length": -1,
                "expanded": total_expanded,
                "replans": replans,
                "runtime_ms": runtime
            }

        for step in path:

            r = step[0]
            c = step[1]

            if true_grid[r][c] == "#":
                knowledge[r][c] = "#"
                break

            current = step
            moves += 1

            if current == goal:
                runtime = (time.perf_counter() - start_time) * 1000
                return {
                    "found": True,
                    "path_length": moves,
                    "expanded": total_expanded,
                    "replans": replans,
                    "runtime_ms": runtime
                }

    runtime = (time.perf_counter() - start_time) * 1000
    return {
        "found": True,
        "path_length": moves,
        "expanded": total_expanded,
        "replans": replans,
        "runtime_ms": runtime
    }

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--maze_file", required=True)
    parser.add_argument("--tie_breaking", required=True)
    parser.add_argument("--show_vis", action="store_true")
    parser.add_argument("--maze_vis_id", type=int, default=0)
    parser.add_argument("--save_vis_path")
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    with open(args.maze_file, "r") as f:
        mazes = json.load(f)

    results = []

    for maze_id, maze in enumerate(mazes):
        true_grid = maze["grid"]
        start = tuple(maze["start"])
        goal = tuple(maze["goal"])

        rows = len(true_grid)
        cols = len(true_grid[0])

        def run(strategy):
            knowledge = [["?" for _ in range(cols)] for _ in range(rows)]
            return repeated_forward_astar(
                true_grid,
                knowledge,
                start,
                goal,
                strategy
            )

        if args.tie_breaking == "both":
            result_min = run("small_g")
            result_max = run("large_g")
            results.append({
                "maze_id": maze_id,
                "max_g": result_max,
                "min_g": result_min
            })
        elif args.tie_breaking == "small_g":
            result_min = run("small_g")
            results.append({
                "maze_id": maze_id,
                "max_g": None,
                "min_g": result_min
            })
        elif args.tie_breaking == "large_g":
            result_max = run("large_g")
            results.append({
                "maze_id": maze_id,
                "max_g": result_max,
                "min_g": None
            })
            with open(args.output, "w") as f:
                json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()