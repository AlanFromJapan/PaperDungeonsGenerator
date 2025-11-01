
from PIL import Image, ImageDraw
from grid import Grid

class BasicRenderer:
    def __init__(self):
        self.objects = []

    def draw_wall(self, draw, x1, y1, x2, y2, is_wall, wall_color, door_color, width=2):
        if is_wall:
            draw.line([(x1, y1), (x2, y2)], fill=wall_color, width=width)
        else:
            draw.line([(x1, y1), (x1 + abs(x2 - x1) // 3, y1 + abs(y2 - y1) // 3)], fill=door_color, width=width)
            draw.line([(x1 + 2 * abs(x2 - x1) // 3, y1 + 2 * abs(y2 - y1) // 3), (x2, y2)], fill=door_color, width=width)


    def to_image(self, g : Grid, filename="grid.png", show=False):
        # Placeholder for image generation logic
        IMAGE_CELL_SIZE = 100  # Size of each cell in pixels
        IMAGE_BG_COLOR = "white"
        IMAGE_WALL_COLOR = "black"
        IMAGE_DOOR_COLOR = "lightgray"

        image = Image.new("RGB", (g.width * IMAGE_CELL_SIZE, g.height * IMAGE_CELL_SIZE), IMAGE_BG_COLOR)
        draw = ImageDraw.Draw(image)
        for y in range(g.height):
            for x in range(g.width):
                cell = g.get_cell(x, y)
                # Draw the cell contents (walls, traps, treasures, monsters)
                for direction, has_wall in cell.walls.items():
                    #is a wall if this cell has a wall in this direction OR the adjacent cell has a wall in the opposite direction
                    is_wall = has_wall
                    if not has_wall:
                        if direction == 'N' and y > 0:
                            is_wall = g.get_cell(x, y - 1).walls['S']
                        elif direction == 'S' and y < g.height - 1:
                            is_wall = g.get_cell(x, y + 1).walls['N']
                        elif direction == 'E' and x < g.width - 1:
                            is_wall = g.get_cell(x + 1, y).walls['W']
                        elif direction == 'W' and x > 0:
                            is_wall = g.get_cell(x - 1, y).walls['E']

                    #draw wall or door
                    if direction == 'N':
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR)
                    elif direction == 'S':
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR)
                    elif direction == 'E':
                        self.draw_wall(draw, (x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR)
                    elif direction == 'W':
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR)

                # Trap? Red dot in bottom left corner
                if cell.traps:
                    dot_radius = 5
                    for trap in cell.traps:
                        trap_position = (x * IMAGE_CELL_SIZE + dot_radius * 2, y * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - dot_radius * 2)
                        draw.ellipse([trap_position[0] - dot_radius, trap_position[1] - dot_radius, trap_position[0] + dot_radius, trap_position[1] + dot_radius], fill="red")

                # Monster? Blue dot in top left corner
                if cell.monsters:
                    dot_radius = 5
                    for monster in cell.monsters:
                        monster_position = (x * IMAGE_CELL_SIZE + dot_radius * 2, y * IMAGE_CELL_SIZE + dot_radius * 2)
                        draw.ellipse([monster_position[0] - dot_radius, monster_position[1] - dot_radius, monster_position[0] + dot_radius, monster_position[1] + dot_radius], fill="blue")
                    # Monster's nemesis classes could be indicated with letter
                    offset = 0
                    for nemesis in monster.nemesis_classes:
                        hero_class, level = nemesis
                        text_position = (x * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - 15 - offset, y * IMAGE_CELL_SIZE  + 10)
                        draw.text(text_position, hero_class.name[0] + str(level), fill="black")
                        offset += 15
                # Treasure? Gold dot in bottom right corner
                if cell.treasures:
                    dot_radius = 5
                    for treasure in cell.treasures:
                        treasure_position = (x * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - dot_radius * 2, y * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - dot_radius * 2)
                        draw.ellipse([treasure_position[0] - dot_radius, treasure_position[1] - dot_radius, treasure_position[0] + dot_radius, treasure_position[1] + dot_radius], fill="gold")


                #Boss? Large red square in center with boss ID number in middle
                if cell.boss_id != 0:
                    square_size = IMAGE_CELL_SIZE // 2
                    top_left = (x * IMAGE_CELL_SIZE + (IMAGE_CELL_SIZE - square_size) // 2, y * IMAGE_CELL_SIZE + (IMAGE_CELL_SIZE - square_size) // 2)
                    bottom_right = (top_left[0] + square_size, top_left[1] + square_size)
                    draw.rectangle([top_left, bottom_right], fill="red")
                    text_position = (top_left[0] + square_size // 4, top_left[1] + square_size // 4)
                    draw.text(text_position, str(cell.boss_id), fill="black")


        image.save(filename)
        if show:
            image.show()            