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
    canvas.create_rectangle(0, 0, app.width, app.height, color=color, width=0)

def drawSeashells(app, canvas, topX, topY):
    ''' draw the player's Seashell count '''
    # draw box and seashell icon
    canvas.create_rectangle(topX, topY, topX + 40, topY + 20) # change later
    # insert icon here

    canvas.create_text(topX, topY, text=app.seashells, anchor="nw",
                            font=app.buttonFont)

def drawButton(app, canvas, topX, topY, botX, botY, color=app.buttonColor,
                text=""):
    ''' draw a rectangle representing a button '''
    canvas.create_rectangle(topX, topY, botX, botY, fill=color)

    centerX = botX - topX
    centerY = botY - topY
    canvas.create_text(centerX, centerY, text=text, color=app.textColor,
                        font=app.buttonFont)

def drawBackButton(app, canvas, topX, topY):
    ''' draw a back arrow button '''
    botX = topX + 10 # change later if needed
    botY = topY + 10
    drawButton(app, canvas, topX, topY, botX, botY, text="<--")

####
# Menu screen drawing functions
####

def drawThreeButtonMenu(app, canvas, text1, text2, text3,
        color1=app.buttonColor, color2=app.buttonColor, color3=app.buttonColor):
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
                            color1=storyColor, color2=freeplayColor)

    # draw credits
    creditText = '''(C) Isabella Yee 2021 | made with Python | 15-112
Special thanks to Casper Wong'''
    canvas.create_text(0, app.height, text=creditText, anchor="sw",
                            color=app.textColor, font=app.buttonFont)

def transitionMode_redrawAll(app, canvas):
    ''' draw the transition screen '''
    # draw progress bar
    progress = app.droplets // app.moatSize
    fillLength = (app.width - (2 * app.margin)) * progress
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin,
                app.margin + 10, fill="black")
    canvas.create_rectangle(app.margin, app.margin, app.margin + fillLength,
                app.margin + 10, fill="blue", width=0)
    canvas.create_text(app.width // 2, 5, text=f"{app.droplets}/{app.moatSize}",
                color="white")

    drawSeashells(app, canvas, app.margin, app.margin + 15)

    drawThreeButtonMenu(app, canvas, "Gacha", "Battle", "Team")

def settingsMode_redrawAll(app, canvas):
    ''' draw the settings screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    drawThreeButtonMenu(app, canvas, "Change Moat Size", "Toggle Extras",
                            "Do Nothing")

####
# Dialogue drawing functions
####

def drawDialogueBox(app, canvas, name, text, position="bottom"):
    ''' draw a character's dialogue box '''
    if position == "bottom":
        topX = 0
        topY = app.height - 10 # change later
        botX = app.width
        botY = app.height
    else: # position == "top"
        topX = topY = 0
        botX = app.width
        botY = 10 # change later
    
    canvas.create_rectangle(topX, topY, botX, botY, outline=app.borderColor,
        width=5)
    
    # draw text
    canvas.create_text(topX + app.margin, topY + app.margin, anchor="nw",
        text=name, color=app.textColor, font=app.dialogueFont)
    
    space = 10 # change later
    for line in text.splitlines():
        drawDialogue(app, canvas, line, topX + app.margin, topY + space)
        space *= 2

def drawDialogue(app, canvas, line, topX, topY):
    ''' draw a line of dialogue '''
    canvas.create_text(topX, topY, text=line, anchor="nw", color=app.textColor,
                            font=app.dialogueFont)

####
# Gacha drawing functions
####

def gachaMode_redrawAll(app, canvas):
    ''' draw the gacha screen '''
    # draw Anna dialogue
    if not app.tutorial:
        dialogue = '''I wonder who we'll meet today!
Each pull costs 1 Seashell.'''
    else:
        dialogue = "I haven't written this yet." # change later
    drawDialogueBox(app, canvas, "Anna", dialogue, "top")

    drawSeashells(app, canvas, app.margin, 10) # change later

    drawBackButton(app, canvas, app.margin, 10) # change later

    # draw gacha machine
    pass

    # draw buttons
    oneFifthWidth = app.width // 5
    oneFifthHeight = app.height // 5
    drawButton(app, canvas, oneFifthWidth, oneFifthHeight * 4,
                oneFifthWidth * 2, oneFifthHeight * 9 // 2, text="1-pull")
    drawButton(app, canvas, oneFifthWidth * 3, oneFifthHeight * 4,
                oneFifthWidth * 4, oneFifthHeight * 9 // 2, text="3-pull")

####
# Team drawing functions
####

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
    # outline selected units in red
    if app.selected == slotNum:
        outlineColor = "red"
    else:
        outlineColor = "black"
    canvas.create_rectangle(0, topY, app.width, topY + (app.height//5),
                                fill=app.buttonColor, outline=outlineColor)

    # draw unit name and icon
    canvas.create_text(app.margin, topY + app.margin, anchor="nw",
        text=unit.name, color=app.textColor, font=app.dialogueFont)
    cx = cy = app.margin + (app.cellSize // 2)
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(unit.image))

    # draw stats and inventory
    offset = (2 * app.margin) + app.cellSize
    drawHPBar(app, canvas, unit, offset, topY)
    # insert weapon icon later
    stats = f'''Attack {unit.attack}
Def {unit.defense}      Res {unit.res}'''

def drawHPBar(app, canvas, unit, topX, topY):
    ''' draw a unit's HP bar '''
    canvas.create_text(topX, topY, text=f"{unit.hp} / {unit.maxHP}",
                        anchor="nw", color=app.textColor, font=app.dialogueFont)

    # draw bar below text
    filled = unit.hp // unit.maxHP
    fillLength = (app.width - topX - app.margin) * filled
    canvas.create_rectangle(topX, topY + 10, app.width - app.margin, topY + 20,
                                fill="black") # change Ys later
    canvas.create_rectangle(topX, topY + 10, topX + fillLength, topY + 20,
                                fill="green", width=0)

####
# Battle drawing functions
####

def drawBattleScreen(app, canvas):
    ''' draw the battle screen '''
    # insert check for menu/status/etc here

    drawMap(app, canvas, app.map)
    for unit in app.team:
        pass # draw player team
    # draw enemies

def drawMap(app, canvas):
    ''' draw a battle map '''
    # terrain colors - change later
    sand = "yellow"
    dune = "orange"
    water = "blue"
    castle = "brown"

    # draw terrain according to map
    rows, cols = len(app.map), len(app.map[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.map[row][col]
            if cell == "O":
                drawCell(app, canvas, row, col, dune)
            elif cell == "X":
                drawCell(app, canvas, row, col, water)
            elif cell == "*":
                drawCell(app, canvas, row, col, castle)
            else:
                drawCell(app, canvas, row, col, sand)

def drawCell(app, canvas, row, col, color):
    ''' draw a cell of a battle map '''
    topX = app.margin + (app.cellSize * col)
    topY = app.mapOffset + (app.cellSize * row)
    botX = topX + app.cellSize
    botY = topY + app.cellSize

    canvas.create_rectangle(topX, topY, botX, botY, color=color)