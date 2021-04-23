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

    drawThreeButtonMenu(app, canvas, "Change Moat Size", "Toggle Cheats",
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
    
    canvas.create_rectangle(topX, topY, botX, botY, fill="white",
                            outline=app.buttonColor)
    
    # draw text
    canvas.create_text(topX + app.margin, topY + app.margin, anchor="nw",
        text=name, fill=app.textColor, font=app.dialogueFont+" bold")
    
    space = 30
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
    if app.foundAllUnits: # new character button is inactive
        pullButtonColor = "gray"
    else:
        pullButtonColor = app.buttonColor

    oneEighthWidth = app.width // 8
    buttonWidth = int(2.5 * oneEighthWidth)
    oneFifthHeight = app.height // 5
    drawButton(app, canvas, oneEighthWidth, oneFifthHeight * 4,
                oneEighthWidth + buttonWidth, oneFifthHeight * 9 // 2,
                color=pullButtonColor, text="New Character")
    drawButton(app, canvas, (oneEighthWidth*7) - buttonWidth,
                oneFifthHeight * 4, oneEighthWidth * 7, oneFifthHeight * 9 // 2,
                color=app.buttonColor, text="Strengthen 3 Characters")

####
# Cutscene drawing functions
####

def cutsceneMode_redrawAll(app, canvas):
    ''' draw a cutscene '''
    drawBackground(app, canvas, app.buttonColor) # change later

    # play dialogue of most recently acquired character
    characterName = app.barracks[-1].name
    allDialogue = chooseCutscene(app, characterName)
    
    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, characterName,
                            allDialogue[app.onCutsceneLine])
    else:
        fourFifthsHeight = int(app.height * 4/5)
        drawButton(app, canvas, 0, fourFifthsHeight, app.width, app.height,
                        color=app.buttonColor, text="Click to go back to gacha")

def chooseCutscene(app, character=None):
    ''' return the dialogue corresponding to a cutscene '''
    if character == "Giang":
        return giangDialogue(app)
    elif character == "Iara":
        return iaraDialogue(app)
    elif character == "Kai":
        return kaiDialogue(app)
    elif character == "Marina":
        return marinaDialogue(app)
    elif character == "Morgan":
        return morganDialogue(app)
    elif character == "Naia":
        return naiaDialogue(app)
    elif character == "Walter":
        return walterDialogue(app)
    else: # ending scene
        return endDialogue(app)

def giangDialogue(app):
    ''' return Giang's cutscene dialogue '''
    giangIntro = [
        '''Oh, hey. This is the Sand Castle, right?
>>''',
        '''I thought so... I'm Giang, he/him, by the way.
>>''',
        '''I saw a bunch of suspicious characters on my way here, so I wanted to
check if anyone was taking care of that.
>>''',
        "Huh? You want me to help you? ...I guess there's no helping it."
    ]
    return giangIntro

def iaraDialogue(app):
    ''' return Iara's cutscene dialogue '''
    iaraIntro = [
        f'''Aren't you {app.aqua.name}? The hero who's helping fill the Moat?
>>''',
        '''There's no need to be humble. It's a noble cause. In fact, I'm here
to lend my aid as well.
>>''',
        "My name is Iara, she/her, and my Pool Noodle is at your disposal."
    ]
    return iaraIntro

def kaiDialogue(app):
    ''' return Kai's cutscene dialogue '''
    kaiIntro = [
        '''Ah. You saw me.
>>''',
        '''I know there's a gatekeeper, but every time I try scouting the Sand
Castle for places to shoot from, she tries recruiting me to fill the Moat.
>>''',
        '''You're doing that too? Hm... if you insist, I'll join you.
>>''',
        '''My name is Kai.
>>''',
        "Pronouns? ...just avoid referring to me. It's fine."
    ]
    return kaiIntro

