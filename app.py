from grid import Grid


def main():
    print("Hello, World!")
    grid = Grid()
    print(grid)
    grid.to_image("grid.png", show=True)


if __name__ == "__main__":
    main()