#Global constants for pygame applications

from drawconf import *

#Game window

RES_X = 1280
RES_Y = 960
CAPTION = 'Supercars'
#CREDITS = 'by JSI'
FONT = 'arial'
FONTSIZE = 16
BIGSIZE = 32

#Menu

MENU_X = RES_X / 2 - 150
MENU_Y = RES_Y / 2 - 100
MENU_W = 300
MENU_H = 200
MENU_HEAD_X = MENU_X + 75
MENU_HEAD_Y = MENU_Y + 10
MENU_COL_X = MENU_HEAD_X + 15
MENU_COL_Y = MENU_HEAD_Y + 10
COLSPAN = 80

#Keys

KEYTEXT = ['turn left', 'turn right', 'thrust']
IMAGE = 0

#Supercar

SPEEDLIMIT = 10
WIDTH = 40
LENGTH = 50
CAR_ROTATION = 180
ROTATION_STEP = 10  #Degrees per cycle of player input

#Tracks

MARK_COLOR = WHITE
MARK_WIDTH = 4
ROAD_WIDTH = 200

#Animation

FPS = 30        #Frames per second during driving
QPS = 1.0 / 10  #FPS after finishing the race
