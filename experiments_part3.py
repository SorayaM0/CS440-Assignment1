import os
import csv

from create_grid_worlds import GridWorld
from repeated_forward_astar import repeated_forward_astar
from repeated_backward_astar import repeated_backward_astar

def run_forward(true_grid, tie="large_g"):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return repeated_forward_astar(true_grid, knowledge, (0, 0), (true_grid.rows - 1, true_grid.cols - 1), tie_breaker=tie)

def run_backward(true_grid, tie="large_g"):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return repeated_backward_astar(true_grid, knowledge, (0, 0), (true_grid.rows - 1, true_grid.cols - 1), tie_breaker=tie)

def main():
    os.makedirs("experiments", exist_ok=True)
    out_path = "experiments/part3_forward_vs_backward.csv"

    rows_out = []
    for i in range(50):
        map_name = f"grid_{i:02d}.txt"
        path = os.path.join("maps", map_name)

        true_grid = GridWorld.load_from_file(path)

        # Make sure start/goal are open
        true_grid.grid[0][0] = '.'
        true_grid.grid[true_grid.rows - 1][true_grid.cols - 1] = '.'

        # Use the better tie-breaker from Part 2
        tie = "large_g"

        f = run_forward(true_grid, tie)
        b = run_backward(true_grid, tie)

        rows_out.append({
            "map": map_name,
            "tie_breaker": tie,

            "forward_expanded": "" if f is None else f["expanded"],
            "forward_moves": "" if f is None else f["moves"],
            "forward_replans": "" if f is None else f["replans"],

            "backward_expanded": "" if b is None else b["expanded"],
            "backward_moves": "" if b is None else b["moves"],
            "backward_replans": "" if b is None else b["replans"],
        })

        print(f"Done {i+1}/50")

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nSaved results to: {out_path}")

if __name__ == "__main__":
    main()
