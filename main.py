from create_grid_worlds import GridWorld
from adaptive_astar import adaptive_astar

def main():
    # Load a known solvable map
    g = GridWorld.load_from_file("maps/grid_02.txt")

    # Make sure start and goal are open
    g.grid[0][0] = '.'
    g.grid[g.rows - 1][g.cols - 1] = '.'

    # Agent knowledge (initially assumes all open)
    knowledge = [['.' for _ in range(g.cols)] for _ in range(g.rows)]

    result = adaptive_astar(
        g,
        knowledge,
        (0, 0),
        (g.rows - 1, g.cols - 1),
        tie_breaker="large_g"
    )

    print("Adaptive result:", result)

if __name__ == "__main__":
    main()