def marinaDialogue(app):
    ''' return Marina's cutscene dialogue '''
    marinaIntro = [
        '''Such a pretty castle! And so big! Hey, you! It's nice to meet you!
>>''',
        '''You can call me Marina! She/her! I'm here to help fill the Moat!
>>''',
        "You're doing that too? Wow! I'm glad I came to the right place!"
    ]
    return marinaIntro

def morganDialogue(app):
    ''' return Morgan's cutscene dialogue '''
    morganIntro = [
        '''...
>>''',
        '''...
>>''',
        "...Morgan, he/him. Here to help."
    ]
    return morganIntro

def naiaDialogue(app):
    ''' return Naia's cutscene dialogue '''
    naiaIntro = [
        f'''Why, hello. You must be {app.aqua.name}. My name is Naia, she/her.
Pleased to make your acquaintance.
>>''',
        "I've come to assist the Moat-filling effort in any way that I can."
    ]
    return naiaIntro

def walterDialogue(app):
    ''' return Walter's cutscene dialogue '''
    walterIntro = [
        '''This is the Sand Castle with a Moat that needs to be filled, right?
>>''',
        '''...Don't get the wrong idea! It's not like I'm here to help.
I just wanted to know.
>>''',
        '''Don't look at me like that...! Ugh, fine. Since you need my help so
badly, I guess I'll lend a hand.
>>''',
        "I'm Walter, he/him. The L is silent. Don't get it wrong."
    ]
    return walterIntro

def endDialogue(app):
    ''' return Nerissa's dialogue during the ending cutscene '''
    endingDialogue = [
        f'''Hello, {app.aqua.name}. Thank you for your help filling the Moat.
We couldn't have done it without you!
>>''',
        '''Wait, did I forget to introduce myself? I'm Nerissa, the princess of
the Sand Castle.
>>'''
    ] # add more later
    return endingDialogue

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
    canvas.create_text(offset, topY + app.margin, text=f"Level {unit.level}",
                        anchor="nw", fill=app.textColor, font=app.dialogueFont)
    drawHPBar(app, canvas, unit, offset, topY + 25)

    stats = f'''Attack {unit.attack}
Def {unit.defense}      Res {unit.res}'''
    canvas.create_text(offset, topY + 60, text=stats, anchor="nw",
                        fill=app.textColor, font=app.dialogueFont)
    
    canvas.create_text(offset * 4, topY + app.margin, text=unit.weapon,
                        anchor="nw", fill=app.textColor, font=app.dialogueFont)

def drawHPBar(app, canvas, unit, topX, topY):
    ''' draw a unit's HP bar '''
    canvas.create_text(topX, topY, text=f"HP: {unit.hp} / {unit.maxHP}",
                        anchor="nw", fill=app.textColor, font=app.dialogueFont)

    # draw bar below text
    filled = unit.hp / unit.maxHP
    fillLength = int((app.width - topX - app.margin) * filled)
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
    drawUnitsOnMap(app, canvas)
    
    # draw status bar of selected unit
    if app.selected != None:
        unit = app.team[app.selected]
        drawStatus(app, canvas, unit, 0)
        drawMoveRadius(app, canvas, unit)
    else:
        if app.battleMenuDisplay == 0:
            drawPlayerMenu(app, canvas)
    
    if app.battleMessage != None:
        canvas.create_text(app.width // 2, int(app.height * 0.9),
                            text=app.battleMessage, font=app.dialogueFont,
                            justify="center")

def drawUnitsOnMap(app, canvas):
    ''' draw the icons of undefeated units on the map '''
    for unit in app.team:
        if unit.hp != 0:
            drawCell(app, canvas, unit.row, unit.col, unit.image)
    for enemy in app.enemyTeam:
        if enemy.hp != 0:
            drawCell(app, canvas, enemy.row, enemy.col, enemy.image)

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
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))

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
    elif newCol < 0 or newCol >= len(app.map[0]):
        return False

    # water and moats cannot be walked onto
    elif app.map[newRow][newCol] == "X":
        return False

    else:
        return True

def drawMoveRadius(app, canvas, unit):
    ''' draw rectangles around a unit's possible move locations '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))

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
