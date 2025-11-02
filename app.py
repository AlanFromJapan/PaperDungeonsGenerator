from grid import Grid
from renderer_basic import BasicRenderer
from renderer_sprites import SpritesRenderer
import sys

def main():
    print("Generating grid image with sprites renderer...")

    #Params
    to_file = "grid.png"
    show_file = False
    
    if "--show" in sys.argv:
        show_file = True
    
    if "--output" in sys.argv:
        output_index = sys.argv.index("--output") + 1
        if output_index < len(sys.argv):
            to_file = sys.argv[output_index]
        else:
            print("Error: --output flag provided but no filename specified.")
            exit(1)

    #rendering
    grid = Grid()
    grid.GEMINESS = 10
    grid.generate()

    renderer = SpritesRenderer()
    renderer.IMAGE_CELL_SIZE = 150
    renderer.to_image(grid, to_file, show=show_file)

    print(f"Image saved to {to_file}")


if __name__ == "__main__":
    main()