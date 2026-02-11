import random

class GridWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['?' for _ in range(cols)] for _ in range(rows)]

    def generate(self, block_prob=0.30):
        # DFS-style generation with backtracking
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        stack = []

        def in_bounds(r, c):
            return 0 <= r < self.rows and 0 <= c < self.cols

        def unvisited_neighbors(r, c):
            nbrs = []
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and not visited[nr][nc]:
                    nbrs.append((nr, nc))
            return nbrs

        # Start from a random cell
        start_r = random.randrange(self.rows)
        start_c = random.randrange(self.cols)
        visited[start_r][start_c] = True
        self.grid[start_r][start_c] = '.'  # unblocked
        stack.append((start_r, start_c))

        # Visit all cells (if stack empties early, restart from another unvisited cell)
        total_cells = self.rows * self.cols
        visited_count = 1

        while visited_count < total_cells:
            if stack:
                r, c = stack[-1]
                nbrs = unvisited_neighbors(r, c)

                if not nbrs:
                    stack.pop()  # dead-end, backtrack
                    continue

                nr, nc = random.choice(nbrs)
                visited[nr][nc] = True
                visited_count += 1

                # 30% blocked, 70% unblocked
                if random.random() < block_prob:
                    self.grid[nr][nc] = '#'
                    # do NOT push blocked cells (acts like a wall)
                else:
                    self.grid[nr][nc] = '.'
                    stack.append((nr, nc))
            else:
                # Stack empty but still unvisited cells exist -> pick a new unvisited cell
                # (assignment explicitly allows this)
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
