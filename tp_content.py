####
# Name: Isabella Yee
# andrewID: iby
####

import random

####
# Characters
####

class Unit(object):
    ''' class for all units '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                    image):
        self.name = name
        self.weapon = weapon
        self.image = image
        
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
    
    def __repr__(self):
        ''' return a value when self is printed '''
        return self.name

    def __hash__(self):
        ''' return a hash value for self '''
        return hash(self.name)

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
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                    image):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                        image)

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
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                    image):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                        image)

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
        # magical units attack the player unit with lowest res
        else:
            lowestRes = 1000
            target = None
            for unit in playerTeam:
                if unit.res < lowestRes:
                    target = unit
                    lowestRest = unit.res
        return target

def loadPlayableUnits(app):
    ''' define all playable units '''
    blankImage = "that's not right"
    # balance stats, replace images later
    app.aqua = PlayableChar(app.playerName, "pool noodle", 15, 5, 5, 5, 95,
                            blankImage)
    app.giang = PlayableChar("Giang", "water gun", 15, 5, 5, 5, 95,
                            blankImage)
    app.iara = PlayableChar("Iara", "pool noodle", 15, 5, 5, 5, 95,
                            blankImage)
    app.kai = PlayableChar("Kai", "water gun", 15, 5, 5, 5, 95,
                            blankImage)
    app.marina = PlayableChar("Marina", "bubble wand", 15, 5, 5, 5, 95,
                            blankImage)
    app.morgan = PlayableChar("Morgan", "bubble wand", 15, 5, 5, 5, 95,
                            blankImage)
    app.naia = PlayableChar("Naia", "water gun", 15, 5, 5, 5, 95,
                            blankImage)
    app.walter = PlayableChar("Walter", "pool noodle", 15, 5, 5, 5, 95,
                            blankImage)

####
# Searching algorithm for enemies
####

"""
Pseudocode

destination = nearest cell such that target is in range
store nodes n: node n-1 in dictionary --> reconstruct path later in helper

heuristic h = (estimate) Manhattan/row,col distance to destination from node
// this doesn't account for terrain in the way
// use as a function param, so calculate beforehand

Need:
- list of visited nodes (represents a stack, so only pop off the end)
// = [startNode] at first
- empty dict() for path storage

"""