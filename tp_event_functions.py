####
# Name: Isabella Yee
# andrewID: iby
####

import random
from cmu_112_graphics import *
from tp_graphics import *
from tp_content import *

####
# Main app
####

def appStarted(app):
    # import images and create playable characters
    loadImages(app)
    loadPlayableUnits(app)

    # define size constants
    app.margin = 5 # change later
    app.cellSize = 50
    app.mapOffset = 0 # change later

    # set up collections
    app.barracks = [app.aqua]
    app.team = [app.aqua]
    app.foundAllUnits = False
    app.selected = None
    app.droplets = app.seashells = 3 # change later after testing
    app.moatSize = 25

    # define game colors and fonts
    app.borderColor = "blue"
    app.buttonColor = "blue"
    app.textColor = "black"
    app.buttonFont = "Arial 12 bold"
    app.dialogueFont = "Arial 14"

    # define game mode
    app.freeplay = False
    app.mode = "mainScreenMode"
    app.cheats = False

def menuButtonClicked(app, event):
    ''' return the number (1, 2, or 3 top-down) of a menu button clicked '''
    xClick, yClick = event.x, event.y
    oneFifthHeight = app.height // 5

    # all 3-button menus are formatted the same, so compare y values
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
    if topX <= event.x <= topX + (app.height // 10):
        if topY <= event.y <= topY + (app.height // 10):
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
            #app.mode = "tutorialMode"
            app.mode = "transitionMode" # change later after testing
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
        changeMoatSize(app)
        app.showMessage(f"Moat size is now {app.moatSize} Droplets.")
    elif menuButtonClicked(app, event) == 2: # toggle extras/cheats
        app.cheats = not app.cheats
        if app.cheats:
            app.showMessage("Developer extras ON.")
        else:
            app.showMessage("Developer extras OFF.")
    elif menuButtonClicked(app, event) == 3: # nothing... (for now)
        app.showMessage("Why did you click this button?")
    elif backButtonClicked(app, event, app.margin, app.margin): # back to main
        app.mode = "mainScreenMode"

def changeMoatSize(app):
    ''' change the moat size to change story mode length '''
    sizes = [25, 50]
    for size in sizes:
        # increase moat size by 1 step if moat size is not max
        if app.moatSize < size:
            app.moatSize = size
            return
    # decrease moat size to minimum if moat size is max
    app.moatSize = 10

####
# Tutorial
####

def tutorialMode_mousePressed(app, event):
    ''' handle mouse presses in tutorial mode '''
    name = app.getUserInput("Enter a name.")
    if name != None and not name.isspace():
        app.aqua.name = name

####
# Transition screen
####

def transitionMode_mousePressed(app, event):
    ''' handle mouse presses in transition mode '''
    if menuButtonClicked(app, event) == 1: # gacha button
        app.mode = "gachaMode"
    elif menuButtonClicked(app, event) == 2: # battle button
        chooseMap(app)
        spawnTeam(app, app.team)
        app.mode = "battleMode"
    elif menuButtonClicked(app, event) == 3: # team button
        app.mode = "barracksMode"

####
# Barracks screen and team selection screen
####

def barracksMode_mousePressed(app, event):
    ''' handle mouse presses in barracks mode '''
    clicked = unitStatusClicked(app, event)

    if backButtonClicked(app, event, app.margin, app.margin):
        app.mode = "transitionMode"
    elif clicked != None:
        app.selected = clicked

def unitStatusClicked(app, event):
    ''' return the slot number (1, 2, or 3) of a unit status clicked '''
    yClick = event.y
    oneFifthHeight = app.height // 5

    if oneFifthHeight <= yClick <= oneFifthHeight * 2:
        return 1
    elif oneFifthHeight * 2 <= yClick <= oneFifthHeight * 3:
        return 2
    elif oneFifthHeight * 3 <= yClick <= oneFifthHeight * 4:
        return 3
    return None

def barracksMode_keyPressed(app, event):
    ''' handle key presses in barracks mode '''
    if app.selected != None:
        if event.key in ["Up", "Right"]:
            reorderTeam(app, True)
        elif event.key in ["Down", "Left"]:
            reorderTeam(app, False)
        elif event.key == "Enter":
            app.mode = "teamSelectionMode"

def reorderTeam(app, moveUp):
    ''' change the order of the current team '''
    # index of currently selected unit
    curr = app.selected - 1

    if moveUp:
        toSwap = curr - 1
    else: # move down
        toSwap = curr + 1
    
    # toSwap must be a valid index
    if 0 <= toSwap < len(app.team):
        app.team[curr], app.team[toSwap] = app.team[toSwap], app.team[curr]
    
    app.selected = None

def teamSelectionMode_mousePressed(app, event):
    ''' handle mouse presses in team selection mode '''
    clicked = unitIconClicked(app, event)

    if backButtonClicked(app, event, app.margin, app.margin):
        app.mode = "barracksMode"
    elif clicked != None:
        if clicked < len(app.barracks):
            app.team[app.selected - 1] = app.barracks[clicked]
            app.selected = None
            app.mode = "barracksMode"

def unitIconClicked(app, event):
    ''' return the index in app.barracks of a unit icon clicked '''
    xClick, yClick = event.x, event.y

    gridOffsetX = (app.width - (7*app.cellSize)) // 2
    gridOffsetY = (app.height - (3*app.cellSize)) // 2

    col = (xClick - gridOffsetX) // 50
    row = (yClick - gridOffsetY) // 50
    numCols = 7
    numRows = 3
   
    if 0 <= col < numCols and 0 <= row < numRows:
        if col % 2 == 0 and row % 2 == 0:
            return (col//2) + (2*row)
    return None

####
# Battle screen
####

def chooseMap(app):
    ''' set the current map for one battle '''
    # _ = sand, O = dune, X = water/moat, * = sand castle
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
    
    # check that newRow,newCol is on map
    if newRow < 0 or newRow >= len(app.map):
        return False
    elif newCol < 0 or newCol >= len(app.map):
        return False

    # check if cell is occupied later

    # water and moats cannot be walked onto
    elif app.map[newRow][newCol] == "X":
        return False

    else:
        return True

####
# Gacha screen
####

def gachaMode_mousePressed(app, event):
    ''' handle mouse presses in gacha mode '''
    if backButtonClicked(app, event, app.margin, (app.height//5) + app.margin):
        app.mode = "transitionMode"
    elif app.foundAllUnits:
        # no more characters can be found if the collection is complete
        return
    elif gachaButtonClicked(app, event) == 1:
        if app.seashells >= 1:
            gachaPull(app, 1)
        else:
            app.showMessage("Not enough Seashells!") # may replace later
    elif gachaButtonClicked(app, event) == 3:
        if app.seashells >= 3:
            gachaPull(app, 3)
        else:
            app.showMessage("Not enough Seashells!")

def gachaButtonClicked(app, event):
    ''' return the pull number (1 or 3) of a gacha button clicked '''
    xClick, yClick = event.x, event.y
    oneFifthWidth = app.width // 5
    oneFifthHeight = app.height // 5

    # pull buttons are at the same y, so compare x values
    if oneFifthHeight * 4 <= yClick <= oneFifthHeight * 9 // 2:
        if oneFifthWidth <= xClick <= oneFifthWidth * 2:
            return 1
        elif oneFifthWidth * 3 <= xClick <= oneFifthWidth * 4:
            return 3
    return None

def gachaPull(app, pullNum):
    ''' add pullNum characters to the barracks '''
    if pullNum == 1:
        newUnit = app.toPull.pop()
        app.barracks.append(newUnit)
        if len(app.team) < 3:
            app.team.append(newUnit)
        # change later - play dialogue
    else: # pullNum == 3
        pass

    if app.toPull == set():
        app.foundAllUnits = True
        app.showMessage(
                "Congratulations! You've met all the playable characters!")
    
    app.seashells -= pullNum

####
# Main
####

def main():
    runApp(width=500, height=500) # change later

if (__name__ == '__main__'):
    main()