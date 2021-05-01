####
# Name: Isabella Yee
# andrewID: iby
####

from cmu_112_graphics import *
from tp_event_functions import readFile
from tp_content import PlayableChar

####
# Import images
####

def loadImages(app):
    ''' import images from local files '''
    # backgrounds
    app.sandCastleImg = app.loadImage("images/sandCastle.png")
    app.decoImg = app.loadImage("images/deco.png")

    # map-related images
    app.castleCellImg = app.loadImage("images/castle.png")
    app.duneCellImg = app.loadImage("images/dune.png")
    app.moatCellImg = app.loadImage("images/moat.png")
    app.sandCellImg = app.loadImage("images/sand.png")
    
    # character images
    loadIcons(app)
    app.nerissaImg = app.loadImage("images/nerissa.png")

    # misc
    app.titleImg = app.loadImage("images/title.png")
    app.seashellImg = app.loadImage("images/seashell.png")
    app.gachaImg = app.loadImage("images/gacha.png")

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

def drawBackground(app, canvas, image):
    ''' set the background to an image '''
    canvas.create_image(0, 0, anchor="nw", image=ImageTk.PhotoImage(image))

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
    canvas.create_text(centerX, centerY, text=text,
                        font=app.buttonFont, justify="center")

def drawBackButton(app, canvas, topX, topY):
    ''' draw a back arrow button '''
    botX = topX + (app.height // 10)
    botY = topY + (app.height // 10)
    drawButton(app, canvas, topX, topY, botX, botY, color=app.buttonColor,
                text="<--")

####
# Menu-only screen drawing functions
####

def drawThreeButtonMenu(app, canvas, text1, text2, text3,
                            color1, color2, color3):
    ''' draw a menu with three buttons '''
    oneFifthHeight = app.height // 5
    buttonHeight = oneFifthHeight - app.margin

    drawButton(app, canvas, app.margin, oneFifthHeight, app.width - app.margin,
                    oneFifthHeight + buttonHeight, color=color1, text=text1)
    drawButton(app, canvas, app.margin, oneFifthHeight * 2,
                    app.width - app.margin, (oneFifthHeight*2) + buttonHeight,
                    color=color2, text=text2)
    drawButton(app, canvas, app.margin, oneFifthHeight * 3,
                    app.width - app.margin, (oneFifthHeight*3) + buttonHeight,
                    color=color3, text=text3)

def mainScreenMode_redrawAll(app, canvas):
    ''' draw the main screen '''
    drawTitle(app, canvas)

    # draw buttons
    if app.saveFilePath == None:
        # a save file must be chosen before the game can begin
        playColor = "gray"
    else:
        playColor = app.buttonColor
    oneFifthHeight = app.height // 5
    drawThreeButtonMenu(app, canvas, "Choose Save File", "Play", "Settings",
                                    app.buttonColor, playColor, app.buttonColor)

    # draw credits
    creditText = ''' (C) Isabella Yee 2021 | made with Python | 15-112
 Special thanks to Casper Wong'''
    canvas.create_text(0, app.height, text=creditText, anchor="sw",
                            font=app.buttonFont)

def drawTitle(app, canvas):
    ''' draw the game title '''
    canvas.create_image(0, 0, anchor="nw",
                            image=ImageTk.PhotoImage(app.titleImg))

def settingsMode_redrawAll(app, canvas):
    ''' draw the settings screen '''
    drawBackground(app, canvas, app.decoImg)

    drawBackButton(app, canvas, app.margin, app.margin)

    # display current settings
    moatButtonText = f"Change Moat Size (currently {app.moatSize} Droplets)"
    if app.cheats:
        cheatButtonText = "Toggle Cheats (currently ON)"
    else:
        cheatButtonText = "Toggle Cheats (currently OFF)"
    if app.freeplay:
        gameModeButtonText = "Toggle Game Mode (currently Freeplay)"
    else:
        gameModeButtonText = "Toggle Game Mode (current Story)"

    drawThreeButtonMenu(app, canvas, moatButtonText, cheatButtonText,
                            gameModeButtonText,
                            app.buttonColor, app.buttonColor, app.buttonColor)

def saveMode_redrawAll(app, canvas):
    ''' draw the save file choice screen '''
    drawBackground(app, canvas, app.decoImg)

    drawBackButton(app, canvas, app.margin, app.margin)

    canvas.create_text(app.width // 2, app.height // 5,
                        text="Click to choose a save file.",
                        font=app.dialogueFont)

    # draw player names associated with saves
    name1, name2 = getSaveNames(app)
    drawButton(app, canvas, app.margin, app.height // 3,
                    (app.width - app.margin) // 2, app.height // 3 * 2,
                    color=app.buttonColor, text=f"Save 1\n{name1}")
    drawButton(app, canvas, (app.width + app.margin) // 2, app.height // 3,
                    app.width - app.margin, app.height // 3 * 2,
                    color=app.buttonColor, text=f"Save 2\n{name2}")
    
    # display current selected save file
    saveNum = 0
    if app.saveFilePath == "saves/save1.txt": saveNum = 1
    elif app.saveFilePath == "saves/save2.txt": saveNum = 2

    if saveNum != 0:
        canvas.create_text(app.width // 2, app.height - 100,
                                text=f'''Currently using save file {saveNum}.
Press Delete or Backspace to clear the save file.''',
                                font=app.dialogueFont, justify="center")

def getSaveNames(app):
    ''' return the player name corresponding to a save, or Empty for no save '''
    # the first line of a filled save file is the player name
    try:
        name1 = readFile("saves/save1.txt").splitlines()[0]
    except:
        name1 = "Empty"
    
    try:
        name2 = readFile("saves/save2.txt").splitlines()[0]
    except:
        name2 = "Empty"
    
    return name1, name2

####
# Transition screen drawing functions
####

def transitionMode_redrawAll(app, canvas):
    ''' draw the transition screen '''
    drawProgressBar(app, canvas)

    drawSeashells(app, canvas, app.margin, app.margin + 35)

    if app.tutorial: # deactivate buttons at some steps of the tutorial
        drawTutorialTransition(app, canvas)
        if len(app.team) == 1:
            color1 = app.buttonColor
            color2 = color3 = "gray"
        else:
            color2 = "gray"
            color1 = color3 = app.buttonColor
    else:
        color1 = color2 = color3 = app.buttonColor

        # draw reminder to save
        canvas.create_text(app.width // 2, app.height - 40,
                    text="Press S to save the game.", font=app.dialogueFont)

    drawThreeButtonMenu(app, canvas, "Gacha", "Battle", "Team",
                                                        color1, color2, color3)

def drawProgressBar(app, canvas):
    ''' draw the moat filling progress bar '''
    progress = app.droplets / app.moatSize
    fillLength = int((app.width - (2 * app.margin)) * progress)

    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin,
                app.margin + 30, fill="black")
    canvas.create_rectangle(app.margin, app.margin, app.margin + fillLength,
                app.margin + 30, fill="blue", width=0)
    canvas.create_text(app.width // 2, 15,
                        text=f"{app.droplets}/{app.moatSize}", fill="white")

def drawTutorialTransition(app, canvas):
    ''' draw the prompts in transition mode during the tutorial '''
    if len(app.team) == 1:
        allDialogue = enterGachaDialogue()
    else:
        allDialogue = enterBarracksDialogue()
    
    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, "Anna", allDialogue[app.onCutsceneLine])

