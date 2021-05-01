####
# Name: Isabella Yee
# andrewID: iby
####

import random
from cmu_112_graphics import *
from tp_graphics import *
from tp_content import *
from os import remove as deleteFile

####
# Main app
####

def appStarted(app):
    # graphics
    setColorsAndFonts(app)
    loadImages(app)

    # define size constants
    app.margin = min(app.width, app.height) // 100
    app.cellSize = 50

    resetBattleVars(app)

    app.mode = "mainScreenMode"
    app.saveFilePath = None
    newSave(app)

def setColorsAndFonts(app):
    ''' define game colors and fonts '''
    app.buttonColor = "#60C1FF"
    app.buttonFont = "Arial 12 bold"
    app.dialogueFont = "Arial 14"
    app.summaryFont = "Arial 11"

####
# Functions used in multiple screens
####

def resetBattleVars(app):
    ''' reset battle-related variables '''
    app.enemyTeam = []
    app.selected = app.battleMessage = None
    app.battleMenuDisplay = 0
    app.playerTurn = True
    app.victory = app.defeat = False
    app.endOfBattleMessage = ""
    app.onCutsceneLine = 0

def menuButtonClicked(app, event):
    ''' return the number (1, 2, or 3 top-down) of a menu button clicked '''
    xClick, yClick = event.x, event.y
    oneFifthHeight = app.height // 5
    buttonHeight = oneFifthHeight - app.margin

    # all 3-button menus are formatted the same, so compare y values
    if app.margin <= xClick <= app.width - app.margin:
        if oneFifthHeight <= yClick <= oneFifthHeight + buttonHeight:
            return 1
        elif oneFifthHeight * 2 <= yClick <= (oneFifthHeight*2) + buttonHeight:
            return 2
        elif oneFifthHeight * 3 <= yClick <= (oneFifthHeight*3) + buttonHeight:
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
    # save file choice button
    if menuButtonClicked(app, event) == 1:
        app.mode = "saveMode"

    # play button
    elif app.saveFilePath != None and menuButtonClicked(app, event) == 2:
        # only one game mode (story or freeplay) is available at a time 
        if app.freeplay:
            saveGame(app)
            app.storyModeEnd = False
            app.battleMenuDisplay = 3
            chooseMap(app)
            spawnTeam(app, app.team)
            makeEnemyTeam(app)
            spawnTeam(app, app.enemyTeam, unitType="enemy")
            app.mode = "battleMode"
        elif app.tutorial:
            app.mode = "tutorialMode"
        else:
            app.mode = "transitionMode"
    
    # settings button
    elif menuButtonClicked(app, event) == 3:
        app.mode = "settingsMode"

####
# Save/load file (and save screen) functions
####

def saveMode_mousePressed(app, event):
    ''' handle mouse presses in save mode '''
    # go back to main screen
    if backButtonClicked(app, event, app.margin, app.margin):
        app.mode = "mainScreenMode"
    
    # choose a save file to use
    elif saveFileChosen(app, event) == 1:
        app.saveFilePath = "saves/save1.txt"
        if saveIsBlank(app.saveFilePath):
            newSave(app)
        else:
            loadSave(app)
    elif saveFileChosen(app, event) == 2:
        app.saveFilePath = "saves/save2.txt"
        if saveIsBlank(app.saveFilePath):
            newSave(app)
        else:
            loadSave(app)

def saveIsBlank(path):
    ''' return True if a .txt file is empty '''
    if readFile(path) == "":
        return True
    return False

# from:
# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    ''' return the contents of a .txt file '''
    with open(path, "rt") as f:
        return f.read()

def saveFileChosen(app, event):
    ''' return the file number (1 or 2) of a chosen save file '''
    xClick, yClick = event.x, event.y

    if app.height // 3 <= yClick <= app.height // 3 * 2:
        if app.margin <= xClick <= (app.width - app.margin) // 2:
            return 1
        elif (app.width + app.margin) // 2 <= xClick <= app.width - app.margin:
            return 2
    return None

