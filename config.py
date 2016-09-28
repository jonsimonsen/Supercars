#Global constants for pygame applications

from drawconf import *

#Game window

RES_X = 1280
RES_Y = 960
MID_X = RES_X / 2
CAPTION = 'Supercars'
#CREDITS = 'by JSI'
FONT = 'arial'
FONTSIZE = 16
BIGSIZE = 32

#Menu

MENU_X = RES_X / 2 - 150
MENU_Y = RES_Y / 2 - 150
MENU_W = 300
MENU_H = 300
MENU_HEAD_X = MENU_X + 60
MENU_HEAD_Y = MENU_Y + 10
MENU_COL_X = MENU_HEAD_X - 25
MENU_COL_Y = MENU_HEAD_Y + 10
COLSPAN = 160

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

DISPLAY_DELAY = 3   #Delay until the game window is created.
FPS = 30            #Frames per second during driving
QPS = 1.0 / 10      #FPS after finishing the race

#Other

MAX_NAMELEN = 16
DEF_NAME = 'Anonymous'
DEF_TRACK = 'BERMUDA'
MAX_SCORES = 10
SCORE_CAPT = 'High scores for '
