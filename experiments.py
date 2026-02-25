import os
import csv
from create_grid_worlds import GridWorld
from repeated_forward_astar import repeated_forward_astar
from repeated_backward_astar import repeated_backward_astar

def run_forward(true_grid, tie):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return repeated_forward_astar(true_grid, knowledge, (0,0), (true_grid.rows-1, true_grid.cols-1), tie_breaker=tie)

def run_backward(true_grid, tie):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return repeated_backward_astar(true_grid, knowledge, (0,0), (true_grid.rows-1, true_grid.cols-1), tie_breaker=tie)

def main():
    os.makedirs("experiments", exist_ok=True)

    out_path = "experiments/part3_forward_vs_backward.csv"
    maps_dir = "maps"

    rows = []
    for i in range(50):
        path = os.path.join(maps_dir, f"grid_{i:02d}.txt")
        true_grid = GridWorld.load_from_file(path)

        # Force start/goal open
        true_grid.grid[0][0] = '.'
        true_grid.grid[true_grid.rows-1][true_grid.cols-1] = '.'

        # Use SAME tie-breaker for fair forward vs backward comparison
        tie = "large_g"   # (use large_g since it dominated in Part 2)

        f = run_forward(true_grid, tie)
        b = run_backward(true_grid, tie)

        rows.append({
            "map": f"grid_{i:02d}.txt",

            "forward_expanded": None if f is None else f["expanded"],
            "forward_moves": None if f is None else f["moves"],
            "forward_replans": None if f is None else f["replans"],

            "backward_expanded": None if b is None else b["expanded"],
            "backward_moves": None if b is None else b["moves"],
            "backward_replans": None if b is None else b["replans"],
        })

        print(f"Done {i+1}/50")

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {out_path}")

if __name__ == "__main__":
    main()