def newSave(app):
    ''' define characters and other variables for a new save file '''
    makePlayableUnits(app)

    # set up collections
    app.barracks = [app.aqua]
    app.team = [app.aqua]
    app.foundAllUnits = False
    app.droplets = app.seashells = 0
    app.moatSize = 25

    # define game mode
    app.freeplay = app.cheats = app.storyModeEnd = False
    app.tutorial = True

def loadSave(app):
    ''' define characters and other variables from a previous save file '''
    saveData = readFile(app.saveFilePath)

    loadPlayableUnits(app, saveData)

    loadProgress(app, saveData)

    # saving is unlocked after tutorial, cheats are toggled after every load
    app.cheats = app.storyModeEnd = app.tutorial = False

def loadProgress(app, saveData):
    ''' load saved progress and Seashells '''
    for line in saveData.splitlines():
        try:
            firstWord = line.split(" ")[0]
            secondWord = line.split(" ")[1]
        except:
            continue
        if firstWord == "Freeplay":
            if secondWord == "True":
                app.freeplay = True
            else:
                app.freeplay = False
        elif firstWord == "MoatSize":
            app.moatSize = int(secondWord)
        elif firstWord == "Droplets":
            app.droplets = int(secondWord)
        elif firstWord == "Seashells":
            app.seashells = int(secondWord)

def saveGame(app):
    ''' save a player's game data to the chosen save file '''
    # confirm that user wants to overwrite a previous save file
    if not saveIsBlank(app.saveFilePath):
        if not overwriteSaveOkay(app):
            return

    # delete old file and write a new one
    deleteFile(app.saveFilePath)
    saveContents = writeSaveContents(app)
    writeFile(app.saveFilePath, saveContents)

    app.showMessage("The game was saved.")

def overwriteSaveOkay(app):
    ''' return False if a user cancels saving over a previous file '''
    confirmation = app.getUserInput('''Saving will overwrite the previous save.
Type or click Cancel to cancel the save.''')
    if confirmation == None or confirmation.upper() == "CANCEL":
        app.showMessage("The game was not saved.")
        return False
    return True

def writeSaveContents(app):
    ''' return the contents of a new save file '''
    # player name
    contents = f"{app.aqua.name}"

    # collected characters
    contents += "\nBarracks"
    for unit in app.barracks:
        contents += f'''
{unit.name}:
{unit.maxHP}, {unit.attack}, {unit.defense}, {unit.res}, {unit.level}'''

    # current team
    contents += "\nTeam"
    for unit in app.team:
        contents += f"\n{unit.name}"

    # game progress status
    contents += "\nGame Status"
    contents += f'''
Freeplay {app.freeplay}
MoatSize {app.moatSize}
Droplets {app.droplets}
Seashells {app.seashells}'''

    return contents

# from:
# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def writeFile(path, contents):
    ''' add to the contents of a .txt file '''
    with open(path, "wt") as f:
        f.write(contents)

def saveMode_keyPressed(app, event):
    ''' handle key presses in save mode '''
    if app.saveFilePath != None:
        if event.key in ["Backspace", "Delete"]:
            if deleteSaveOkay(app):
                deleteFile(app.saveFilePath)
                writeFile(app.saveFilePath, "")
                app.saveFilePath = None

def deleteSaveOkay(app):
    ''' return False if a user cancels deleting a previous save file '''
    if saveIsBlank(app.saveFilePath):
        app.showMessage("This file is already empty!")
    else:
        confirmation = app.getUserInput('''The old save will be lost forever.
Type or click OK to continue deleting.''')
        if confirmation != None:
            if confirmation == "" or confirmation.upper() == "OK":
                app.showMessage("Save deleted.")
                return True
    return False

####
# Settings
####

