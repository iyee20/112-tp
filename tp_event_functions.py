####
# Name: Isabella Yee
# andrewID: iby
####

import random, time
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
    app.margin = min(app.width, app.height) // 100
    app.cellSize = 50

    # set up collections
    app.barracks = [app.aqua]
    app.team = [app.aqua]
    app.foundAllUnits = False
    app.droplets = app.seashells = 3 # change to 0 later after testing
    app.moatSize = 25

    # set up battle variables
    app.enemyTeam = []
    app.selected = app.battleMessage = None
    app.battleMenuDisplay = 0
    app.playerTurn = True

    # define game colors and fonts
    app.buttonColor = "#699bf0"
    app.textColor = "black"
    app.buttonFont = "Arial 12 bold"
    app.dialogueFont = "Arial 14"

    # define game mode
    app.freeplay = app.cheats = False
    app.mode = "mainScreenMode"
    app.onCutsceneLine = 0
    app.tutorial = True

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
            app.mode = "tutorialMode"
    else: # freeplay button
        if menuButtonClicked(app, event) == 2:
            chooseMap(app)
            spawnTeam(app, app.team)
            makeEnemyTeam(app)
            spawnTeam(app, app.enemyTeam, unitType="enemy")
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
            app.showMessage("Developer cheats ON.")
        else:
            app.showMessage("Developer cheats OFF.")
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

def settingsMode_keyPressed(app, event):
    ''' handle key presses in settings mode (only used for cheats) '''
    if not app.cheats: return

    if event.key in ["c", "C"]:
        getAllCharacters(app)
    elif event.key in ["l", "L"]:
        tenLevelUpAll(app)

def getAllCharacters(app):
    ''' cheat all characters into the barracks '''
    while app.toPull != set():
        newUnit = app.toPull.pop()
        app.barracks.append(newUnit)
        if len(app.team) < 3:
            app.team.append(newUnit)
    
    app.showMessage("All the kids are here!")

def tenLevelUpAll(app):
    ''' cheat all characters in the barracks 10 levels higher '''
    for character in app.barracks:
        for level in range(10):
            character.levelUp()
    
    app.showMessage("The kids are more buff now!")

####
# Tutorial
####

def tutorialMode_mousePressed(app, event):
    ''' handle mouse presses in tutorial mode '''
    if app.aqua.name == "Aqua":
        name = app.getUserInput("Enter a name.") # limit characters later
        if name != None and not name.isspace():
            app.aqua.name = name.title()
            app.onCutsceneLine += 1

def tutorialMode_keyPressed(app, event):
    ''' handle key presses in tutorial mode '''
    if event.key == "Space":
        app.onCutsceneLine += 1
        allDialogue = openingDialogue(app)
        if app.onCutsceneLine >= len(allDialogue):
            app.onCutsceneLine = 0
            chooseMap(app)
            spawnTeam(app, app.team)
            makeEnemyTeam(app)
            spawnTeam(app, app.enemyTeam, unitType="enemy")
            app.mode = "battleMode"

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
        makeEnemyTeam(app)
        spawnTeam(app, app.enemyTeam, unitType="enemy")
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
        app.selected = None
        app.mode = "barracksMode"
    elif clicked != None:
        if clicked < len(app.barracks):
            if app.barracks[clicked] not in app.team:
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
# Gacha screen
####

