####
# Name: Isabella Yee
# andrewID: iby
####

from cmu_112_graphics import *
import random

# This file is only for testing.

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
    
    def heal(self, target):
        ''' heal a target unit '''
        amount = self.attack // 2
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
    # balance stats later
    app.aqua = PlayableChar("Aqua", "pool noodle", 15, 5, 5, 5, 95, app.aquaImg)
    giang = PlayableChar("Giang", "water gun", 15, 5, 5, 5, 95, app.giangImg)
    iara = PlayableChar("Iara", "pool noodle", 15, 5, 5, 5, 95, app.iaraImg)
    kai = PlayableChar("Kai", "water gun", 15, 5, 5, 5, 95, app.kaiImg)
    marina = PlayableChar("Marina", "bubble wand", 15, 5, 5, 5, 95,
                            app.marinaImg)
    morgan = PlayableChar("Morgan", "bubble wand", 15, 5, 5, 5, 95,
                            app.morganImg)
    naia = PlayableChar("Naia", "water gun", 15, 5, 5, 5, 95, app.naiaImg)
    walter = PlayableChar("Walter", "pool noodle", 15, 5, 5, 5, 95,
                            app.walterImg)
    
    app.toPull = {giang, iara, kai, marina, morgan, naia, walter}

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

def loadImages(app):
    ''' import images from local files '''
    # backgrounds

    # map-related images
    
    # character icons
    loadIcons(app)

    # character fullbodies

    # misc
    app.seashellImg = app.loadImage("images/seashell.png")
    app.castleCellImg = app.loadImage("images/castle.png")
    app.duneCellImg = app.loadImage("images/dune.png")
    app.moatCellImg = app.loadImage("images/moat.png")
    app.sandCellImg = app.loadImage("images/sand.png")

def loadIcons(app):
    ''' load character icon images '''
    # NPCs
    app.annaImg = app.loadImage("images/anna.png")

    # playable characters
    app.aquaImg = app.loadImage("images/aqua.png")
    app.giangImg = app.loadImage("images/giang.png")
    app.iaraImg = app.loadImage("images/iara.png")
    app.kaiImg = app.loadImage("images/kai.png")
    app.marinaImg = app.loadImage("images/marina.png")
    app.morganImg = app.loadImage("images/morgan.png")
    app.naiaImg = app.loadImage("images/naia.png")
    app.walterImg = app.loadImage("images/walter.png")

    # enemies
    app.dehydrationImg = app.loadImage("images/dehydration.png")
    app.heatstrokeImg = app.loadImage("images/heatstroke.png")
    app.saltImg = app.loadImage("images/salt.png")

def drawBackground(app, canvas, color):
    ''' set the background to a solid color '''
    canvas.create_rectangle(0, 0, app.width, app.height, fill=color, width=0)

def drawSeashells(app, canvas, topX, topY):
    ''' draw the player's Seashell count '''
    # draw box and seashell icon
    canvas.create_rectangle(topX, topY, topX + 70, topY + 40)
    canvas.create_image(topX + app.margin, topY + app.margin, anchor="nw",
                            image=ImageTk.PhotoImage(app.seashellImg))

    canvas.create_text(topX + 40, topY + 20, text=app.seashells, anchor="w",
                            font=app.buttonFont)

def drawButton(app, canvas, topX, topY, botX, botY, color="blue", text=""):
    ''' draw a rectangle representing a button '''
    canvas.create_rectangle(topX, topY, botX, botY, fill=color)

    centerX = (botX + topX) // 2
    centerY = (botY + topY) // 2
    canvas.create_text(centerX, centerY, text=text, fill=app.textColor,
                        font=app.buttonFont)

