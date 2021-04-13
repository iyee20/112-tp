####
# Name: Isabella Yee
# andrewID: iby
####

import random

####
# Classes (characters)
####

class Unit(object):
    ''' class for all units '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy):
        self.name = name
        self.weapon = weapon
        
        # set weapon characteristics
        if self.weapon == "bubble wand":
            self.type = "magical"
        else:
            self.type = "physical"
        if self.weapon == "pool noodle":
            self.range = 1
        else:
            self.range = 2

        # set stats
        self.maxHP = self.hp = maxHP
        self.attack = attack
        self.defense, self.res = defense, res
        self.accuracy = accuracy
        self.defeated = False

    def attack(self, target):
        ''' attack a target unit '''
        # accuracy check
        hitChance = random.randint(0, 100)
        if self.accuracy >= hitChance:
            # physical units target defense, magical units target res
            if self.type == "physical":
                defended = self.defense
            else:
                defended = self.res
            target.hp -= self.attack - defended
            if target.hp < 0:
                target.hp = 0
                target.defeated = True
            return True # attack succeeded
        else:
            return False # attack failed
    
    def heal(self, target, amount=self.attack // 2):
        ''' heal a target unit '''
        # default: bubble wand user healing another unit
        target.hp += amount
        if target.hp > target.maxHP:
            target.hp = target.maxHP
    
    def resetHP(self):
        ''' reset a unit's HP to max '''
        self.hp = self.maxHP
        self.defeated = False

class PlayableChar(Unit):
    ''' class for playable characters (inherits from Unit class) '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy)

        # set stats unique to playable characters
        self.level = 1
        self.toNextLevel = 3 # number of enemies to defeat to advance
        self.equipped = "" # equipped item (start with none)
    
    def levelUp(self):
        ''' increase stats based on increasing unit level '''
        # leveling up requires more enemies defeated per level
        self.level += 1
        self.toNextLevel = self.level * 3

        # stat boosts
        self.maxHP += 2
        stats = [self.maxHP, self.attack, self.defense, self.res]
        toIncrease = [True, True, True, False]
        random.shuffle(toIncrease)
        # randomly increase 3 stats
        for i in range(len(stats)):
            if toIncrease[i]:
                stats[i] += 1

class Enemy(Unit):
    ''' class for enemies (inherits from Unit class) '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy)

        # set stats unique to enemies
        self.droplets = random.randint(0, 5) # number of Droplets carried
        self.seashellDropRate = random.randint(0, 100)
    
    def chooseTarget(self, playerTeam):
        ''' choose a player unit to target '''
        # physical units attack the player unit with lowest defense
        if self.type == "physical":
            lowestDefense = 1000
            target = None
            for unit in playerTeam:
                if unit.defense < lowestDefense:
                    target = unit
                    lowestDefense = unit.defense
        # magicaly units attack the player unit with lowest res
        else:
            lowestRes = 1000
            target = None
            for unit in playerTeam:
                if unit.res < lowestRes:
                    target = unit
                    lowestRest = unit.res
        return target

####
# Maps
####

# _ = sand, O = dune, X = water, * = sand castle
# A = player unit spawn point, E = enemy unit spawn point

sandCastleMap = [
    ["_", "_", "_", "_", "_", "O", "O"],
    ["_", "_", "_", "_", "_", "E", "O"],
    ["_", "A", "_", "_", "_", "_", "E"],
    ["_", "_", "A", "_", "_", "E", "_"],
    ["_", "A", "_", "_", "_", "_", "E"],
    ["_", "_", "X", "X", "X", "E", "_"],
    ["_", "_", "X", "*", "X", "_", "_"],
]

dunesMap = [
    ["O", "_", "_", "_", "_", "E", "_"],
    ["_", "A", "_", "_", "_", "_", "O"],
    ["_", "A", "O", "O", "_", "E", "O"],
    ["_", "A", "_", "O", "_", "_", "E"],
    ["_", "_", "_", "_", "_", "_", "_"],
    ["O", "_", "_", "O", "_", "E", "_"],
    ["O", "O", "_", "O", "E", "_", "_"],
]

beachMap = [
    ["X", "X", "X", "X", "X", "X", "X"],
    ["_", "_", "_", "_", "_", "_", "E"],
    ["A", "_", "_", "_", "O", "_", "E"],
    ["_", "A", "_", "_", "_", "E", "_"],
    ["A", "_", "O", "_", "_", "_", "E"],
    ["_", "_", "O", "_", "_", "_", "E"],
    ["_", "_", "_", "_", "_", "O", "O"],
]

tidalMap = [
    ["X", "_", "E", "E", "_", "X", "X"],
    ["_", "_", "_", "_", "E", "_", "O"],
    ["_", "O", "O", "_", "_", "_", "_"],
    ["_", "_", "X", "X", "_", "E", "_"],
    ["_", "_", "X", "O", "E", "_", "_"],
    ["_", "A", "_", "O", "_", "_", "X"],
    ["_", "A", "A", "_", "_", "O", "X"],
]

islandMap = [
    ["X", "X", "X", "X", "X", "X", "X"],
    ["X", "_", "_", "_", "E", "_", "X"],
    ["X", "A", "_", "_", "_", "E", "X"],
    ["X", "A", "_", "O", "E", "_", "X"],
    ["X", "A", "_", "_", "_", "E", "X"],
    ["X", "_", "_", "_", "E", "_", "X"],
    ["X", "X", "X", "X", "X", "X", "X"],
]

maps = [sandCastleMap, dunesMap, beachMap, tidalMap, islandMap]

####
# Searching algorithm for enemies
####