def gachaMode_mousePressed(app, event):
    ''' handle mouse presses in gacha mode '''
    if backButtonClicked(app, event, app.margin, (app.height//5) + app.margin):
        app.mode = "transitionMode"
    elif gachaButtonClicked(app, event) == 1 and not app.foundAllUnits:
        # no more characters can be found if the collection is complete
        if app.seashells >= 1:
            gachaPull(app, 1)
        else:
            app.showMessage("Not enough Seashells!")
    elif gachaButtonClicked(app, event) == 3:
        # there must be at least 3 characters who can randomly be strengthened
        if len(app.barracks) < 3:
            app.showMessage("You haven't met enough people yet!")
        elif app.seashells >= 3:
            gachaPull(app, 3)
        else:
            app.showMessage("Not enough Seashells!")

def gachaButtonClicked(app, event):
    ''' return the pull number (1 or 3) of a gacha button clicked '''
    xClick, yClick = event.x, event.y
    oneEighthWidth = app.width // 8
    buttonWidth = int(2.5 * oneEighthWidth)
    oneFifthHeight = app.height // 5

    # pull buttons are at the same y, so compare x values
    if oneFifthHeight * 4 <= yClick <= oneFifthHeight * 9 // 2:
        if oneEighthWidth <= xClick <= oneEighthWidth + buttonWidth:
            return 1
        elif (oneEighthWidth*7) - buttonWidth <= xClick <= oneEighthWidth * 7:
            return 3
    return None

def gachaPull(app, pullNum):
    ''' get a new character or strengthen 3 characters '''
    app.seashells -= pullNum

    if pullNum == 1:
        # move new unit from toPull to barracks
        newUnit = app.toPull.pop()
        app.barracks.append(newUnit)
        if len(app.team) < 3:
            app.team.append(newUnit)
        app.mode = "cutsceneMode"
    else: # pullNum == 3
        mergeMessage = "Congratulations!"
        for i in range(pullNum):
            unit = random.choice(app.barracks)
            increasedStats = unit.merge() # do something with this dict later
            for stat in increasedStats:
                value = increasedStats[stat]
                mergeMessage += f"\n{unit.name}'s {stat} increased to {value}"
        app.showMessage(mergeMessage)

    if app.toPull == set():
        app.foundAllUnits = True
        app.showMessage(
                "Congratulations! You've met all the playable characters!")

####
# Cutscenes
####

def cutsceneMode_keyPressed(app, event):
    ''' handle key presses in cutscene mode '''
    if event.key == "Space":
        app.onCutsceneLine += 1

def cutsceneMode_mousePressed(app, event):
    ''' handle mouse presses in cutscene mode '''
    # return to gacha after reading at least part of cutscene
    if event.y >= int(app.height * 4/5) and app.onCutsceneLine > 1:
        app.onCutsceneLine = 0
        app.mode = "gachaMode"

####
# Battle screen
####

def battleMode_mousePressed(app, event):
    ''' handle mouse presses in battle mode '''
    if not app.playerTurn:
        enemyTurn(app)
        # free player units to move again
        for unit in app.team:
            unit.untapped = True
    else:
        playerTurn(app, event)
        # free enemy units to move again
        for enemy in app.enemyTeam:
            enemy.untapped = True

def enemyTurn(app):
    ''' play through an enemy turn '''
    for enemy in app.enemyTeam:
        # choose target and find path to target
        target = enemy.chooseTarget(app.team)
        enemy.movePath = aStarSearch(app, (enemy.row, enemy.col),
                            (target.row, target.col), heuristic)

        # attack if already in range
        if inRange(enemy, target):
            attackAndCounter(app, enemy, target)

        # move closer to target and attack if possible
        if len(enemy.movePath) != 0:
            enemy.row, enemy.col = enemy.movePath.pop(0)
            if inRange(enemy, target):
                attackAndCounter(app, enemy, target)
        
        enemy.tapped = False

    app.playerTurn = True

def playerTurn(app, event):
    ''' handle mouse presses in battle mode during the player's turn '''
    xClick, yClick = event.x, event.y
    clickedCell = mapCellClicked(app, xClick, yClick)

    # activate one of the player menu buttons or make a character selection
    if app.selected == None:
        if battleMenuButtonClicked(app, xClick, yClick): return
        for unitNum in range(len(app.team)):
            unit = app.team[unitNum]
            if clickedCell[0] == unit.row and clickedCell[1] == unit.col:
                if unit.untapped:
                    app.selected = unitNum

    # fix later - don't change selection ? end turn ??
    else:
        unit = app.team[app.selected]
        drow = clickedCell[0] - unit.row
        dcol = clickedCell[1] - unit.col
        # unit can move up to 2 spaces per turn
        if -2 <= drow <= 2 and -2 <= dcol <= 2 and abs(drow) + abs(dcol) <= 2:
            if moveIsLegal(app, unit.row, unit.col, drow, dcol):
                unit.row += drow
                unit.col += dcol
                app.selected = None
    
    # end turn after all units have moved
    if allUnitsTapped(app):
        app.playerTurn = False

def battleMenuButtonClicked(app, xClick, yClick):
    ''' if a battle menu button is clicked, perform the correct action '''
    fullHeight = (app.height//5) - (2*app.margin)
    buttonWidth = app.width // 6
    buttonHeight = fullHeight // 3

    # make these do things later
    if buttonWidth <= xClick <= 2 * buttonWidth:
        if app.margin <= yClick <= app.margin + buttonHeight: # flee battle
            return True
        elif (app.margin + (2*buttonHeight) <= yClick
                            <= app.margin + (3*buttonHeight)): # end turn
            return True
    elif 3 * buttonWidth <= xClick <= 5 * buttonWidth:
        if app.margin <= yClick <= app.margin + buttonHeight:
            # display untapped units
            return True
        elif (app.margin + (2*buttonHeight) <= yClick
                            <= app.margin + (3*buttonHeight)): # team summary
            return True
    return False # none of the buttons were clicked

def mapCellClicked(app, xClick, yClick):
    ''' return the row,col of a clicked cell on the map '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))

    col = (xClick - mapOffsetX) // app.cellSize
    row = (yClick - mapOffsetY) // app.cellSize
    return row, col

def allUnitsTapped(app):
    ''' return True if all team members have moved this turn '''
    for unit in app.team:
        if unit.untapped:
            return False
    return True

def battleMode_keyPressed(app, event):
    ''' handle key presses in battle mode '''
    # display player menu
    if event.key in ["m", "M"]:
        app.selected = None
    
    # add more later
    elif app.selected != None:
        unit = app.team[app.selected]

        # finish selected unit's move without attacking
        if event.key == "Enter":
            unit.untapped = False
        
        # attack an enemy or heal a team member in range
        elif event.key in ["Up", "Left", "Right", "Down"]:
            target = getTargetFromPosition(app, event.key)
            if isinstance(target, Enemy):
                attackAndCounter(app, unit, target, True)
            elif target != None:
                amount = unit.heal(target)
                if amount != False:
                    app.battleMessage = f'''{unit.name} healed {target.name}
for {amount} HP.'''
            unit.untapped = False
        
        app.selected = None

def inRange(unit, target):
    ''' return True if target is within range of unit '''
    drow = abs(unit.row - target.row)
    dcol = abs(unit.col - target.col)
    return drow + dcol == unit.range

def attackAndCounter(app, unit, target, unitIsPlayer=False):
    ''' play through a unit's attack and target's counterattack '''
    # unit attacks target
    amount = unit.attackTarget(target)
    if amount != False:
        app.battleMessage = f'''{unit.name} attacked {target.name}
for {amount} damage!'''
        if target.hp == 0:
            app.battleMessage += f"\n{target.name} was defeated!"
            if unitIsPlayer: # player unit defeats enemy unit
                getExperience(app, unit)
    else:
        app.battleMessage = f"{unit.name}'s attack missed!"

    # if possible, target counterattacks unit
    if inRange(target, unit) and target.hp != 0:
        counterAmount = target.attackTarget(unit)
        if counterAmount != False:
            app.battleMessage += f'''\n{target.name} counterattacked {unit.name}
for {counterAmount} damage!'''
            if unit.hp == 0:
                app.battleMessage += f"\n{unit.name} was defeated!"
                if not unitIsPlayer: # enemy unit is defeated by player unit
                    getExperience(app, target)
        else:
            app.battleMessage += f"\n{target.name}'s counterattack missed!"

def getExperience(app, unit):
    ''' grant experience to a player unit after defeating an enemy '''
    unit.toNextLevel -= 1
    if unit.toNextLevel <= 0:
        unit.levelUp()
        app.battleMessage += f"\n{unit.name} leveled up to level {unit.level}!"

def getTargetFromPosition(app, direction):
    ''' return the unit in-range of the current selected character '''
    unit = app.team[app.selected]

    if direction == "Up":
        drow, dcol = -1 * unit.range, 0
    elif direction == "Left":
        drow, dcol = 0, -1 * unit.range
    elif direction == "Right":
        drow, dcol = 0, unit.range
    else: # direction = "Down"
        drow, dcol = unit.range, 0
    targetRow = unit.row + drow
    targetCol = unit.col + dcol

    # target must be on the map
    if targetRow < 0 or targetRow > len(app.map): return None
    elif targetCol < 0 or targetCol > len(app.map[0]): return None

    # find enemy to attack
    for enemy in app.enemyTeam:
        if enemy.row == targetRow and enemy.col == targetCol: return enemy
    
    # find team member to heal
    if unit.weapon == "bubble wand":
        for teamMember in app.team:
            if teamMember.row == targetRow and teamMember.col == targetCol:
                return teamMember
    return None # no target in range

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

    if app.tutorial: # choose the sand castle map for the tutorial
        app.map = sandCastleMap
        return

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

def makeEnemyTeam(app):
    ''' generate enemies based on the current team size '''
    # 3 to 5 enemies should be made
    app.enemyTeam = []
    numEnemies = len(app.team) + 2

    # make 1 of each possible type of enemy
    enemy1 = makeEnemy(app, "Dehydration", "bubble wand", app.dehydrationImg)
    enemy2 = makeEnemy(app, "Heatstroke", "pool noodle", app.heatstrokeImg)
    enemy3 = makeEnemy(app, "Salt", "water gun", app.saltImg)

    if app.tutorial: # only make 1 enemy for the tutorial
        app.enemyTeam.append(enemy1)
        return
    
    app.enemyTeam.extend([enemy1, enemy2, enemy3])

    # make extra enemies
    if numEnemies > 3:
        enemy4 = makeEnemy(app, "Heatstroke", "pool noodle", app.heatstrokeImg)
        app.enemyTeam.append(enemy4)
        if numEnemies > 4:
            enemy5 = makeEnemy(app, "Salt", "water gun", app.saltImg)
            app.enemyTeam.append(enemy5)

def makeEnemy(app, name, weapon, image):
    ''' generate an enemy based on the current team '''
    # use the lowest player stats
    worstHP = worstAttack = worstDefense = worstRes = 1000
    for unit in app.team:
        if unit.hp < worstHP: worstHP = unit.hp
        if unit.attack < worstAttack: worstAttack = unit.attack
        if unit.defense < worstDefense: worstDefense = unit.defense
        if unit.res < worstRes: worstRes = unit.res
    lowestDefended = min(worstDefense, worstRes)

    # balance stats based on enemy's weapon type
    if weapon == "pool noodle":
        hp = int((worstHP+2) * (2/3))
        attack = int((worstAttack+1) * (2/3))
        defense = int(lowestDefended * (2/3))
        res = int((lowestDefended-1) * (2/3))
        accuracy = 85
    elif weapon == "water gun":
        hp = int(worstHP * (2/3))
        attack = int(worstAttack * (2/3))
        defense = res = int(lowestDefended * (2/3))
        accuracy = 80
    else:
        hp = int((worstHP-1) * (2/3))
        attack = int((worstAttack-1) * (2/3))
        defense = int((lowestDefended-1) * (2/3))
        res = int(lowestDefended * (2/3))
        accuracy = 90
    return Enemy(name, weapon, hp, attack, defense, res, accuracy, image)

####
# Searching algorithm for enemies
####

# pseudocode based on:
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

def makePathFromNodes(nodes, goal):
    ''' construct a path from a dictionary of nodes '''
    path = [(goal)]
    currNode = goal

    # start from the end, using keys to find previous nodes
    while currNode in nodes.keys():
        currNode = nodes[currNode]
        path = [currNode] + path
    # exclude current position and goal position
    return path[1:-1]

def heuristic(node, goal):
    ''' return the Manhattan distance from node to goal '''
    # difference of rows + difference of cols
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def lowestFCostNode(nodes, fCosts):
    ''' return the node with the lowest f(n) (cost to travel to it) '''
    lowestCost = 1000
    bestNode = None
    for node in nodes:
        if fCosts[node] < lowestCost:
            lowestCost = fCosts[node]
            bestNode = node
    return bestNode

def nodeNeighbors(app, node, goal):
    ''' return a set of all the neighbors of a row,col node '''
    currRow, currCol = node
    neighbors = set()

    # possible drow,dcol values for movement range = 2 cells
    twoCellMoves = [(2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (1, -1),
                        (-1, 1), (-1, -1)]
    oneCellMoves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # add valid neighbors (and goal, if possible) to set
    for i in range(len(twoCellMoves)):
        # add 2-cell neighbors
        drow, dcol = twoCellMoves[i]
        newRow = currRow + drow
        newCol = currCol + dcol
        if (newRow, newCol) == goal:
            neighbors.add((newRow, newCol))
        elif moveIsLegal(app, currRow, currCol, drow, dcol):
            neighbors.add((newRow, newCol))
        # add 1-cell neighbors
        if i < len(oneCellMoves):
            drow, dcol = oneCellMoves[i]
            newRow = currRow + drow
            newCol = currCol + dcol
            if moveIsLegal(app, currRow, currCol, drow, dcol):
                neighbors.add((newRow, newCol))
    return neighbors

def aStarSearch(app, startNode, goal, heuristic):
    ''' perform an A* informed search to find a path of nodes to goal '''
    visited = {startNode}
    path = dict()
    gCosts = {startNode: 0} # g(n) = cost to get to node n
    fCosts = {startNode: heuristic(startNode, goal)} # f(n) = g(n) + h(n)

    # visit all nodes to find the best path, using lowest-cost paths
    while visited != set():
        currNode = lowestFCostNode(visited, fCosts)
        if currNode == goal:
            return makePathFromNodes(path, goal)
        visited.remove(currNode) # travel past current node

        # travel to the neighbor node with the lowest f(n) so far
        for neighbor in nodeNeighbors(app, currNode, goal):
            gEstimate = gCosts[currNode] + heuristic(currNode, neighbor)
            # compare current estimate g(n) to previous estimate of g(n)
            gCostSoFar = gCosts.get(neighbor, 1000)
            if gEstimate < gCostSoFar:
               path[neighbor] = currNode
               gCosts[neighbor] = gEstimate
               fCosts[neighbor] = gEstimate + heuristic(neighbor, goal)
               if neighbor not in visited:
                   visited.add(neighbor)
    # failure: goal is never reached
    print("uh oh")

####
# Main
####

def main():
    runApp(width=600, height=700) # change later

if (__name__ == '__main__'):
    main()