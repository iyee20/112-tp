####
# Name: Isabella Yee
# andrewID: iby
####

from cmu_112_graphics import *

####
# Import images
####

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

####
# General drawing functions
####

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
    drawButton(app, canvas, topX, topY, botX, botY, color=app.buttonColor,
                text="<--")

####
# Menu screen drawing functions
####

def drawThreeButtonMenu(app, canvas, text1, text2, text3,
                            color1, color2, color3):
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
                            storyColor, freeplayColor, app.buttonColor)

    # draw credits
    creditText = '''(C) Isabella Yee 2021 | made with Python | 15-112
Special thanks to Casper Wong'''
    canvas.create_text(0, app.height, text=creditText, anchor="sw",
                            fill=app.textColor, font=app.buttonFont)

def transitionMode_redrawAll(app, canvas):
    ''' draw the transition screen '''
    # draw progress bar
    progress = app.droplets / app.moatSize
    fillLength = int((app.width - (2 * app.margin)) * progress)
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin,
                app.margin + 30, fill="black")
    canvas.create_rectangle(app.margin, app.margin, app.margin + fillLength,
                app.margin + 30, fill="blue", width=0)
    canvas.create_text(app.width // 2, 15,
                        text=f"{app.droplets}/{app.moatSize}", fill="white")

    drawSeashells(app, canvas, app.margin, app.margin + 35)

    drawThreeButtonMenu(app, canvas, "Gacha", "Battle", "Team",
                            app.buttonColor, app.buttonColor, app.buttonColor)

def settingsMode_redrawAll(app, canvas):
    ''' draw the settings screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    drawThreeButtonMenu(app, canvas, "Change Moat Size", "Toggle Extras",
                            "Do Nothing",
                            app.buttonColor, app.buttonColor, app.buttonColor)

####
# Dialogue drawing functions
####

def cutsceneMode_redrawAll(app, canvas):
    ''' draw a cutscene '''
    # play cutscene for the most recently obtained character
    cutsceneUnit = app.barracks[-1]

    #add more later

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
    
    canvas.create_rectangle(topX, topY, botX, botY, outline=app.buttonColor)
    
    # draw text
    canvas.create_text(topX + app.margin, topY + app.margin, anchor="nw",
        text=name, fill=app.textColor, font=app.dialogueFont+" bold")
    
    space = 25
    for line in text.splitlines():
        drawDialogue(app, canvas, line, topX + app.margin, topY + space)
        space *= 2

def drawDialogue(app, canvas, line, topX, topY):
    ''' draw a line of dialogue '''
    canvas.create_text(topX, topY, text=line, anchor="nw", fill=app.textColor,
                            font=app.dialogueFont)

####
# Tutorial drawing functions
####

def tutorialMode_redrawAll(app, canvas):
    ''' draw tutorial screen '''
    pass

####
# Gacha drawing functions
####

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
# Team drawing functions
####

def barracksMode_redrawAll(app, canvas):
    ''' draw the current team in the barracks screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    oneFifthHeight = app.height // 5
    slotNum = 1
    for unit in app.team:
        drawStatus(app, canvas, unit, oneFifthHeight * slotNum, slotNum)
        slotNum += 1

def drawStatus(app, canvas, unit, topY, slotNum=-1):
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

    # draw stats and weapon
    offset = (2 * app.margin) + app.cellSize
    drawHPBar(app, canvas, unit, offset, topY)

    stats = f'''Attack {unit.attack}
Def {unit.defense}      Res {unit.res}'''
    canvas.create_text(offset, topY + 35, text=stats, anchor="nw",
                        fill=app.textColor, font=app.dialogueFont)
    
    canvas.create_text(offset * 5, topY + 35, text=unit.weapon, anchor="nw",
                        fill=app.textColor, font=app.dialogueFont)

def drawHPBar(app, canvas, unit, topX, topY):
    ''' draw a unit's HP bar '''
    canvas.create_text(topX, topY, text=f"HP: {unit.hp} / {unit.maxHP}",
                        anchor="nw", fill=app.textColor, font=app.dialogueFont)

    # draw bar below text
    filled = unit.hp // unit.maxHP
    fillLength = (app.width - topX - app.margin) * filled
    canvas.create_rectangle(topX, topY + 20, app.width - app.margin, topY + 30,
                                fill="black")
    canvas.create_rectangle(topX, topY + 20, topX + fillLength, topY + 30,
                                fill="green", width=0)