def settingsMode_mousePressed(app, event):
    ''' handle mouse presses in settings mode '''
    # change moat size
    if menuButtonClicked(app, event) == 1:
        if app.saveFilePath == None:
            app.showMessage("Please choose a save file first!")
            return
        changeMoatSize(app)
        app.showMessage(f"Moat size is now {app.moatSize} Droplets.")

    # toggle cheats
    elif menuButtonClicked(app, event) == 2:
        app.cheats = not app.cheats
        if app.cheats: app.showMessage("Developer cheats ON.")
        else: app.showMessage("Developer cheats OFF.")

    # toggle game mode (story or freeplay)
    elif menuButtonClicked(app, event) == 3:
        if app.saveFilePath == None:
            app.showMessage("Please load a non-empty save file first!")
            return
        app.freeplay = not app.freeplay
        if app.freeplay:
            app.battleMenuDisplay = 3
            app.tutorial = False
            app.showMessage("Story mode skipped.")
        else:
            app.battleMenuDisplay = 0
            app.tutorial = True
            app.showMessage("Now in story mode.")

    # go back to main screen
    elif backButtonClicked(app, event, app.margin, app.margin):
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

    if event.key in "Cc":
        getAllCharacters(app)
    elif event.key in "Ll":
        tenLevelUpAll(app)
    elif event.key in "Ss": # switch to sample save file
        app.saveFilePath = "saves/sample_save.txt"
        loadSave(app)
        app.showMessage(f'''Switched to sample save file.
Remember to toggle cheats back on.''')

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
    # name can only be entered during the first scene
    if app.aqua.name == "Aqua" and app.onCutsceneLine == 0:
        name = app.getUserInput("Enter a name with 6 characters or less.")
        if name != None and name.isalpha() and len(name) <= 6:
            name = name.title()
            if nameInUse(name):
                app.showMessage('''Someone else has that name.
Please pick a different one. A nickname, maybe?''')
            else:
                app.aqua.name = name
                app.onCutsceneLine += 1

def nameInUse(name):
    ''' return True if a name is already used in the game '''
    names = {"Anna", "Nerissa", "Giang", "Iara", "Kai", "Marina", "Morgan",
                "Naia", "Walter", "Dehydration", "Heatstroke", "Salt"}
    return name in names

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
        if app.tutorial:
            app.onCutsceneLine = 0
        app.mode = "gachaMode"
    elif menuButtonClicked(app, event) == 2: # battle button
        if app.tutorial: return # button is unusable during tutorial
        chooseMap(app)
        spawnTeam(app, app.team)
        makeEnemyTeam(app)
        spawnTeam(app, app.enemyTeam, unitType="enemy")
        app.mode = "battleMode"
    elif menuButtonClicked(app, event) == 3: # team button
        # button is unlocked during tutorial
        if app.tutorial:
            if len(app.team) == 1: return
            else: app.onCutsceneLine = 0
        app.mode = "barracksMode"

def transitionMode_keyPressed(app, event):
    ''' handle key presses in transition mode '''
    # move through tutorial dialogue
    if app.tutorial and event.key == "Space":
        app.onCutsceneLine += 1

    # save the game
    elif event.key in "Ss":
        saveGame(app)

    # go back to main screen
    elif app.cheats and event.key in "Hh":
        app.mode = "mainScreenMode"

####
# Barracks screen and team selection screen
####

