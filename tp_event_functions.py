####
# Name: Isabella Yee
# andrewID: iby
####

from cmu_112_graphics import *

####
# Startup (main screen) functions
####

def appStarted(app):
    # define size constants
    app.margin = 5 # change later
    app.cellSize = 50
    app.mapOffset = 0 # change later

    # set up collections
    app.barracks = set()
    app.team = []
    app.items = set()
    app.droplets = app.seashells = 0
    app.moatSize = 25

    # define game colors and fonts
    app.borderColor = "blue"
    app.buttonColor = "blue"
    app.textColor = "black"
    app.buttonFont = "Arial 12 bold"
    app.dialogueFont = "Arial 14 bold"

    # define game/menu modes (replace with cmu_graphics modes later)
    app.mainScreen = True
    app.tutorial = True
    app.freeplay = False
    app.inBarracks = False
    app.inBetween = False
    app.inBattle = False
    app.inGacha = False

def keyPressed(app, event):
    pass

####
# Tutorial functions
####

####
# Transition screen functions
####

####
# Battle screen functions
####

####
# Gacha screen functions
####