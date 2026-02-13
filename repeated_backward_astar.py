from repeated_forward_astar import astar_on_knowledge

def repeated_backward_astar(true_grid, knowledge, start, goal, tie_breaker="small_g"):
    (sr, sc) = start
    (gr, gc) = goal

    if true_grid.grid[sr][sc] == '#' or true_grid.grid[gr][gc] == '#':
        return None

    # initialize knowledge near start
    for (r, c), val in true_grid.sense_neighbors(sr, sc).items():
        knowledge[r][c] = val

    cur = (sr, sc)
    moves = 0
    replans = 0
    total_expanded = 0

    while cur != (gr, gc):
        replans += 1

        # Plan BACKWARD on knowledge: GOAL -> CURRENT
        backward_path, expanded = astar_on_knowledge(
            knowledge,
            (gr, gc),  # start in A*
            cur,       # goal in A*
            tie_breaker=tie_breaker
        )
        total_expanded += expanded

        if backward_path is None:
            return None

        # backward_path is from (gr,gc) to cur, excluding (gr,gc), including cur at the end
        if len(backward_path) == 0 or backward_path[-1] != cur:
            return None

        # Convert to FORWARD steps: CURRENT -> GOAL
        # reverse gives [cur, ..., cell_adjacent_to_goal]
        forward_steps = list(reversed(backward_path))

        # remove cur (we're already there)
        forward_steps = forward_steps[1:]

        # IMPORTANT FIX: append the true goal at the end (because backward_path excluded it)
        forward_steps.append((gr, gc))

        for step in forward_steps:
            # If true grid has a block, update knowledge and replan
            if true_grid.grid[step[0]][step[1]] == '#':
                knowledge[step[0]][step[1]] = '#'
                break

            # Move
            cur = step
            moves += 1

            # Sense and update knowledge
            sensed = true_grid.sense_neighbors(cur[0], cur[1])
            for (r, c), val in sensed.items():
                knowledge[r][c] = val

            if cur == (gr, gc):
                return {"expanded": total_expanded, "moves": moves, "replans": replans}

    return {"expanded": total_expanded, "moves": moves, "replans": replans}