def barracksMode_mousePressed(app, event):
    ''' handle mouse presses in barracks mode '''
    clicked = unitStatusClicked(app, event)

    if backButtonClicked(app, event, app.margin, app.margin):
        if app.tutorial:
            app.tutorial = False
        app.selected = None
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
    if app.tutorial and event.key == "Space":
        app.onCutsceneLine += 1

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

    gridOffsetY = (app.height - (2*app.height//10)) // 2

    col = xClick // (app.width//4)
    row = (yClick - gridOffsetY) // (app.height//10)
    numCols = 4
    numRows = 2
   
    if 0 <= col < numCols and 0 <= row < numRows:
        return col + (row*4)
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
            increasedStats = unit.merge()
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
    # normal cutscenes can be partially skipped
    if not app.storyModeEnd:
        # return to gacha after reading at least part of cutscene
        if event.y >= int(app.height * 4/5) and app.onCutsceneLine > 1:
            app.onCutsceneLine = 0
            app.mode = "gachaMode"
    
    # ending cutscene can't be skipped
    else:
        cutSceneLines = 4
        if app.onCutsceneLine > cutSceneLines:
            app.onCutsceneLine = 0
            app.freeplay = True
            app.mode = "mainScreenMode"

####
# Battle screen
####

def battleMode_mousePressed(app, event):
    ''' handle mouse presses in battle mode '''
    # make sure that tutorial dialogue disappears after reading all of it
    if app.tutorial:
        app.onCutsceneLine += 1
        tutorialLines = 5
        if app.onCutsceneLine < tutorialLines: return

    if app.victory or app.defeat:
        # reset all battle-related variables before going back
        resetBattleVars(app)
        for unit in app.team:
            unit.resetHP()
            unit.untapped = unit.canMove = True
        if (app.droplets >= app.moatSize and
                not app.storyModeEnd and not app.freeplay):
            app.droplets = app.moatSize
            app.storyModeEnd = True
            app.mode = "cutsceneMode"
        else: app.mode = "transitionMode"
        return

    if not app.playerTurn:
        enemyTurn(app)
        # free player units to move again
        for unit in app.team:
            unit.untapped = unit.canMove = True
        app.selected = None
    else:
        playerTurn(app, event)
        # free enemy units to move again
        for enemy in app.enemyTeam:
            enemy.untapped = enemy.canMove = True

def enemyTurn(app):
    ''' play through an enemy turn '''
    for enemy in app.enemyTeam:
        if enemy.untapped and enemy.hp != 0:
            target = enemy.chooseTarget(app.team)

            # attack if already in range
            if inRange(enemy, target):
                attackAndCounter(app, enemy, target)
                enemy.canMove = False

            # find a path to target
            goalRow, goalCol = findCellInRange(app, enemy, target, heuristic)
            enemy.movePath = aStarSearch(app, (enemy.row, enemy.col),
                                            (goalRow, goalCol), heuristic)
            if enemy.range == 2: removeTooCloseCell(enemy, target, heuristic)

            # move closer to target and attack if possible
            if (enemy.movePath != None and enemy.canMove
                and len(enemy.movePath) != 0):
                enemy.row, enemy.col = enemy.movePath.pop(0)
                enemy.canMove = False
                if inRange(enemy, target): attackAndCounter(app, enemy, target)
        
            enemy.untapped = False
            break # separate each enemy's move with mouse presses

    # end turn after all enemies have moved
    if allUnitsTapped(app.enemyTeam): app.playerTurn = True

def findCellInRange(app, unit, target, heuristic):
    ''' return a row,col position such that target will be in range of unit '''
    # find all relative positions that unit could be at
    if unit.range == 1:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    else: # unit.range == 2
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0),
                        (1, 1), (-1, -1), (-1, 1), (1, -1)]
    
    # find cells that can be moved to
    legalCells = []
    for drow, dcol in directions:
        if moveIsLegal(app, target.row, target.col, drow, dcol, False):
            cell = (target.row + drow, target.col + dcol)
            legalCells.append(cell)
    
    # find closest cell to move to
    unitCell = (unit.row, unit.col)
    targetCell = (target.row, target.col)
    secondOptions = []
    for guess in legalCells:
        if cellIsBetweenCells(guess, unitCell, targetCell, heuristic):
            return guess
        elif heuristic(guess, targetCell) == unit.range:
            if heuristic(guess, unitCell) == 1:
                return guess
            else:
                secondOptions.append(guess)
    return findBestCell(unitCell, secondOptions, heuristic)

def cellIsBetweenCells(guess, currCell, goalCell, heuristic):
    ''' return True if a cell is between currCell and goalCell '''
    fullDistance = heuristic(currCell, goalCell)

    # distance from guess to currCell or goalCell should be less than total
    if heuristic(guess, currCell) < fullDistance:
        if heuristic(guess, goalCell) < fullDistance:
            return True
    return False

