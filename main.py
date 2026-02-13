from grid import GridWorld
from repeated_backward_astar import repeated_backward_astar

def main():
    true_grid = GridWorld.load_from_file("maps/grid_01.txt")
    true_grid.grid[0][0] = '.'
    true_grid.grid[100][100] = '.'

    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]

    result = repeated_backward_astar(true_grid, knowledge, (0, 0), (100, 100), tie_breaker="small_g")
    print("Backward result:", result)

if __name__ == "__main__":
    main()
