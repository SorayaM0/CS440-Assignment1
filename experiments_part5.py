import os
import csv
from create_grid_worlds import GridWorld
from repeated_forward_astar import repeated_forward_astar
from adaptive_astar import adaptive_astar

def run_forward(true_grid, tie="large_g"):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return repeated_forward_astar(true_grid, knowledge, (0,0), (true_grid.rows-1, true_grid.cols-1), tie_breaker=tie)

def run_adaptive(true_grid, tie="large_g"):
    knowledge = [['.' for _ in range(true_grid.cols)] for _ in range(true_grid.rows)]
    return adaptive_astar(true_grid, knowledge, (0,0), (true_grid.rows-1, true_grid.cols-1), tie_breaker=tie)

def main():
    os.makedirs("experiments", exist_ok=True)
    out_path = "experiments/part5_adaptive_vs_forward.csv"

    rows_out = []
    for i in range(50):
        map_name = f"grid_{i:02d}.txt"
        path = os.path.join("maps", map_name)
        true_grid = GridWorld.load_from_file(path)

        true_grid.grid[0][0] = '.'
        true_grid.grid[true_grid.rows-1][true_grid.cols-1] = '.'

        tie = "large_g"

        f = run_forward(true_grid, tie)
        a = run_adaptive(true_grid, tie)

        rows_out.append({
            "map": map_name,
            "tie_breaker": tie,

            "forward_expanded": "" if f is None else f["expanded"],
            "forward_moves": "" if f is None else f["moves"],
            "forward_replans": "" if f is None else f["replans"],

            "adaptive_expanded": "" if a is None else a["expanded"],
            "adaptive_moves": "" if a is None else a["moves"],
            "adaptive_replans": "" if a is None else a["replans"],
        })

        print(f"Done {i+1}/50")

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nSaved results to: {out_path}")

if __name__ == "__main__":
    main()
