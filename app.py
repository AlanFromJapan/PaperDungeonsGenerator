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


    if "--renderer" in sys.argv:
        renderer_index = sys.argv.index("--renderer") + 1
        if renderer_index < len(sys.argv):
            renderer_type = sys.argv[renderer_index]
            if renderer_type == "basic":
                print("Using Basic Renderer")
                renderer = BasicRenderer()
            elif renderer_type == "sprites":
                print("Using Sprites Renderer")
                renderer = SpritesRenderer()
            else:
                print(f"Unknown renderer type: {renderer_type}. Using Sprites Renderer by default.")
                renderer = SpritesRenderer()
        else:
            print("Error: --renderer flag provided but no renderer type specified.")
            exit(1)
    else:
        print("No renderer specified. Using default Renderer by default.")
        renderer = BasicRenderer()

    #rendering
    grid = Grid()
    grid.GEMINESS = 10
    grid.NEMESISINESS = 1 #classic game style: each monster is nemesis to only one hero class
    grid.generate()

    renderer.IMAGE_CELL_SIZE = 120
    renderer.WALL_WIDTH = 6
    #renderer.sprites["bg"] = "assets/backgrounds/altes-papier-pergament-hintergrund-16602085209L8.jpg"
    renderer.to_image(grid, to_file, show=show_file)

    print(f"Image saved to {to_file}")


if __name__ == "__main__":
    main()