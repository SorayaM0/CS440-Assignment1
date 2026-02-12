from grid import GridWorld
from repeated_forward_astar import repeated_forward_astar

def main():
    attempts = 0

    while True:
        attempts += 1

        grid = GridWorld(10, 10)
        grid.generate()

        # Force start/goal open for testing
        grid.grid[0][0] = '.'
        grid.grid[9][9] = '.'

        start = (0, 0)
        goal = (9, 9)

        expanded = repeated_forward_astar(grid, start, goal, tie_breaker="small_g")

        # If a path exists, print and stop
        if expanded is not None:
            print(f"Found a path after {attempts} tries\n")
            grid.display()
            print("\nExpanded nodes:", expanded)
            break

if __name__ == "__main__":
    main()
