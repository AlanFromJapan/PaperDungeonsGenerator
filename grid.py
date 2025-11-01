from enum import Enum
import random

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
        monster_names = ["Goblin", "Troll", "Dragon", "Skeleton"]
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
        
