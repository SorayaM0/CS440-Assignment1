from repeated_forward_astar import astar_on_knowledge

def repeated_backward_astar(true_grid, knowledge, start, goal, tie_breaker="small_g"):
    (sr, sc) = start
    (gr, gc) = goal

    if true_grid.grid[sr][sc] == '#' or true_grid.grid[gr][gc] == '#':
        return None

    for (r, c), val in true_grid.sense_neighbors(sr, sc).items():
        knowledge[r][c] = val

    cur = (sr, sc)
    moves = 0
    replans = 0
    total_expanded = 0

    while cur != (gr, gc):
        replans += 1

        backward_path, expanded = astar_on_knowledge(
            knowledge,
            (gr, gc),
            cur,
            tie_breaker=tie_breaker
        )
        total_expanded += expanded

        if backward_path is None:
            return None

        if len(backward_path) == 0 or backward_path[-1] != cur:
            return None

        forward_steps = list(reversed(backward_path))
        forward_steps = forward_steps[1:]
        forward_steps.append((gr, gc))

        for step in forward_steps:
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
