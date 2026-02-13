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