def drawBackButton(app, canvas, topX, topY):
    ''' draw a back arrow button '''
    botX = topX + (app.height // 10)
    botY = topY + (app.height // 10)
    drawButton(app, canvas, topX, topY, botX, botY, text="<--")

def drawThreeButtonMenu(app, canvas, text1, text2, text3,
        color1="blue", color2="blue", color3="blue"):
    ''' draw a menu with three buttons '''
    oneFifthHeight = app.height // 5
    drawButton(app, canvas, app.margin, oneFifthHeight, app.width - app.margin,
            (oneFifthHeight*2) - app.margin, color=color1, text=text1)
    drawButton(app, canvas, app.margin, oneFifthHeight * 2,
                    app.width - app.margin, (oneFifthHeight*3) - app.margin,
                    color=color2, text=text2)
    drawButton(app, canvas, app.margin, oneFifthHeight * 3,
                    app.width - app.margin, (oneFifthHeight*4) - app.margin,
                    color=color3, text=text3)

def drawDialogueBox(app, canvas, name, text, position="bottom"):
    ''' draw a character's dialogue box '''
    if position == "bottom":
        topX = 0
        topY = app.height * 4 // 5
        botX = app.width
        botY = app.height
    else: # position == "top"
        topX = topY = 0
        botX = app.width
        botY = app.height // 5
    
    canvas.create_rectangle(topX, topY, botX, botY, outline=app.borderColor,
        width=5)
    
    # draw text
    canvas.create_text(topX + app.margin, topY + app.margin, anchor="nw",
        text=name, fill=app.textColor, font=app.dialogueFont)
    
    space = 25
    for line in text.splitlines():
        drawDialogue(app, canvas, line, topX + app.margin, topY + space)
        space *= 2

def drawDialogue(app, canvas, line, topX, topY):
    ''' draw a line of dialogue '''
    canvas.create_text(topX, topY, text=line, anchor="nw", fill=app.textColor,
                            font=app.dialogueFont)

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

def mainScreenMode_redrawAll(app, canvas):
    ''' draw the main screen '''
    drawBackground(app, canvas, "white") # change later

    # draw title
    pass

    # draw buttons
    if app.freeplay:
        storyColor = "gray"
        freeplayColor = app.buttonColor
    else:
        storyColor = app.buttonColor
        freeplayColor = "gray"
    oneFifthHeight = app.height // 5
    drawThreeButtonMenu(app, canvas, "Story", "Freeplay", "Settings",
                            color1=storyColor, color2=freeplayColor)

    # draw credits
    creditText = '''(C) Isabella Yee 2021 | made with Python | 15-112
Special thanks to Casper Wong'''
    canvas.create_text(0, app.height, text=creditText, anchor="sw",
                            fill=app.textColor, font=app.buttonFont)

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

def settingsMode_redrawAll(app, canvas):
    ''' draw the settings screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    drawThreeButtonMenu(app, canvas, "Change Moat Size", "Toggle Extras",
                            "Do Nothing")

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

def transitionMode_redrawAll(app, canvas):
    ''' draw the transition screen '''
    # draw progress bar
    progress = app.droplets // app.moatSize
    fillLength = (app.width - (2 * app.margin)) * progress
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin,
                app.margin + 30, fill="black")
    canvas.create_rectangle(app.margin, app.margin, app.margin + fillLength,
                app.margin + 30, fill="blue", width=0)
    canvas.create_text(app.width // 2, 15,
                        text=f"{app.droplets}/{app.moatSize}", fill="white")

    drawSeashells(app, canvas, app.margin, app.margin + 35)

    drawThreeButtonMenu(app, canvas, "Gacha", "Battle", "Team")

####
# Barracks screen
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
        # insert more options later

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

def barracksMode_redrawAll(app, canvas):
    ''' draw the current team in the barracks screen '''
    drawBackground(app, canvas, "blue")

    drawBackButton(app, canvas, app.margin, app.margin)

    oneFifthHeight = app.height // 5
    slotNum = 1
    for unit in app.team:
        drawStatus(app, canvas, unit, oneFifthHeight * slotNum, slotNum)
        slotNum += 1

def drawStatus(app, canvas, unit, topY, slotNum):
    ''' draw a unit's status bar '''
    statusBarHeight = topY + (app.height//5)

    # outline selected units in red
    if app.selected == slotNum:
        outlineColor = "red"
    else:
        outlineColor = "black"
    canvas.create_rectangle(0, topY, app.width, statusBarHeight,
                                fill=app.buttonColor, outline=outlineColor)

    # draw unit name and icon
    canvas.create_text(app.margin, statusBarHeight - app.margin, anchor="sw",
        text=unit.name, fill=app.textColor, font=app.dialogueFont)
    cx = app.margin + (app.cellSize // 2)
    cy = cx + topY
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(unit.image))

    # draw stats and inventory
    offset = (2 * app.margin) + app.cellSize
    drawHPBar(app, canvas, unit, offset, topY)
    # insert weapon name later
    stats = f'''Attack {unit.attack}
Def {unit.defense}      Res {unit.res}'''
    canvas.create_text(offset, topY + 35, text=stats, anchor="nw",
                        fill=app.textColor, font=app.dialogueFont)

def drawHPBar(app, canvas, unit, topX, topY):
    ''' draw a unit's HP bar '''
    canvas.create_text(topX, topY, text=f"{unit.hp} / {unit.maxHP}",
                        anchor="nw", fill=app.textColor, font=app.dialogueFont)

    # draw bar below text
    filled = unit.hp // unit.maxHP
    fillLength = (app.width - topX - app.margin) * filled
    canvas.create_rectangle(topX, topY + 20, app.width - app.margin, topY + 30,
                                fill="black")
    canvas.create_rectangle(topX, topY + 20, topX + fillLength, topY + 30,
                                fill="green", width=0)

####
# Battle screen
####

####
# Searching algorithm for enemies
####

"""
Pseudocode

destination = nearest cell such that target is in range
store nodes n: node n-1 in dictionary --> reconstruct path later in helper

heuristic h(n) = (estimate) Manhattan/row,col distance to destination from node
// this doesn't account for terrain in the way
// function used as a function param

Need:
- set (?) of visited nodes (more efficient is a priority queue, but...)
// == {startNode} at first
- empty dict() for path storage
- dict() for g(n) = cost to get to node n (== 0 for start)
- dict() for f(n) = g(n) + h(n) (== h(start) for start)

While loop (while node storage isn't empty):
    current node = the one with the lowest f(n)
    if current node is the destination: return the reconstructed path
    remove the current node from the node storage (represents traveling past it)
    for each (legal) neighbor of the current node:
        calculated g (from start to neighbor via current) = g(current) +
                distance from neighbor to current
        if calculated g < g(neighbor): path is the best so far
            store path to neighbor as current
            g[neighbor] = calculated g
            f[neighbor] = g[neighbor] + h(neighbor)
            if neighbor not in visited nodes: add neighbor to visited nodes

failure condition = node storage is empty without reaching destination
// this shouldn't happen...
"""

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

def battleMode_redrawAll(app, canvas):
    ''' draw the battle screen '''
    # insert check for menu/status/etc here later

    drawMap(app, canvas)
    for unit in app.team:
        if unit.hp != 0:
            drawCell(app, canvas, unit.row, unit.col, unit.image)
    # draw enemies later

def drawMap(app, canvas):
    ''' draw a battle map '''
    # draw terrain according to 2D list
    rows, cols = len(app.map), len(app.map[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.map[row][col]
            if cell == "O":
                drawCell(app, canvas, row, col, app.duneCellImg)
            elif cell == "X":
                drawCell(app, canvas, row, col, app.moatCellImg)
            elif cell == "*":
                drawCell(app, canvas, row, col, app.castleCellImg)
            else:
                drawCell(app, canvas, row, col, app.sandCellImg)

def drawCell(app, canvas, row, col, image):
    ''' draw a cell of a battle map '''
    topX = app.margin + (app.cellSize * col)
    topY = app.mapOffset + (app.cellSize * row)

    canvas.create_image(topX, topY, anchor="nw",
                            image=ImageTk.PhotoImage(image))

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

def gachaMode_redrawAll(app, canvas):
    ''' draw the gacha screen '''
    # draw Anna dialogue
    dialogue = '''I wonder who we'll meet today!
Each pull costs 1 Seashell.'''
    drawDialogueBox(app, canvas, "Anna", dialogue, "top")

    offsetFromBox = (app.height//5) + app.margin
    drawSeashells(app, canvas, (app.height//10) + (2*app.margin), offsetFromBox)

    drawBackButton(app, canvas, app.margin, offsetFromBox)

    # draw gacha machine
    pass

    # draw buttons
    if app.foundAllUnits: # buttons are inactive
        pullButtonColor = "gray"
    else:
        pullButtonColor = app.buttonColor

    oneFifthWidth = app.width // 5
    oneFifthHeight = app.height // 5
    drawButton(app, canvas, oneFifthWidth, oneFifthHeight * 4,
                oneFifthWidth * 2, oneFifthHeight * 9 // 2,
                color=pullButtonColor, text="1-pull")
    drawButton(app, canvas, oneFifthWidth * 3, oneFifthHeight * 4,
                oneFifthWidth * 4, oneFifthHeight * 9 // 2,
                color=pullButtonColor, text="3-pull")

####
# Main
####

def main():
    runApp(width=500, height=500) # change later

if (__name__ == '__main__'):
    main()