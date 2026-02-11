from grid import GridWorld

def main():
    grid = GridWorld(10, 10)
    grid.generate()
    grid.display()

if __name__ == "__main__":
    main()