def findBestCell(currCell, options, heuristic):
    ''' return the cell in options that is the closest to currCell '''
    bestDist = heuristic(currCell, options[0])
    bestCell = options[0]

    for i in range(1, len(options)):
        cell = options[i]
        distance = heuristic(currCell, cell)
        if distance < bestDist:
            bestDist = distance
            bestCell = cell
    return bestCell

def removeTooCloseCell(unit, target, heuristic):
    ''' remove moves that would place a 2-cell ranged unit next to a target '''
    if unit.movePath == None:
        return

    newPath = []

    for cell in unit.movePath:
        if heuristic(cell, (target.row, target.col)) != 1:
            newPath.append(cell)
    unit.movePath = newPath

def playerTurn(app, event):
    ''' handle mouse presses in battle mode during the player's turn '''
    xClick, yClick = event.x, event.y
    clickedCell = mapCellClicked(app, xClick, yClick)

    # activate one of the player menu buttons or make a character selection
    if app.selected == None:
        if battleMenuButtonClicked(app, xClick, yClick): return
        app.battleMenuDisplay = 0
        selectUnit(app, clickedCell)

    else: # move selected unit
        app.battleMenuDisplay = 0
        unit = app.team[app.selected]
        if unit.canMove: movePlayableCharacter(app, unit, clickedCell)
    
    # end turn after all units have moved
    if allUnitsTapped(app.team):
        app.playerTurn = False

def selectUnit(app, clickedCell):
    ''' set app.selected to the appropriate unit number '''
    for unitNum in range(len(app.team)):
        unit = app.team[unitNum]
        if clickedCell[0] == unit.row and clickedCell[1] == unit.col:
            if unit.untapped:
                app.selected = unitNum

def movePlayableCharacter(app, unit, clickedCell):
    ''' move a playable character to a clicked cell if possible '''
    drow = clickedCell[0] - unit.row
    dcol = clickedCell[1] - unit.col

    # unit can move up to 2 spaces per turn
    if -2 <= drow <= 2 and -2 <= dcol <= 2 and abs(drow) + abs(dcol) <= 2:
        if moveIsLegal(app, unit.row, unit.col, drow, dcol):
            unit.row += drow
            unit.col += dcol
            unit.canMove = False

            # adjust battle message based on unit type
            attackKeys = "an arrow key"
            if unit.range == 2:
                attackKeys += " or WESD"
            instruction = "attack an enemy"
            if unit.weapon == "bubble wand":
                instruction += " or heal an ally"
            app.battleMessage = f'''Press {attackKeys} to {instruction}
or Enter to wait.'''

def allUnitsTapped(team):
    ''' return True if all living team members have moved this turn '''
    for unit in team:
        if unit.untapped and unit.hp != 0:
            return False
    return True

