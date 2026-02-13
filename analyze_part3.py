import csv
import statistics

def to_int(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() == "none":
        return None
    return int(x)

with open("experiments/part3_forward_vs_backward.csv") as f:
    rows = list(csv.DictReader(f))

f_vals = []
b_vals = []

wins_f = 0
wins_b = 0
ties = 0
both = 0

for r in rows:
    fexp = to_int(r.get("forward_expanded"))
    bexp = to_int(r.get("backward_expanded"))

    if fexp is not None:
        f_vals.append(fexp)
    if bexp is not None:
        b_vals.append(bexp)

    if fexp is not None and bexp is not None:
        both += 1
        if fexp < bexp:
            wins_f += 1
        elif bexp < fexp:
            wins_b += 1
        else:
            ties += 1

print("Solved maps forward:", len(f_vals))
print("Solved maps backward:", len(b_vals))
print("Solved by both:", both)

if f_vals:
    print("Avg expanded forward:", round(statistics.mean(f_vals), 2))
if b_vals:
    print("Avg expanded backward:", round(statistics.mean(b_vals), 2))

print("Wins forward (fewer expansions):", wins_f)
print("Wins backward (fewer expansions):", wins_b)
print("Ties:", ties)
