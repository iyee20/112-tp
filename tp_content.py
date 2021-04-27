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
        self.untapped = True # whether unit can attack this turn
        self.canMove = True # whether unit can move this turn
    
    def __repr__(self):
        ''' return a value when self is printed '''
        return self.name

    def __hash__(self):
        ''' return a hash value for self '''
        return hash(self.name)

    def attackTarget(self, target):
        ''' attack a target unit '''
        # accuracy check
        hitChance = random.randint(0, 100)
        if self.accuracy >= hitChance:
            # physical units target defense, magical units target res
            if self.type == "physical":
                defended = self.defense
            else:
                defended = self.res
            # unit can't do negative damage
            amountLost = max(0, self.attack - defended)
            target.hp -= amountLost
            if target.hp < 0:
                target.hp = 0
                target.defeated = True
            return amountLost # attack succeeded
        else:
            return False # attack failed
    
    def heal(self, target):
        ''' heal a target unit '''
        # only bubble wand users can heal, only damaged units can be healed
        if self.weapon != "bubble wand" or target.hp == target.maxHP:
            return False

        # target can only be healed up to max HP
        amount = min(self.attack // 2, target.maxHP - target.hp)
        target.hp += amount
        return amount
    
    def resetHP(self):
        ''' reset a unit's HP to max '''
        self.hp = self.maxHP
        self.defeated = False

class PlayableChar(Unit):
    ''' class for playable characters (inherits from Unit class) '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                    image, level=1):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                        image)

        # set stats unique to playable characters
        self.level = level
        self.toNextLevel = 3 # number of enemies to defeat to advance
    
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
        
        self.maxHP = stats[0]
        self.attack = stats[1]
        self.defense, self.res = stats[2], stats[3]
        self.resetHP()
    
    def merge(self):
        ''' increase stats after merging with a duplicate of unit '''
        increasedStats = dict()
        statNames = ["Max HP", "Attack", "Defense", "Resistance"]

        stats = [self.maxHP, self.attack, self.defense, self.res]
        toIncrease = [True, True, False, False]
        random.shuffle(toIncrease)

        # randomly increase 2 stats
        for i in range(len(stats)):
            if toIncrease[i]:
                stats[i] += 1
                increasedStats[statNames[i]] = stats[i]

        self.maxHP = stats[0]
        self.attack = stats[1]
        self.defense, self.res = stats[2], stats[3]
        self.resetHP()
        return increasedStats

def makePlayableUnits(app):
    ''' define all playable units '''
    app.aqua = PlayableChar("Aqua", "pool noodle", 15, 9, 5, 4, 95, app.aquaImg)
    giang = PlayableChar("Giang", "water gun", 15, 7, 5, 5, 85, app.giangImg)
    iara = PlayableChar("Iara", "pool noodle", 15, 8, 6, 5, 90, app.iaraImg)
    kai = PlayableChar("Kai", "water gun", 15, 8, 6, 6, 80, app.kaiImg)
    marina = PlayableChar("Marina", "bubble wand", 15, 6, 4, 6, 100,
                            app.marinaImg)
    morgan = PlayableChar("Morgan", "bubble wand", 16, 7, 4, 5, 95,
                            app.morganImg)
    naia = PlayableChar("Naia", "water gun", 16, 8, 5, 5, 80, app.naiaImg)
    walter = PlayableChar("Walter", "pool noodle", 17, 8, 5, 4, 90,
                            app.walterImg)
    
    app.toPull = {giang, iara, kai, marina, morgan, naia, walter}

class Enemy(Unit):
    ''' class for enemies (inherits from Unit class) '''
    def __init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                    image):
        Unit.__init__(self, name, weapon, maxHP, attack, defense, res, accuracy,
                        image)

        # set stats unique to enemies
        self.droplets = random.randint(1, 5) # number of Droplets carried
        self.seashellDropRate = random.randint(0, 100)
        self.movePath = []
    
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