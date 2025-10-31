from enum import Enum
import random
from PIL import Image, ImageDraw

# Walliness factor for random grid generation (percentage of chance of having walls)
WALLINESS = 25
TRAPINESS = 30
GEMINESS = 15
TREASURINESS = 20
TREASURINESS_DOUBLE = 30
MONSTERINESS = 30

class TreasureType(Enum):
    GEMS = "gems"
    POTION = "potion"
    ARTIFACT = "artifact"
    LEVEL_UP = "level_up"

class HeroesType(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"

class Monster:
    def __init__(self, name, nemesis_classes=[]):
        self.name = name
        self.nemesis_classes = nemesis_classes

    @classmethod
    def random_monster(cls):
        monster_names = ["Goblin", "Orc", "Troll", "Dragon", "Skeleton"]
        name = random.choice(monster_names)
        heroes_classes = random.sample(list(HeroesType), k=random.randint(1, 2))
        nemesis_classes = []
        for hero_class in heroes_classes:
            nemesis_classes.append((hero_class, random.randint(1, 6)))
        return cls(name, nemesis_classes)
    
    def __repr__(self):
        return f"Monster({self.name}, Nemesis: {self.nemesis_classes})"

class Treasure:
    def __init__(self, treasure_type: TreasureType = TreasureType.POTION):
        self.treasure_type = treasure_type

class Cell:
    def __init__(self):
        self.walls = {'N': False, 'S': False, 'E': False, 'W': False}
        self.traps = []
        self.treasures = []
        self.items = []
        self.monsters = []
        self.warps = []
        self.boss_id = 0


    def remove_wall(self, direction):
        if direction in self.walls:
            self.walls[direction] = False

    def add_wall(self, direction):
        if direction in self.walls:
            self.walls[direction] = True
    
    def randomize(self):
        # Set a random wall based on WALLINESS factor
        if random.randint(1, 100) <= WALLINESS:
            self.walls[random.choice(['N', 'S', 'E', 'W'])] = True
        if random.randint(1, 100) <= TRAPINESS:
            self.traps.append("Trap")
        if random.randint(1, 100) <= GEMINESS:
            #if gem then mandatory monster
            self.treasures.append(Treasure(TreasureType.GEMS))
            self.monsters.append(Monster.random_monster())
        else:
            #no gem then MAYBE treasure
            if random.randint(1, 100) <= TREASURINESS:
                treasure_type = random.choice(list(TreasureType))
                self.treasures.append(Treasure(treasure_type))
                # maybe double treasure?
                if random.randint(1, 100) <= TREASURINESS_DOUBLE:
                    treasure_type = random.choice(list(TreasureType))
                    self.treasures.append(Treasure(treasure_type))
            #maybe monster
            if random.randint(1, 100) <= MONSTERINESS:  # 30% chance of monster
                self.monsters.append(Monster.random_monster())

    @classmethod
    def generate_random_cell(cls):
        cell = cls()
        cell.randomize()
        return cell

    def __repr__(self):
        return f"Cell(Walls: {self.walls}, Traps: {self.traps}, Treasures: {self.treasures}, Monsters: {self.monsters})"


class Grid:
    def __init__(self, width = 6, height = 7):
        self.width = width
        self.height = height
        #make grid
        self.cells = [[Cell.generate_random_cell() for _ in range(width)] for _ in range(height)]
        #add bosses
        self.randomize_bosses(bosses_count=3)
        #cosmetics
        self.fence_grid()


    def randomize_bosses(self, bosses_count):
        placed_bosses = 0
        while placed_bosses < bosses_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            cell = self.get_cell(x, y)
            if cell.boss_id == 0:  # No boss assigned yet
                cell.boss_id = placed_bosses + 1  # Assign a unique boss ID
                placed_bosses += 1

                #if boss the no monster
                cell.monsters.clear()
    

    def fence_grid(self):
        """Add walls around the perimeter of the grid."""
        for x in range(self.width):
            self.get_cell(x, 0).add_wall('N')
            self.get_cell(x, self.height - 1).add_wall('S')
        for y in range(self.height):
            self.get_cell(0, y).add_wall('W')
            self.get_cell(self.width - 1, y).add_wall('E')


    def __repr__(self):
        grid_repr = ""
        for row in self.cells:
            grid_repr += "||"
            for cell in row:
                grid_repr += repr(cell) + "|"
            grid_repr += "||\n"
        return grid_repr
    
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds")
        
    def to_image(self, filename="grid.png", show=False):
        # Placeholder for image generation logic
        IMAGE_CELL_SIZE = 100  # Size of each cell in pixels
        IMAGE_BG_COLOR = "white"
        IMAGE_WALL_COLOR = "black"
        IMAGE_DOOR_COLOR = "lightgray"

        image = Image.new("RGB", (self.width * IMAGE_CELL_SIZE, self.height * IMAGE_CELL_SIZE), IMAGE_BG_COLOR)
        draw = ImageDraw.Draw(image)
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                # Draw the cell contents (walls, traps, treasures, monsters)
                for direction, has_wall in cell.walls.items():
                    #is a wall if this cell has a wall in this direction OR the adjacent cell has a wall in the opposite direction
                    is_wall = has_wall
                    if not has_wall:
                        if direction == 'N' and y > 0:
                            is_wall = self.get_cell(x, y - 1).walls['S']
                        elif direction == 'S' and y < self.height - 1:
                            is_wall = self.get_cell(x, y + 1).walls['N']
                        elif direction == 'E' and x < self.width - 1:
                            is_wall = self.get_cell(x + 1, y).walls['W']
                        elif direction == 'W' and x > 0:
                            is_wall = self.get_cell(x - 1, y).walls['E']

                    #draw wall or door
                    if direction == 'N':
                        draw.line([(x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE), ((x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE)], fill=IMAGE_WALL_COLOR if is_wall else IMAGE_DOOR_COLOR, width=2)
                    elif direction == 'S':
                        draw.line([(x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE), ((x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE)], fill=IMAGE_WALL_COLOR if is_wall else IMAGE_DOOR_COLOR, width=2)
                    elif direction == 'E':
                        draw.line([((x + 1) * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE), ((x + 1) * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE)], fill=IMAGE_WALL_COLOR if is_wall else IMAGE_DOOR_COLOR, width=2)
                    elif direction == 'W':
                        draw.line([(x * IMAGE_CELL_SIZE, y * IMAGE_CELL_SIZE), (x * IMAGE_CELL_SIZE, (y + 1) * IMAGE_CELL_SIZE)], fill=IMAGE_WALL_COLOR if is_wall else IMAGE_DOOR_COLOR, width=2)

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