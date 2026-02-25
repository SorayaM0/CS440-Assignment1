import os
import csv
import heapq
import math
from create_grid_worlds import GridWorld

def astar_on_knowledge(knowledge, start, goal, tie_breaker="large_g"):

    rows = len(knowledge)
    cols = len(knowledge[0])

    if knowledge[start[0]][start[1]] == '#' or knowledge[goal[0]][goal[1]] == '#':
        return None, 0

    open_heap = []
    push_id = 0
    expanded = 0

    best_g = {start: 0}
    parent = {}

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def push(cell, g):
        nonlocal push_id
        h = manhattan(cell, goal)
        f = g + h

        tie = g if tie_breaker == "small_g" else -g

        heapq.heappush(open_heap, (f, tie, push_id, cell))
        push_id += 1

    push(start, 0)

    while open_heap:

        _, _, _, current = heapq.heappop(open_heap)

        if best_g[current] != best_g.get(current):
            continue

        expanded += 1

        if current == goal:
            path = []
            cur = goal
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, expanded

        r, c = current

        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols:
                if knowledge[nr][nc] != '#':
                    new_g = best_g[current] + 1

                    if new_g < best_g.get(neighbor, math.inf):
                        best_g[neighbor] = new_g
                        parent[neighbor] = current
                        push(neighbor, new_g)

    return None, expanded

def repeated_forward_astar(true_grid, start, goal, tie="large_g"):

    knowledge = [['.' for _ in range(true_grid.cols)]
                 for _ in range(true_grid.rows)]

    for (r, c), val in true_grid.sense_neighbors(start[0], start[1]).items():
        knowledge[r][c] = val

    current = start
    moves = 0
    replans = 0
    total_expanded = 0

    while current != goal:

        replans += 1

        path, expanded = astar_on_knowledge(
            knowledge, current, goal, tie_breaker=tie
        )

        total_expanded += expanded

        if path is None:
            return None

        for step in path:

            if true_grid.grid[step[0]][step[1]] == '#':
                knowledge[step[0]][step[1]] = '#'
                break

            current = step
            moves += 1

            sensed = true_grid.sense_neighbors(current[0], current[1])
            for (r, c), val in sensed.items():
                knowledge[r][c] = val

            if current == goal:
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

def repeated_backward_astar(true_grid, start, goal, tie="large_g"):

    knowledge = [['.' for _ in range(true_grid.cols)]
                 for _ in range(true_grid.rows)]

    for (r, c), val in true_grid.sense_neighbors(start[0], start[1]).items():
        knowledge[r][c] = val

    current = start
    moves = 0
    replans = 0
    total_expanded = 0

    while current != goal:

        replans += 1

        backward_path, expanded = astar_on_knowledge(
            knowledge, goal, current, tie_breaker=tie
        )

        total_expanded += expanded

        if backward_path is None:
            return None

        forward_steps = list(reversed(backward_path))
        forward_steps = forward_steps[1:]
        forward_steps.append(goal)

        for step in forward_steps:

            if true_grid.grid[step[0]][step[1]] == '#':
                knowledge[step[0]][step[1]] = '#'
                break

            current = step
            moves += 1

            sensed = true_grid.sense_neighbors(current[0], current[1])
            for (r, c), val in sensed.items():
                knowledge[r][c] = val

            if current == goal:
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

def main():

    os.makedirs("experiments", exist_ok=True)
    output_path = "experiments/part3_forward_vs_backward.csv"

    tie = "large_g"
    rows_out = []

    for i in range(50):

        map_name = f"grid_{i:02d}.txt"
        path = os.path.join("maps", map_name)

        true_grid = GridWorld.load_from_file(path)

        true_grid.grid[0][0] = '.'
        true_grid.grid[true_grid.rows - 1][true_grid.cols - 1] = '.'

        forward = repeated_forward_astar(
            true_grid, (0, 0),
            (true_grid.rows - 1, true_grid.cols - 1),
            tie
        )

        backward = repeated_backward_astar(
            true_grid, (0, 0),
            (true_grid.rows - 1, true_grid.cols - 1),
            tie
        )

        rows_out.append({
            "map": map_name,
            "tie_breaker": tie,
            "forward_expanded": "" if forward is None else forward["expanded"],
            "forward_moves": "" if forward is None else forward["moves"],
            "forward_replans": "" if forward is None else forward["replans"],
            "backward_expanded": "" if backward is None else backward["expanded"],
            "backward_moves": "" if backward is None else backward["moves"],
            "backward_replans": "" if backward is None else backward["replans"],
        })

        print(f"Done {i+1}/50")

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows_out[0].keys())
        writer.writeheader()
        writer.writerows(rows_out)

    print("\nSaved results to:", output_path)


if __name__ == "__main__":
    main()