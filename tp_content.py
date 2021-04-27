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
        return hash( (self.name, self.weapon) )

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

def makePlayableUnits(app, makeAquaToo=True):
    ''' define all playable units at level 1 '''
    if makeAquaToo:
        makeAqua(app)
    giang = makeGiang(app)
    iara = makeIara(app)
    kai = makeKai(app)
    marina = makeMarina(app)
    morgan = makeMorgan(app)
    naia = makeNaia(app)
    walter = makeWalter(app)
    
    app.toPull = {giang, iara, kai, marina, morgan, naia, walter}

def makeAqua(app, name="Aqua", hp=15, attack=9, defense=5, res=4, level=1):
    ''' define an instance of PlayableChar (the player's own character) '''
    app.aqua = PlayableChar(name, "pool noodle", hp, attack, defense,
                                res, 95, app.aquaImg, level)
    return app.aqua

def makeGiang(app, hp=15, attack=7, defense=5, res=5, level=1):
    ''' return an instance of PlayableChar (Giang) '''
    return PlayableChar("Giang", "water gun", hp, attack, defense,
                                res, 85, app.giangImg, level)

def makeIara(app, hp=15, attack=8, defense=6, res=5, level=1):
    ''' return an instance of PlayableChar (Iara) '''
    return PlayableChar("Iara", "pool noodle", hp, attack, defense,
                                res, 90, app.iaraImg, level)

def makeKai(app, hp=15, attack=8, defense=6, res=6, level=1):
    ''' return an instance of PlayableChar (Kai) '''
    return PlayableChar("Kai", "water gun", hp, attack, defense,
                                res, 80, app.kaiImg, level)

def makeMarina(app, hp=15, attack=6, defense=4, res=6, level=1):
    ''' return an instance of PlayableChar (Marina) '''
    return PlayableChar("Marina", "bubble wand", hp, attack, defense,
                                res, 100, app.marinaImg, level)

def makeMorgan(app, hp=16, attack=7, defense=4, res=5, level=1):
    ''' return an instance of PlayableChar (Morgan) '''
    return PlayableChar("Morgan", "bubble wand", hp, attack, defense,
                                res, 95, app.morganImg, level)

def makeNaia(app, hp=16, attack=8, defense=5, res=5, level=1):
    ''' return an instance of PlayableChar (Naia) '''
    return PlayableChar("Naia", "water gun", hp, attack, defense,
                                res, 80, app.naiaImg, level)

def makeWalter(app, hp=17, attack=8, defense=5, res=4, level=1):
    ''' return an instance of PlayableChar (Walter) '''
    return PlayableChar("Walter", "pool noodle", hp, attack, defense,
                                res, 90, app.walterImg, level)

def loadPlayableUnits(app, saveData):
    ''' define playable units, barracks, and team members from save data '''
    app.barracks = []
    app.team = []
    addingToBarracks = addingToTeam = False
    currName = ""

    for line in saveData.splitlines():
        if line == "Barracks":
            addingToBarracks = True
        elif line == "Team":
            addingToBarracks = False
            addingToTeam = True
        elif addingToBarracks:
            # extract obtained character information
            if line.endswith(":"):
                currName = line[-1]
            elif line[0].isdigit():
                character = makeCharacter(app, currName, line)
                app.barracks.append(character)
        elif addingToTeam:
            # extract team members
            for unit in app.barracks:
                if unit.name == line:
                    app.team.append(unit)

    if len(app.barracks) == 8:
        app.foundAllUnits = True
    else:
        app.foundAllUnits = False
        makeRemainingUnits(app)

def makeCharacter(app, character, stats):
    ''' call a function to create the specified character with given stats '''
    stats = stats.split(", ")
    hp = stats[0]
    attack = stats[1]
    defense = stats[2]
    res = stats[3]
    level = stats[4]

    if character == "Giang":
        return makeGiang(app, hp, attack, defense, res, level)
    elif character == "Iara":
        return makeIara(app, hp, attack, defense, res, level)
    elif character == "Kai":
        return makeKai(app, hp, attack, defense, res, level)
    elif character == "Marina":
        return makeMarina(app, hp, attack, defense, res, level)
    elif character == "Morgan":
        return makeMorgan(app, hp, attack, defense, res, level)
    elif character == "Naia":
        return makeNaia(app, hp, attack, defense, res, level)
    elif character == "Walter":
        return makeWalter(app, hp, attack, defense, res, level)
    else: # character == player's character
        return makeAqua(app, hp, attack, defense, res, level)

def makeRemainingUnits(app):
    ''' define unobtained playable units at level 1 '''
    # make app.toPull a set of all characters other than Aqua at level 1
    makePlayableUnits(app, False)

    # remove all "duplicate" characters from toPull
    for character in app.toPull:
        for unit in app.barracks:
            if character.name == unit.name:
                app.toPull.remove(character)

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