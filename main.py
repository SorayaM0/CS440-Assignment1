from grid import GridWorld
from repeated_forward_astar import repeated_forward_astar
from repeated_backward_astar import repeated_backward_astar
from adaptive_astar import adaptive_astar

def print_knowledge(knowledge, max_rows=10, max_cols=10):
    r = min(len(knowledge), max_rows)
    c = min(len(knowledge[0]), max_cols)
    for i in range(r):
        print(" ".join(knowledge[i][:c]))

def main():
    attempts = 0

    while True:
        attempts += 1

        true_grid = GridWorld(10, 10)
        true_grid.generate()

        # force start/goal open for testing
        true_grid.grid[0][0] = '.'
        true_grid.grid[9][9] = '.'

        # agent knowledge: assumes unknown cells are open ('.')
        knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]

        result = repeated_backward_astar(true_grid, knowledge, (0, 0), (9, 9), tie_breaker="small_g")

        if result is not None:
            print(f"Reached goal after {attempts} tries\n")

            print("TRUE GRID:")
            true_grid.display()

            print("\nAGENT KNOWLEDGE (end):")
            print_knowledge(knowledge)

            print("\nStats:", result)
            break

if __name__ == "__main__":
    main()
