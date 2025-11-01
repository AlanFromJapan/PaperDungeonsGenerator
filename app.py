from grid import Grid
from renderer_basic import BasicRenderer


def main():
    print("Hello, World!")
    grid = Grid()
    print(grid)

    renderer = BasicRenderer()
    renderer.to_image(grid, "grid.png", show=True)


if __name__ == "__main__":
    main()