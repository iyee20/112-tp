####
# Name: Isabella Yee
# andrewID: iby
####

import random
from cmu_112_graphics import *
from tp_graphics import *

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
    app.cheats = False

def menuButtonClicked(app, event):
    ''' return the number (1, 2, or 3 top-down) of a menu button clicked '''
    event.x, event.y = xClick, yClick
    oneFifthHeight = app.height // 5

    # all 3-button menus are formatted the same
    if app.margin <= xClick <= app.width - app.margin:
        if oneFifthHeight <= yClick <= (oneFifthHeight*2) - app.margin:
            return 1
        elif oneFifthHeight * 2 <= yClick <= (oneFifthHeight*3) - app.margin:
            return 2
        elif oneFifthHeight * 3 <= yClick <= (oneFifthHeight*4) - app.margin:
            return 3
    return None

def backButtonClicked(app, event, topX, topY):
    ''' return True if a back arrow button is clicked '''
    if topX <= event.x <= topX + 10: # change later
        if topY <= event.y <= topY + 10:
            return True
    return False

####
# Main screen
####

def mainScreenMode_mousePressed(app, event):
    ''' handle mouse presses in main screen mode '''
    # only one game mode (story or freeplay) is available at a time 
    if not app.freeplay: # story button
        if menuButtonClicked(app, event) == 1:
            app.mode = "tutorialMode"
    else: # freeplay button
        if menuButtonClicked(app, event) == 2:
            app.mode = "battleMode"
    # settings button
    if menuButtonClicked(app, event) == 3:
        app.mode = "settingsMode"

####
# Settings
####

def settingsMode_mousePressed(app, event):
    ''' handle mouse presses in settings mode '''
    if menuButtonClicked(app, event) == 1: # change moat size
        pass # fix later
    elif menuButtonClicked(app, event) == 2: # toggle extras/cheats
        app.cheats = not app.cheats
    elif menuButtonClicked(app, event) == 3: # nothing...
        print("Why did you click this button?")
    elif backButtonClicked(app, event, app.margin, app.margin): # back to main
        app.mode = "mainScreenMode"

####
# Tutorial
####

def tutorialMode_mousePressed(app, event):
    ''' handle mouse presses in tutorial mode '''
    name = app.getUserInput("name??") # change later - limit characters
    if name.isspace():
        app.playerName = "Aqua"
    else:
        app.playerName = name

####
# Transition screen
####

def transitionMode_mousePressed(app, event):
    ''' handle mouse presses in transition mode '''
    if menuButtonClicked(app, event) == 1: # gacha button
        app.mode = "gachaMode"
    elif menuButtonClicked(app, event) == 2: # battle button
        app.mode = "battleMode"
    elif menuButtonClicked(app, event) == 3: # team button
        app.mode = "barracksMode"

####
# Barracks screen
####

def barracksMode_mousePressed(app, event):
    ''' handle mouse presses in barracks mode '''
    if backButtonClicked(app, event, app.margin, app.margin):
        app.mode = "transitionMode"

####
# Battle screen
####

def chooseMap(app):
    ''' set the current map for one battle '''
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
    app.map = random.choice(maps)

def spawnTeam(app, team, unitType="playable"):
    ''' set positions for a team of units based on available spawn points '''
    # create a set of possible spawn points
    spawnPoints = set()
    rows, cols = len(app.map), len(app.map[0])
    # spawn units on corresponding spawn points
    if unitType == "playable":
        spawnSymbol = "A"
    else: # unitType == "enemy"
        spawnSymbol = "E"
    for row in range(rows):
        for col in range(cols):
            if app.map[row][col] == spawnSymbol:
                spawnPoints.add((row, col))
    
    # place each unit at a randomly chosen row,col position from those available
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

def moveIsLegal(app, unit, drow, dcol):
    ''' check if a unit can legally move in direction drow,dcol '''
    newRow = unit.row + drow
    newCol = unit.col + dcol
    
    if newRow < 0 or newRow >= len(app.map):
        return False
    elif newCol < 0 or newCol >= len(app.map):
        return False
    # insert check for occupied cell here
    # insert check for terrain here
    else:
        return True

####
# Gacha screen
####

def gachaMode_mousePressed(app, event):
    ''' handle mouse presses in gacha mode '''
    if backButtonClicked(app, event, app.margin, 10): # change later
        app.mode = "transitionMode"