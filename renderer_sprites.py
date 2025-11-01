
from PIL import Image, ImageDraw
from grid import Grid
from renderer_basic import BasicRenderer

class SpritesRenderer(BasicRenderer):
    sprites = {
        "trap": "assets/sprites/trap24.png",

        "potion": "assets/sprites/potion24.png",
        "artifact": "assets/sprites/artifact24.png",
        "gems": "assets/sprites/gem24.png",
        "level_up": "assets/sprites/levelup24.png",

        "cleric": "assets/sprites/cleric24.png",
        "mage": "assets/sprites/mage24.png",
        "rogue": "assets/sprites/rogue24.png",
        "warrior": "assets/sprites/warrior24.png",

        "goblin": "assets/sprites/gobelin24.png",
        "troll": "assets/sprites/troll24.png",
        "dragon": "assets/sprites/dragon24.png",
        "skeleton": "assets/sprites/skel24.png",

        "boss": "assets/sprites/boss24.png",
    }

    def __init__(self):
        self.objects = []

    def to_image(self, g : Grid, filename="grid.png", show=False):
        # Placeholder for image generation logic
        IMAGE_CELL_SIZE = 100  # Size of each cell in pixels
        IMAGE_BG_COLOR = "white"
        IMAGE_WALL_COLOR = "black"
        IMAGE_DOOR_COLOR = "lightgray"
        SPRITES_PADDING = 4
        WALL_WIDTH = 4

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
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR, width=WALL_WIDTH)
                    elif direction == 'S':
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR, width=WALL_WIDTH)
                    elif direction == 'E':
                        self.draw_wall(draw, (x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, (x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR, width=WALL_WIDTH)
                    elif direction == 'W':
                        self.draw_wall(draw, x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE, x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE, is_wall, IMAGE_WALL_COLOR, IMAGE_DOOR_COLOR, width=WALL_WIDTH)

                # Trap? Red dot in bottom left corner
                if cell.traps and len(cell.traps) > 0:
                    sprite = Image.open(self.sprites["trap"])
                    trap_position = (x * IMAGE_CELL_SIZE + SPRITES_PADDING, y * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - SPRITES_PADDING - sprite.size[1])
                    image.paste(sprite, trap_position, sprite)
                    print("Drawing trap at", trap_position)

                # Monster? Blue dot in top left corner
                if cell.monsters:
                    offset = 0
                    for monster in cell.monsters:
                        sprite = Image.open(self.sprites[monster.name.lower()]) 

                        monster_position = (x * IMAGE_CELL_SIZE + SPRITES_PADDING + offset, y * IMAGE_CELL_SIZE + SPRITES_PADDING )
                        image.paste(sprite, monster_position, sprite)
                        # Monsters overlap a bit if multiple
                        offset += sprite.size[0] // 2

                    # Monster's nemesis classes could be indicated with letter
                    offset = 0
                    for nemesis in monster.nemesis_classes:
                        hero_class, level = nemesis

                        sprite = Image.open(self.sprites[hero_class.name.lower()]) 
                        nemesis_position = (x * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - SPRITES_PADDING - sprite.size[0] - offset, y * IMAGE_CELL_SIZE + SPRITES_PADDING)
                        image.paste(sprite, nemesis_position, sprite)
                        # Draw level next to nemesis sprite
                        text_position = (x * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - SPRITES_PADDING - offset - 6, y * IMAGE_CELL_SIZE + SPRITES_PADDING + sprite.size[1] - 12)
                        draw.text(text_position, str(level), fill="black")
                        # Nemesis indicators side by side (no overlap)
                        offset += sprite.size[0]

                # Treasure? Gold dot in bottom right corner
                if cell.treasures:
                    offset = 0
                    for treasure in cell.treasures:
                        sprite = Image.open(self.sprites[treasure.treasure_type.name.lower()])
                        treasure_position = (x * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - SPRITES_PADDING - sprite.size[0] - offset, y * IMAGE_CELL_SIZE + IMAGE_CELL_SIZE - SPRITES_PADDING - sprite.size[1])
                        image.paste(sprite, treasure_position, sprite)
                        # Treasures overlap a bit if multiple
                        offset += sprite.size[0] // 2


                #Boss? Large red square in center with boss ID number in middle
                if cell.boss_id != 0:
                    sprite = Image.open(self.sprites["boss"])

                    offset = IMAGE_CELL_SIZE // 2 - sprite.size[0] // 2
                    top_left = (x * IMAGE_CELL_SIZE + offset, y * IMAGE_CELL_SIZE + offset)
                    bottom_right = (top_left[0] + sprite.size[0], top_left[1] + sprite.size[1])
                    draw.rectangle([top_left, bottom_right], fill="red")

                    image.paste(sprite, top_left, sprite)

                    offset = IMAGE_CELL_SIZE // 2 - 6
                    text_position = (x * IMAGE_CELL_SIZE + offset + 3, y * IMAGE_CELL_SIZE + offset + 5)
                    draw.text(text_position, str(cell.boss_id), fill="black")


        image.save(filename)
        if show:
            image.show()            