def enterGachaDialogue():
    ''' return the prompt to enter the gacha screen '''
    enterGachaDialogue = [
        '''Nice work! We're one Droplet closer to filling the Moat now. And it
looks like you picked up a Seashell, too.
>>''',
        '''I hear that Seashells can be used to make wishes that actually come
true. Why don't you go to the Gacha area and see for yourself?'''
    ]
    return enterGachaDialogue

def enterBarracksDialogue():
    ''' return the prompt to enter the barracks screen '''
    enterBarracksDialogue = [
        '''Looks like we have a new friend! Let's try changing the order of the
team in the Team area.'''
    ]
    return enterBarracksDialogue

####
# Dialogue drawing functions
####

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
        text=name, font=app.dialogueFont+" bold")
    
    space = 30
    for line in text.splitlines():
        drawDialogue(app, canvas, line, topX + app.margin, topY + space)
        space += 30

def drawDialogue(app, canvas, line, topX, topY):
    ''' draw a line of dialogue '''
    canvas.create_text(topX, topY, text=line, anchor="nw",
                        font=app.dialogueFont)

####
# Tutorial (opening) drawing functions
####

def tutorialMode_redrawAll(app, canvas):
    ''' draw tutorial screen '''
    drawBackground(app, canvas, app.sandCastleImg)

    canvas.create_image(app.width // 2, app.height // 2,
                            image=ImageTk.PhotoImage(app.annaImg))

    allDialogue = openingDialogue(app)

    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, "Anna", allDialogue[app.onCutsceneLine])

