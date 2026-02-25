import csv
import statistics

print("Reading CSV...")

with open("experiments/part2_tie_breaking.csv", "r") as f:
    rows = list(csv.DictReader(f))

def to_int(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "none":
        return None
    return int(x)

small_expanded = []
large_expanded = []

wins_small = 0
wins_large = 0
ties = 0
both_solved = 0

for r in rows:
    s = to_int(r.get("small_g_expanded"))
    l = to_int(r.get("large_g_expanded"))

    if s is not None:
        small_expanded.append(s)
    if l is not None:
        large_expanded.append(l)

    if s is not None and l is not None:
        both_solved += 1
        if s < l:
            wins_small += 1
        elif l < s:
            wins_large += 1
        else:
            ties += 1

print("Solved maps (small_g):", len(small_expanded))
print("Solved maps (large_g):", len(large_expanded))

if small_expanded:
    print("Average expanded (small_g):", round(statistics.mean(small_expanded), 2))
if large_expanded:
    print("Average expanded (large_g):", round(statistics.mean(large_expanded), 2))

print("Maps solved by both:", both_solved)
print("Wins (small_g fewer expansions):", wins_small)
print("Wins (large_g fewer expansions):", wins_large)
print("Ties:", ties)

import argparse
import json
import copy

from repeated_forward_astar import repeated_forward_astar
from create_grid_worlds import GridWorld  


#### example code
# import argparse
# import json
# import copy
#
# from repeated_forward_astar import repeated_forward_astar
# from gridworld import GridWorld   # <-- adjust if filename differs
#
#
# def main():
#     parser = argparse.ArgumentParser(description="Repeated Forward A* - Tie Breaking")
#
#     parser.add_argument("--maze_file", type=str, required=True)
#     parser.add_argument("--tie_braking", type=str,
#                         choices=["small_g", "large_g", "both"],
#                         required=True)
#     parser.add_argument("--show_vis", action="store_true")
#     parser.add_argument("--maze_vis_id", type=int)
#     parser.add_argument("--save_vis_path", type=str)
#     parser.add_argument("--output", type=str, required=True)
#
#     args = parser.parse_args()
#
#     # Load maze file
#     with open(args.maze_file, "r") as f:
#         maze_files = json.load(f)
#         # This should contain FILE PATHS to mazes
#
#     results = []
#
#     for maze_id, maze_path in enumerate(maze_files):
#
#         true_grid = GridWorld.load_from_file(maze_path)
#
#         start = (0, 0)
#         goal = (true_grid.rows - 1, true_grid.cols - 1)
#
#         # initialize knowledge grid (unknown everywhere)
#         knowledge = [['?' for _ in range(true_grid.cols)]
#                      for _ in range(true_grid.rows)]
#
#         if args.tie_braking == "both":
#             modes = ["small_g", "large_g"]
#         else:
#             modes = [args.tie_braking]
#
#         maze_result = {"maze_id": maze_id}
#
#         for mode in modes:
#             knowledge_copy = copy.deepcopy(knowledge)
#
#             stats = repeated_forward_astar(
#                 true_grid=true_grid,
#                 knowledge=knowledge_copy,
#                 start=start,
#                 goal=goal,
#                 tie_breaker=mode
#             )
#
#             if stats is None:
#                 maze_result[f"{mode}_expanded"] = None
#                 maze_result[f"{mode}_moves"] = None
#                 maze_result[f"{mode}_replans"] = None
#             else:
#                 maze_result[f"{mode}_expanded"] = stats["expanded"]
#                 maze_result[f"{mode}_moves"] = stats["moves"]
#                 maze_result[f"{mode}_replans"] = stats["replans"]
#
#         results.append(maze_result)
#
#     with open(args.output, "w") as f:
#         json.dump(results, f, indent=4)
#
#     print("Results saved to", args.output)
#
#
# if __name__ == "__main__":
#     main()