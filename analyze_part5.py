import csv, statistics

def to_int(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "none":
        return None
    return int(x)

with open("experiments/part5_adaptive_vs_forward.csv") as f:
    rows = list(csv.DictReader(f))

f_vals = []
a_vals = []
wins_f = wins_a = ties = both = 0

for r in rows:
    fexp = to_int(r.get("forward_expanded"))
    aexp = to_int(r.get("adaptive_expanded"))

    if fexp is not None: f_vals.append(fexp)
    if aexp is not None: a_vals.append(aexp)

    if fexp is not None and aexp is not None:
        both += 1
        if fexp < aexp: wins_f += 1
        elif aexp < fexp: wins_a += 1
        else: ties += 1

print("Solved maps forward:", len(f_vals))
print("Solved maps adaptive:", len(a_vals))
print("Solved by both:", both)
print("Avg expanded forward:", round(statistics.mean(f_vals), 2) if f_vals else None)
print("Avg expanded adaptive:", round(statistics.mean(a_vals), 2) if a_vals else None)
print("Wins forward (fewer expansions):", wins_f)
print("Wins adaptive (fewer expansions):", wins_a)
print("Ties:", ties)
