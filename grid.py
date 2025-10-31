from enum import Enum
import random

# Walliness factor for random grid generation (percentage of chance of having walls)
WALLINESS = 15
TRAPINESS = 50
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
        heroes_classes = random.sample(list(HeroesType), k=random.randint(0, 2))
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
        self.cells = [[Cell.generate_random_cell() for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        grid_repr = ""
        for row in self.cells:
            grid_repr += "||"
            for cell in row:
                grid_repr += repr(cell) + "|"
            grid_repr += "||\n"
        return grid_repr