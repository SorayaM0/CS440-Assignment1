import os
from create_grid_worlds import GridWorld

def main():
    os.makedirs("maps", exist_ok=True)

    for i in range(50):
        gw = GridWorld(101, 101)
        gw.generate()

        # Force start/goal open
        gw.grid[0][0] = '.'
        gw.grid[100][100] = '.'

        filename = f"maps/grid_{i:02d}.txt"
        gw.save_to_file(filename)
        print(f"Saved {filename}")

if __name__ == "__main__":
    main()
