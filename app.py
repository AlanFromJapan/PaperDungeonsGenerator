from grid import Grid
from renderer_basic import BasicRenderer
from renderer_sprites import SpritesRenderer


def main():
    print("Hello, World!")
    grid = Grid()
    print(grid)

    renderer = SpritesRenderer()
    renderer.to_image(grid, "grid.png", show=True)


if __name__ == "__main__":
    main()