def openingDialogue(app):
    ''' return the game's opening dialogue '''
    openingDialogue = [
        f'''Hey there, stranger. Welcome to the Sand Castle. What’s your name?
CLICK TO ENTER NAME >>>''',
        f'''{app.aqua.name}, huh? I’m Anna, the gatekeeper.
PRESS SPACE TO CONTINUE >>''',
        '''Bottom text? What do you mean? ...Maybe you’re imagining things.
It probably won’t happen again.
>>''',
        '''By the way, here’s a message from the programmer…
"Please don’t resize the window or I WILL cry :(("
>>''',
        '''I wonder what that’s about. A sign of being overworked, maybe?
>>''',
        "Huh? What was that?"
    ]
    return openingDialogue

####
# Gacha drawing functions
####

def gachaMode_redrawAll(app, canvas):
    ''' draw the gacha screen '''
    # draw Anna dialogue
    dialogue = '''I wonder who we'll meet today!
Use 1 Seashell to wish for a new character, or use
3 Seashells to power up 3 random characters in the barracks.'''
    drawDialogueBox(app, canvas, "Anna", dialogue, "top")

    offsetFromBox = (app.height//5) + app.margin
    drawSeashells(app, canvas, (app.height//10) + (2*app.margin), offsetFromBox)

    drawBackButton(app, canvas, app.margin, offsetFromBox)

    drawGachaMachine(app, canvas)

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

def drawGachaMachine(app, canvas):
    ''' draw the gacha machine '''
    topX = app.width // 4
    topY = app.height // 3

    canvas.create_image(topX, topY, anchor="nw",
                            image=ImageTk.PhotoImage(app.gachaImg))

####
# Cutscene drawing functions
####

def cutsceneMode_redrawAll(app, canvas):
    ''' draw a cutscene '''
    drawBackground(app, canvas, app.sandCastleImg)

    if not app.storyModeEnd:
        # play dialogue of most recently acquired character
        characterName = app.barracks[-1].name
    else: # ending scene
        characterName = "Nerissa"
    allDialogue, image = chooseCutscene(app, characterName)
    
    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, characterName,
                            allDialogue[app.onCutsceneLine])
    else:
        fourFifthsHeight = int(app.height * 4/5)
        if not app.storyModeEnd:
            text = "Click here to go back to gacha"
        else:
            text = "Click here to return to main screen"
        drawButton(app, canvas, 0, fourFifthsHeight, app.width, app.height,
                        color=app.buttonColor, text=text)
    
    # draw Aqua and character together
    drawAquaWithImage(app, canvas, image)

def drawAquaWithImage(app, canvas, image):
    ''' draw Aqua's icon next to another image '''
    imageWidth, imageHeight = image.size
    fullWidth = (app.cellSize*2) + imageWidth

    aquaLeftX = (app.width-fullWidth) // 2
    imageLeftX = aquaLeftX + (2*app.cellSize)
    cy = app.height - 150 - max(imageHeight//2, 50)

    canvas.create_image(aquaLeftX, cy, anchor="w",
                            image=ImageTk.PhotoImage(app.aquaImg))
    canvas.create_image(imageLeftX, cy, anchor="w",
                            image=ImageTk.PhotoImage(image))

def chooseCutscene(app, character):
    ''' return the dialogue and character image corresponding to a cutscene '''
    if character == "Giang":
        return giangDialogue(), app.giangImg
    elif character == "Iara":
        return iaraDialogue(app), app.iaraImg
    elif character == "Kai":
        return kaiDialogue(), app.kaiImg
    elif character == "Marina":
        return marinaDialogue(), app.marinaImg
    elif character == "Morgan":
        return morganDialogue(), app.morganImg
    elif character == "Naia":
        return naiaDialogue(app), app.naiaImg
    elif character == "Walter":
        return walterDialogue(), app.walterImg
    else: # ending scene
        return endDialogue(app), app.nerissaImg

def giangDialogue():
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

def kaiDialogue():
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

def marinaDialogue():
    ''' return Marina's cutscene dialogue '''
    marinaIntro = [
        '''Such a pretty castle! And so big! Hey, you! It's nice to meet you!
>>''',
        '''You can call me Marina! She/her! I'm here to help fill the Moat!
>>''',
        "You're doing that too? Wow! I'm glad I came to the right place!"
    ]
    return marinaIntro

def morganDialogue():
    ''' return Morgan's cutscene dialogue '''
    morganIntro = [
        '''...
>>''',
        '''......
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

def walterDialogue():
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
>>''',
        '''I heard from Anna how dedicated everyone was. It's all thanks to you!
>>''',
        '''Now that the Moat is full, we can win the Surf War!
>>''',
        f'''I hope that you have a great summer, {app.aqua.name}. You've earned
it!'''
    ]
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
    
    if app.tutorial:
        drawTutorialBarracks(app, canvas)

def drawTutorialBarracks(app, canvas):
    ''' draw the prompt in barracks mode during the tutorial '''
    allDialogue = tutorialBarracksDialogue()

    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, "Anna", allDialogue[app.onCutsceneLine])

def tutorialBarracksDialogue():
    ''' return the tutorial barracks dialogue '''
    barracksIntro = [
        '''Welcome to the barracks! You can click on a unit and use the arrow
keys to change the order of the team. A team has up to 3 members.
>>''',
        '''Once you meet more people, you can click on a unit and press Enter
to change which units you take into battle.
>>''',
        '''Also, if you press S when you're in the Transition menu, you can
save your game.
>>''',
        "Alright, now you're ready to fight!"
    ]
    return barracksIntro

def drawStatus(app, canvas, unit, topY, slotNum=-1):
    ''' draw a unit's status bar '''
    botY = topY + (app.height//5)

    # outline selected units in red
    if app.selected == slotNum:
        outlineColor = "red"
    else:
        outlineColor = "black"
    canvas.create_rectangle(0, topY, app.width, botY,
                                fill=app.buttonColor, outline=outlineColor)

    # draw unit name and icon
    canvas.create_text(app.margin, botY - app.margin, anchor="sw",
                    text=unit.name, font=app.dialogueFont+" bold")
    cx = app.margin + (app.cellSize // 2)
    cy = cx + topY
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(unit.image))

    offset = (2 * app.margin) + app.cellSize
    drawStats(app, canvas, unit, offset, topY)
    drawHPBar(app, canvas, unit, offset, topY + 25,
                        app.width - app.margin - offset, app.dialogueFont)

def drawStats(app, canvas, unit, offset, topY):
    ''' draw a unit's stats in a status bar '''
    # draw unit information
    canvas.create_text(offset, topY + app.margin, text=f"Level {unit.level}",
                        anchor="nw", font=app.dialogueFont)
    stats = f'''Attack {unit.attack}
Def {unit.defense}      Res {unit.res}'''
    canvas.create_text(offset, topY + 60, text=stats, anchor="nw",
                        font=app.dialogueFont)

    # draw weapon information
    canvas.create_text(offset * 4, topY + app.margin, text=unit.weapon.title(),
                        anchor="nw", font=app.dialogueFont)
    weaponInfo = f"Range {unit.range}"
    if unit.weapon == "bubble wand":
        weaponInfo += "\nTargets Res"
        weaponInfo += "\nCan heal allies two spaces away"
    else:
        weaponInfo += "\nTargets Def"
    canvas.create_text(app.width - (3*app.margin), topY + 60, text=weaponInfo,
                        anchor="ne", font=app.dialogueFont, justify="right")

def drawHPBar(app, canvas, unit, topX, topY, barLength, font):
    ''' draw a unit's HP bar '''
    canvas.create_text(topX, topY, text=f"HP: {unit.hp} / {unit.maxHP}",
                        anchor="nw", font=font)

    # draw bar below text
    filled = unit.hp / unit.maxHP
    fillLength = int(barLength * filled)
    canvas.create_rectangle(topX, topY + 20, topX + barLength, topY + 30,
                                fill="black")
    canvas.create_rectangle(topX, topY + 20, topX + fillLength, topY + 30,
                                fill="green", width=0)

def teamSelectionMode_redrawAll(app, canvas):
    ''' draw the current found units in the team selection screen '''
    drawBackButton(app, canvas, app.margin, app.margin)

    gridOffsetY = (app.height - (2*app.height//10)) // 2

    # draw unit icons in a grid (up to 2 x 4)
    for unitNum in range(len(app.barracks)):
        topX = (app.width//4) * (unitNum%4)
        topY = gridOffsetY + ((app.height//10) * (unitNum//4))
        unit = app.barracks[unitNum]
        drawUnitSummary(app, canvas, unit, topX, topY)

def drawUnitSummary(app, canvas, unit, topX, topY):
    ''' draw a unit's abbreviated status bar '''
    botX = topX + (app.width//4)
    botY = topY + (app.height//10)

    canvas.create_rectangle(topX, topY, botX, botY, fill=app.buttonColor)

    # draw unit name and icon
    canvas.create_text(app.margin + topX, botY - app.margin, anchor="sw",
                    text=unit.name, font=app.summaryFont)
    canvas.create_image(topX, topY, anchor="nw",
                            image=ImageTk.PhotoImage(unit.image))

    # draw HP and weapon
    offset = (2 * app.margin) + app.cellSize + topX
    barLength = botX - offset - app.margin
    drawHPBar(app, canvas, unit, offset, topY + app.margin,
                    barLength, app.summaryFont)
    
    canvas.create_text(offset, topY + 35 + app.margin, text=unit.weapon,
                        anchor="nw", font=app.summaryFont)

####
# Battle drawing functions
####

def battleMode_redrawAll(app, canvas):
    ''' draw the battle screen '''
    tutorialLines = 5
    drawMap(app, canvas)
    drawUnitsOnMap(app, canvas)
    
    # display victory or defeat message
    if app.victory or app.defeat:
        drawEndOfBattle(app, canvas)
    
    # draw status bar of selected unit
    elif app.selected != None:
        unit = app.team[app.selected]
        drawStatus(app, canvas, unit, 0)
        if unit.canMove:
            drawMoveRadius(app, canvas, unit)
    
    # display player menu and tutorial dialogue
    else:
        if app.tutorial and app.onCutsceneLine < tutorialLines:
            drawTutorialBattleIntro(app, canvas)
        displayBattleMenu(app, canvas)
        drawClickInstructions(app, canvas)
    
    if app.battleMessage != None:
        if app.tutorial and app.onCutsceneLine < tutorialLines:
            return
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

def drawEndOfBattle(app, canvas):
    ''' draw the end-of-battle message '''
    if app.victory:
        color = "#4fb861"
    else: # app.defeat
        color = "#b62c2c"
    
    drawButton(app, canvas, 0, 0, app.width, app.height // 5,
                color=color, text=app.endOfBattleMessage)

def drawTutorialBattleIntro(app, canvas):
    ''' draw the introduction to battle mode during the tutorial '''
    allDialogue = battleIntroDialogue(app)
    
    if app.onCutsceneLine < len(allDialogue):
        drawDialogueBox(app, canvas, "Anna", allDialogue[app.onCutsceneLine])

def battleIntroDialogue(app):
    ''' return Anna's dialogue during the tutorial battle '''
    enemy = app.enemyTeam[0]

    battleIntro = [
        f'''Enemies approaching! Everyone to battle stations! Even you,
{app.aqua.name}! Pick up your Pool Noodle and fight!
>>''',
        '''What are you looking so confused for? Don’t you know about the
Surf War?
>>''',
        f'''That {enemy.name} is here to steal Droplets from the Moat in front
of the Sand Castle.
>>''',
        f'''You’re right there, so why don’t you try attacking the
{enemy.name}? Click your icon and click to where you want to move.
Then attack with the correct arrow key!
>>''',
        '''You can only attack adjacent enemies with a Pool Noodle. Long-range
weapons can only attack enemies that are two spaces away. Bubble Wands can also
heal allies that are two spaces away.
>>''',
        '''At the end of your turn, don't forget to click through the play-by-
play of the enemy turn.'''
    ]

    return battleIntro

def displayBattleMenu(app, canvas):
    ''' call the function that corresponds to the correct battle menu '''
    if app.battleMenuDisplay == 0:
        drawPlayerMenu(app, canvas)

    # accessed by clicking player menu buttons
    elif app.battleMenuDisplay == 1:
        drawUntappedUnits(app, canvas)
    elif app.battleMenuDisplay == 2:
        drawBattleSummary(app, canvas)

    # only shown when a freeplay-mode save is loaded
    elif app.battleMenuDisplay == 3:
        drawFreeplayIntro(app, canvas)

def drawPlayerMenu(app, canvas):
    ''' draw a player's menu options in battle mode '''
    fullHeight = (app.height//5) - (2*app.margin)
    buttonWidth = app.width // 6
    buttonHeight = fullHeight // 3

    canvas.create_rectangle(0, 0, app.width, app.height // 5,
                                fill=app.buttonColor)

    if app.tutorial: # inactive buttons
        color = "gray"
    else:
        color = "white"

    # draw buttons in a 2 x 2 grid
    drawButton(app, canvas, buttonWidth, app.margin, 2 * buttonWidth,
                app.margin + buttonHeight, color=color, text="Flee")
    drawButton(app, canvas, buttonWidth, app.margin + (2*buttonHeight),
                2 * buttonWidth, app.margin + (3*buttonHeight),
                color=color, text="End turn")
    drawButton(app, canvas, 3 * buttonWidth, app.margin, 5 * buttonWidth,
                app.margin + buttonHeight,
                color=color, text="Show untapped units")
    drawButton(app, canvas, 3 * buttonWidth, app.margin + (2*buttonHeight),
                5 * buttonWidth, app.margin + (3*buttonHeight),
                color=color, text="Show HP summary")

def drawUntappedUnits(app, canvas):
    ''' draw summaries for ever untapped team member '''
    canvas.create_rectangle(0, 0, app.width, app.height // 5,
                                fill=app.buttonColor)

    # determine untapped units
    untappedUnits = []
    for unit in app.team:
        if unit.untapped or unit.canMove:
            untappedUnits.append(unit)

    # draw unit summaries in a row
    offsetX = app.width // 16
    for unitNum in range(len(untappedUnits)):
        topX = (offsetX * (unitNum+1)) + ((app.width//4) * unitNum)
        topY = app.height // 20
        unit = untappedUnits[unitNum]
        drawUnitSummary(app, canvas, unit, topX, topY)

def drawBattleSummary(app, canvas):
    ''' draw summaries for every living unit on the map '''
    canvas.create_rectangle(0, 0, app.width, app.height // 5,
                                fill=app.buttonColor)

    # determine living units
    livingUnits = []
    for unit in app.team:
        if unit.hp != 0:
            livingUnits.append(unit)
    for enemy in app.enemyTeam:
        if enemy.hp != 0:
            livingUnits.append(enemy)

    # draw unit summaries in a grid (up to 2 x 4)
    for unitNum in range(len(livingUnits)):
        topX = (app.width//4) * (unitNum%4)
        topY = (app.height//10) * (unitNum//4)
        unit = livingUnits[unitNum]
        drawUnitSummary(app, canvas, unit, topX, topY)

def drawFreeplayIntro(app, canvas):
    ''' draw the introduction to freeplay mode '''
    freeplayIntro = '''Now that the Moat is full, we can let loose, but we
can’t rest easy yet! Keep defending the Sand Castle from enemies!'''
    drawDialogueBox(app, canvas, "Anna", freeplayIntro, "top")

def drawClickInstructions(app, canvas):
    ''' draw the prompt for the player to click during battles '''
    if app.playerTurn:
        prompt = '''Click to select a unit.
Then click to move or press Enter to wait.'''
    else:
        prompt = "Click to move through the enemy turn."
    
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))
    cy = ((app.height//5) + mapOffsetY) // 2

    canvas.create_text(app.width // 2, cy, text=prompt, font=app.dialogueFont,
                                                justify="center")

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

def moveIsLegal(app, currRow, currCol, drow, dcol, isPlayer=True):
    ''' return True if a unit can legally move in direction drow,dcol '''
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
    if newRow < 0 or newRow >= len(app.map): return False
    elif newCol < 0 or newCol >= len(app.map[0]): return False

    # water and moats cannot be walked onto
    elif app.map[newRow][newCol] == "X": return False

    if obstacleInTheWay(app, currRow, currCol, drow, dcol, isPlayer):
        return False

    return True

def obstacleInTheWay(app, currRow, currCol, drow, dcol, isPlayer=True):
    ''' return True if a 1-cell move is illegal before a 2-cell move '''
    # 1-cell moves and diagonal moves have no obstacles
    if abs(drow) == 1 or abs(dcol) == 1:
        return False

    newRow = currRow + (drow//2)
    newCol = currCol + (dcol//2)
    
    # check that newRow,newCol is not occupied by a unit on the opposite team
    if not isPlayer:
        for unit in app.team:
            if unit.row == newRow and unit.col == newCol:
                return True
    else:
        for enemy in app.enemyTeam:
            if enemy.row == newRow and enemy.col == newCol:
                return True

    # water and moats cannot be walked onto
    if app.map[newRow][newCol] == "X":
        return True

    return False

def drawMoveRadius(app, canvas, unit):
    ''' draw rectangles around a unit's possible move locations '''
    mapOffsetX = (app.width - (2*app.margin) - (7*app.cellSize)) // 2
    mapOffsetY = ((app.height*4//5) - (2*app.margin) - (7*app.cellSize))

    # units can move up to 2 squares per turn
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1),
                    (0, 2), (2, 0), (0, -2), (-2, 0)]

    isPlayer = isinstance(unit, PlayableChar)
    for drow,dcol in directions:
        if moveIsLegal(app, unit.row, unit.col, drow, dcol, isPlayer):
            newRow = unit.row + drow
            newCol = unit.col + dcol
            topX = mapOffsetX + (app.cellSize * newCol)
            topY = mapOffsetY + (app.cellSize * newRow)
            canvas.create_rectangle(topX, topY, topX + app.cellSize,
                                    topY + app.cellSize, outline="blue",
                                    width=3)