def teamSelectionMode_redrawAll(app, canvas):
    ''' draw the current found units in the team selection screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    gridOffsetX = (app.width - (7*app.cellSize)) // 2
    gridOffsetY = (app.height - (3*app.cellSize)) // 2

    # draw unit icons in a grid (up to 2 x 4)
    for unitNum in range(len(app.barracks)):
        topX = gridOffsetX + (100 * (unitNum%4))
        topY = gridOffsetY + (100 * (unitNum//4))
        unit = app.barracks[unitNum]
        # change to be more informative later
        canvas.create_rectangle(topX, topY, topX + 50, topY + 50,
                                    fill=app.buttonColor)
        canvas.create_image(topX, topY, anchor="nw",
                            image=ImageTk.PhotoImage(unit.image))
####
# Battle drawing functions
####

def battleMode_redrawAll(app, canvas):
    ''' draw the battle screen '''
    drawMap(app, canvas)

    # draw character icons on map
    for unit in app.team:
        if unit.hp != 0:
            drawCell(app, canvas, unit.row, unit.col, unit.image)
    for enemy in app.enemyTeam:
        if enemy.hp != 0:
            drawCell(app, canvas, enemy.row, enemy.col, enemy.image)
    
    if app.selected != None:
        unit = app.team[app.selected]
        drawStatus(app, canvas, unit, 0)
        drawMoveRadius(app, canvas, unit)
    else:
        drawPlayerMenu(app, canvas)

def drawPlayerMenu(app, canvas):
    ''' draw a player's menu options in battle mode '''
    fullHeight = (app.height//5) - (2*app.margin)
    buttonWidth = app.width // 6
    buttonHeight = fullHeight // 3

    canvas.create_rectangle(0, 0, app.width, app.height // 5,
                                fill=app.buttonColor)

    # draw buttons in a 2 x 2 grid
    drawButton(app, canvas, buttonWidth, app.margin, 2 * buttonWidth,
                app.margin + buttonHeight, color="white", text="Flee")
    drawButton(app, canvas, buttonWidth, app.margin + (2*buttonHeight),
                2 * buttonWidth, app.margin + (3*buttonHeight),
                color="white", text="End turn")
    drawButton(app, canvas, 3 * buttonWidth, app.margin, 5 * buttonWidth,
                app.margin + buttonHeight,
                color="white", text="Show untapped units")
    drawButton(app, canvas, 3 * buttonWidth, app.margin + (2*buttonHeight),
                5 * buttonWidth, app.margin + (3*buttonHeight),
                color="white", text="Show team summary")

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
    ''' draw a cell of a map '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = (app.height // 5) + app.margin

    topX = mapOffsetX + (app.cellSize * col)
    topY = mapOffsetY + (app.cellSize * row)

    canvas.create_image(topX, topY, anchor="nw",
                            image=ImageTk.PhotoImage(image))

def moveIsLegal(app, currRow, currCol, drow, dcol):
    ''' check if a unit can legally move in direction drow,dcol '''
    newRow = currRow + drow
    newCol = currCol + dcol
    
    # check that newRow,newCol is not already occupied
    for unit in app.team:
        if unit.row == newRow and unit.col == newCol:
            return False
    for enemy in app.enemyTeam:
        if enemy.row == newRow and enemy.col == newCol:
            return False

    # check that newRow,newCol is on map
    if newRow < 0 or newRow >= len(app.map):
        return False
    elif newCol < 0 or newCol >= len(app.map):
        return False

    # water and moats cannot be walked onto
    elif app.map[newRow][newCol] == "X":
        return False

    else:
        return True

def drawMoveRadius(app, canvas, unit):
    ''' draw rectangles around a unit's possible move locations '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = (app.height // 5) + app.margin

    # units can move up to 2 squares per turn
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1),
                    (0, 2), (2, 0), (0, -2), (-2, 0)]

    for drow,dcol in directions:
        if moveIsLegal(app, unit.row, unit.col, drow, dcol):
            newRow = unit.row + drow
            newCol = unit.col + dcol
            topX = mapOffsetX + (app.cellSize * newCol)
            topY = mapOffsetY + (app.cellSize * newRow)
            canvas.create_rectangle(topX, topY, topX + app.cellSize,
                                    topY + app.cellSize, outline="blue",
                                    width=3)
