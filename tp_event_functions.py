####
# Name: Isabella Yee
# andrewID: iby
####

from cmu_112_graphics import *

####
# Main app
####

def appStarted(app):
    # import images and create characters
    loadImages(app)
    loadPlayableUnits(app)

    # define size constants
    app.margin = 5 # change later
    app.cellSize = 50
    app.mapOffset = 0 # change later

    # set up collections
    app.barracks = set()
    app.team = []
    app.items = set() # may remove
    app.droplets = app.seashells = 0
    app.moatSize = 25

    # define game colors and fonts
    app.borderColor = "blue"
    app.buttonColor = "blue"
    app.textColor = "black"
    app.buttonFont = "Arial 12 bold"
    app.dialogueFont = "Arial 14 bold"

    # define game mode
    app.freeplay = False
    app.mode = "mainScreenMode"

####
# Main screen
####

def mainScreenMode_mousePressed(app, event):
    pass

####
# Tutorial
####

def tutorialMode_mousePressed(app, event):
    name = app.getUserInput("name??") # change later - limit characters
    if name.isspace():
        app.playerName = "Aqua"
    else:
        app.playerName = name

####
# Transition screen
####

####
# Barracks screen
####

####
# Battle screen
####

def spawnTeam(team, mapType, unitType="playable"):
    ''' set positions for a team of units based on available spawn points '''
    # create a set of possible spawn points
    spawnPoints = set()
    rows, cols = len(mapType), len(mapType[0])
    if unitType == "playable":
        spawnSymbol = "A"
    else: # unitType == "enemy"
        spawnSymbol = "E"
    for row in range(rows):
        for col in range(cols):
            if mapType[row][col] == spawnSymbol:
                spawnPoints.add((row, col))
    
    # place each unit at a row,col position
    for unit in team:
        unit.row, unit.col = spawnPoints.pop()

def makeEnemyStats(team, weapon):
    ''' generate an enemy's stats based on the current team '''
    # use the lowest player stats
    worstHP = worstAttack = worstDefense = worstRes = 1000
    for unit in team:
        if unit.hp < worstHP: worstHP = unit.hp
        if unit.attack < worstAttack: worstAttack = unit.attack
        if unit.defense < worstDefense: worstDefense = unit.defense
        if unit.res < worstRes: worstRes = unit.res
    lowestDefended = min(worstDefense, worstRes)

    # balance stats based on enemy's weapon type
    if weapon == "pool noodle":
        hp = worstHP + 2
        attack = worstAttack + 1
        defense = lowestDefended
        res = lowestDefended - 1
        accuracy = 85
    elif weapon == "water gun":
        hp = worstHP
        attack = worstAttack
        defense = res = lowestDefended
        accuracy = 80
    else:
        hp = worstHP - 1
        attack = worstAttack - 1
        defense = lowestDefended - 1
        res = lowestDefended
        accuracy = 90
    return hp, attack, defense, res, accuracy

def inRange(unit, target):
    ''' return True if target is within range of unit '''
    drow = abs(unit.row - target.row)
    dcol = abs(unit.col - target.col)
    return drow + dcol == unit.range

def moveIsLegal(unit, drow, dcol):
    ''' check if a unit can legally move in direction drow,dcol '''
    newRow = unit.row + drow
    newCol = unit.col + dcol
    
    if newRow < 0 or newRow > 6: # fix magic numbers later
        return False
    elif newCol < 0 or newCol > 6:
        return False
    # insert check for terrain here
    else:
        return True

####
# Gacha screen
####