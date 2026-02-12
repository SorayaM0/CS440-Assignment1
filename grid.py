import random

class GridWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['?' for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def sense_neighbors(self, r, c):
        """
        Returns dict of neighbor cells in the TRUE grid:
        {(nr,nc): '.' or '#'}
        """
        sensed = {}
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                sensed[(nr, nc)] = self.grid[nr][nc]
        return sensed

    def generate(self, block_prob=0.30):
        # DFS-style generation with backtracking
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        stack = []

        def unvisited_neighbors(r, c):
            nbrs = []
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc) and not visited[nr][nc]:
                    nbrs.append((nr, nc))
            return nbrs

        # start random
        sr = random.randrange(self.rows)
        sc = random.randrange(self.cols)
        visited[sr][sc] = True
        self.grid[sr][sc] = '.'
        stack.append((sr, sc))

        total = self.rows * self.cols
        visited_count = 1

        while visited_count < total:
            if stack:
                r, c = stack[-1]
                nbrs = unvisited_neighbors(r, c)
                if not nbrs:
                    stack.pop()
                    continue

                nr, nc = random.choice(nbrs)
                visited[nr][nc] = True
                visited_count += 1

                if random.random() < block_prob:
                    self.grid[nr][nc] = '#'
                else:
                    self.grid[nr][nc] = '.'
                    stack.append((nr, nc))
            else:
                # restart from an unvisited cell
                unvisited = [(rr, cc) for rr in range(self.rows) for cc in range(self.cols) if not visited[rr][cc]]
                rr, cc = random.choice(unvisited)
                visited[rr][cc] = True
                visited_count += 1

                if random.random() < block_prob:
                    self.grid[rr][cc] = '#'
                else:
                    self.grid[rr][cc] = '.'
                    stack.append((rr, cc))

    def display(self):
        for row in self.grid:
            print(" ".join(row))

    def save_to_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(f"{self.rows} {self.cols}\n")
            for row in self.grid:
                f.write("".join(row) + "\n")

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as f:
            rows, cols = map(int, f.readline().strip().split())
            gw = GridWorld(rows, cols)
            for r in range(rows):
                line = f.readline().rstrip("\n")
                gw.grid[r] = list(line)
        return gw