def battleMenuButtonClicked(app, xClick, yClick):
    ''' if a battle menu button is clicked, perform the correct action '''
    if app.tutorial: return # player menu is locked during tutorial

    fullHeight = (app.height//5) - (2*app.margin)
    buttonWidth = app.width // 6
    buttonHeight = fullHeight // 3

    if buttonWidth <= xClick <= 2 * buttonWidth:
        if app.margin <= yClick <= app.margin + buttonHeight: # flee battle
            app.defeat = True
            checkBattleEnd(app)
            return True
        elif (app.margin + (2*buttonHeight) <= yClick
                            <= app.margin + (3*buttonHeight)): # end turn
            app.playerTurn = False
            return True
    elif 3 * buttonWidth <= xClick <= 5 * buttonWidth:
        if app.margin <= yClick <= app.margin + buttonHeight:
            # display untapped units
            app.battleMenuDisplay = 1
            return True
        elif (app.margin + (2*buttonHeight) <= yClick
                            <= app.margin + (3*buttonHeight)): # HP summary
            app.battleMenuDisplay = 2
            return True
    return False # none of the buttons were clicked

def mapCellClicked(app, xClick, yClick):
    ''' return the row,col of a clicked cell on the map '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))

    col = (xClick - mapOffsetX) // app.cellSize
    row = (yClick - mapOffsetY) // app.cellSize
    return row, col

def battleMode_keyPressed(app, event):
    ''' handle key presses in battle mode '''
    if app.victory or app.defeat: return

    # move through tutorial dialogue
    if app.tutorial and event.key == "Space": app.onCutsceneLine += 1

    # display player menu
    if event.key in ["m", "M"]: app.selected = None
    
    elif app.selected != None:
        unit = app.team[app.selected]

        # finish selected unit's turn without attacking or moving
        if event.key == "Enter": unit.untapped = unit.canMove = False
        
        # attack an enemy or heal a team member in range
        elif event.key in ["Up", "Left", "Right", "Down",
                            "W", "w", "E", "e", "S", "s", "D", "d"]:
            target = getTargetFromPosition(app, event.key)
            if isinstance(target, Enemy):
                attackAndCounter(app, unit, target, True)
            elif target != None:
                amount = unit.heal(target)
                if amount != False:
                    app.battleMessage = f'''{unit.name} healed {target.name}
for {amount} HP.'''
            unit.untapped = unit.canMove = False
        
        app.selected = None

def getTargetFromPosition(app, key):
    ''' return the unit in-range of the current selected character '''
    unit = app.team[app.selected]

    drow, dcol = dRowAndColFromKey(app, key)
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

def dRowAndColFromKey(app, key):
    ''' return a drow,dcol move based on the entered key '''
    unit = app.team[app.selected]

    # cardinal directions
    if key == "Up":
        drow, dcol = -1 * unit.range, 0
    elif key == "Left":
        drow, dcol = 0, -1 * unit.range
    elif key == "Right":
        drow, dcol = 0, unit.range
    elif key == "Down":
        drow, dcol = unit.range, 0
    
    # diagonals
    elif key in "Ww":
        drow, dcol = -1, -1
    elif key in "Ee":
        drow, dcol = -1, 1
    elif key in "Ss":
        drow, dcol = 1, -1
    else: # key == D
        drow, dcol = 1, 1

    return drow, dcol

def attackAndCounter(app, unit, target, unitIsPlayer=False):
    ''' play through a unit's attack and target's counterattack '''
    # unit attacks target
    amount = unit.attackTarget(target)
    if isinstance(amount, int):
        app.battleMessage = f'''{unit.name} attacked {target.name}
for {amount} damage!'''
        if target.hp == 0:
            app.battleMessage += f"\n{target.name} was defeated!"
            target.row = target.col = -1
            if unitIsPlayer: # player unit defeats enemy unit
                getExperience(app, unit)
    else:
        app.battleMessage = f"{unit.name}'s attack missed!"

    # if possible, target counterattacks unit
    if inRange(target, unit) and target.hp != 0:
        counterAmount = target.attackTarget(unit)
        if isinstance(counterAmount, int):
            app.battleMessage += f'''\n{target.name} counterattacked {unit.name}
for {counterAmount} damage!'''
            if unit.hp == 0:
                app.battleMessage += f"\n{unit.name} was defeated!"
                unit.row = unit.col = -1
                if not unitIsPlayer: # enemy unit is defeated by player unit
                    getExperience(app, target)
        else:
            app.battleMessage += f"\n{target.name}'s counterattack missed!"
    
    checkBattleEnd(app)

def inRange(unit, target):
    ''' return True if target is within range of unit '''
    drow = abs(unit.row - target.row)
    dcol = abs(unit.col - target.col)
    return drow + dcol == unit.range

def getExperience(app, unit):
    ''' grant experience to a player unit after defeating an enemy '''
    unit.toNextLevel -= 1
    if unit.toNextLevel <= 0:
        unit.levelUp()
        app.battleMessage += f"\n{unit.name} leveled up to level {unit.level}!"

def checkBattleEnd(app):
    ''' check if a battle is over and set victory or defeat conditions '''
    if checkVictory(app) or app.victory:
        app.victory = True
        app.battleMessage = "You win!"

        victoryRewards(app)

    elif checkDefeat(app) or app.defeat:
        app.defeat = True
        app.battleMessage = "You lose!"

        # lose some Droplets
        if app.droplets > 0:
            dropletsLost = random.randint(1, (app.droplets//3) + 1)
            app.droplets -= dropletsLost
        else:
            dropletsLost = 0
        app.endOfBattleMessage = f'''The enemy made off with
a bucket of {dropletsLost} Droplets.
Click to go back inside.'''

def checkVictory(app):
    ''' return True if a battle has been won by the player '''
    for enemy in app.enemyTeam:
        if enemy.hp != 0:
            return False
    return True

def checkDefeat(app):
    ''' return True if a battle has been lost by the player '''
    for unit in app.team:
        if unit.hp != 0:
            return False
    return True

def victoryRewards(app):
    ''' earn Droplets and Seashells after winning a battle '''
    dropletsWon = seashellsWon = 0

    if not app.tutorial:
        for enemy in app.enemyTeam:
            dropletsWon += enemy.droplets
            if enemy.seashellDropRate > random.randint(0, 75):
                seashellsWon += 1
    else:
        dropletsWon = seashellsWon = 1

    app.droplets += dropletsWon
    app.seashells += seashellsWon
    app.endOfBattleMessage = f'''The enemy fled, leaving behind
a bucket of {dropletsWon} Droplets and {seashellsWon} Seashells.
Click to go back inside.'''

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
    teamScale = len(app.team) / 4
    if weapon == "pool noodle":
        hp = max(int((worstHP+2) * (teamScale/3)), 1)
        attack = max(int((worstAttack+1) * (teamScale/3)), 1)
        defense = max(int(lowestDefended * (teamScale/3)), 1)
        res = max(int((lowestDefended-1) * (teamScale/3)), 1)
        accuracy = 85
    elif weapon == "water gun":
        hp = max(int(worstHP * (teamScale/3)), 1)
        attack = max(int(worstAttack * (teamScale/3)), 1)
        defense = res = max(int(lowestDefended * (teamScale/3)), 1)
        accuracy = 80
    else:
        hp = max(int((worstHP-1) * (teamScale/3)), 1)
        attack = max(int((worstAttack-1) * (teamScale/3)), 1)
        defense = max(int((lowestDefended-1) * (teamScale/3)), 1)
        res = max(int(lowestDefended * (teamScale/3)), 1)
        accuracy = 90
    return Enemy(name, weapon, hp, attack, defense, res, accuracy, image)

####
# Map Choice and Generation
####

def chooseMap(app):
    ''' set the current map for one battle '''
    if app.freeplay: # generate a random map for freeplay
        app.map = makeMap()
        return

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

def makeMap():
    ''' generate a map '''
    rows = cols = 7
    newMap = [ ["_"] * cols for row in range(rows) ] # start with all sand (_)
    
    # place up to 8 water cells (X)
    waterToPlace = random.randint(0, 9)
    for waterCell in range(waterToPlace):
        placeSymOnMap(newMap, "X")

    # dunes (O) can be up to 1/4 of the rest of the map
    dunesToPlace = len(newMap) * len(newMap[0])
    dunesToPlace -= waterToPlace
    dunesToPlace = random.randint(0, dunesToPlace // 4)
    for duneCell in range(dunesToPlace):
        placeSymOnMap(newMap, "O")

    clearBlockedPaths(newMap)

    placeSpawnPoints(newMap)

    return newMap

def placeSymOnMap(currMap, symbol, cell=(None, None)):
    ''' place a symbol on a map cell and return the cell '''
    # choose a random cell
    if cell == (None, None):
        row = random.randrange(0, len(currMap))
        col = random.randrange(0, len(currMap[0]))
    # assign cell based on arguments
    else:
        row, col = cell
    
    while True:
        # only replace "sand" cells
        if currMap[row][col] == "_":
            currMap[row][col] = symbol
            return row, col
        
        # "dunes" and "water" cells can be spawned "together"
        elif currMap[row][col] == symbol:
            row, col = moveSymToSide(currMap, symbol, row, col)

        # limit which side spawn points are placed on
        elif symbol == "A":
            row = random.randint(0, len(currMap) - 1)
            col = random.randint(0, len(currMap[0]) // 2)
        elif symbol == "E":
            row = random.randrange(0, len(currMap))
            col = random.randrange((len(currMap[0])//2) + 1, len(currMap[0]))

        # pick a new random cell
        else:
            row = random.randrange(0, len(currMap))
            col = random.randrange(0, len(currMap[0]))

def moveSymToSide(currMap, symbol, currRow, currCol):
    ''' return a row,col where symbol can be placed next to currRow,currCol '''
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    for drow, dcol in directions:
        newRow = currRow + drow
        newCol = currCol + dcol
        # only place if cell is on the map
        if 0 <= newRow < len(currMap) and 0 <= newCol < len(currMap[0]):
            return newRow, newCol

def clearBlockedPaths(currMap):
    ''' place sand cells to clear a path through water other than a moat '''
    for blockage in findBlockages(currMap):
        toReplaceIndex = random.randrange(0, len(blockage))
        toReplace = blockage[toReplaceIndex]
        placeSymOnMap(currMap, "_", toReplace)

def findBlockages(currMap):
    ''' return a list of lists of cells that form a "blockage" on currMap '''
    blockages = []

    corner = None
    rows, cols = len(currMap), len(currMap[0])
    for row in range(rows):
        for col in range(cols):
            if currMap[row][col] == "X":
                corner = findBlockageFromCell(currMap, row, col)
                if corner != None:
                    blockages.append(corner)
    
    return blockages

def findBlockageFromCell(currMap, currRow, currCol):
    ''' return a list of 3 water cells that form a "corner" on currMap '''
    corner = [(currRow, currCol)]

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # find an adjacent water cell
    for drow, dcol in directions:
        nextRow = currRow + drow
        nextCol = currCol + dcol
        if 0 <= nextRow < len(currMap) and 0 <= nextCol < len(currMap[0]):
            if currMap[nextRow][nextCol] == "X":
                corner.append((nextRow, nextCol))
                # find another adjacent water cell
                for newDrow, newDcol in directions:
                    lastRow = nextRow + newDrow
                    lastCol = nextCol + newDcol
                    if ( 0 <= lastRow < len(currMap) and
                        0 <= lastCol < len(currMap[0]) and
                        (lastRow, lastCol) != (currRow, currCol) ):
                        # make sure cell direction isn't the same as before
                        if newDrow != drow and newDcol != dcol:
                            if currMap[lastRow][lastCol] == "X":
                                corner.append((lastRow, lastCol))
                                return corner
                # no corner found, try the next adjacent water cell
                corner.pop()

    return None

def placeSpawnPoints(currMap):
    ''' place unit and enemy spawn points on a map '''
    # 3 unit spawn points (A) on the left side
    for unitSpawn in range(3):
        col = random.randint(0, len(currMap[0]) // 2)
        row = random.randint(0, len(currMap) - 1)
        placeSymOnMap(currMap, "A", (row, col))

    # 5 enemy spawn points (E) on the right side
    for enemySpawn in range(5):
        col = random.randrange((len(currMap[0])//2) + 1, len(currMap[0]))
        row = random.randrange(0, len(currMap))
        placeSymOnMap(currMap, "E", (row, col))

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
    # exclude current position //and goal position - delete //later?
    return path[1:]

def heuristic(node, goal):
    ''' return the Manhattan distance from node to goal '''
    # drow + dcol
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
    return None

####
# Main
####

def main():
    runApp(width=600, height=750)

if (__name__ == '__main__'):
    main()