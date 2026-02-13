from grid import GridWorld
from repeated_forward_astar import repeated_forward_astar

def main():
    true_grid = GridWorld.load_from_file("maps/grid_02.txt")
    true_grid.grid[0][0] = '.'
    true_grid.grid[100][100] = '.'

    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]

    result = repeated_forward_astar(true_grid, knowledge, (0, 0), (100, 100), tie_breaker="large_g")
    print("Forward result:", result)

if __name__ == "__main__":
    main()
