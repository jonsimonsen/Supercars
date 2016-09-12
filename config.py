#Global constants for pygame applications

#Game window

RES_X = 1280
RES_Y = 960
CAPTION = 'Supercars'
CREDITS = 'by JSI'
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
MENU_COL_Y = MENU_HEAD_Y + 10

#Colors

RED     = (255,  0,  0)
GREEN   = (  0,255,  0)
BLUE    = (  0,  0,255)
YELLOW  = (255,255,  0)
WHITE   = (255,255,255)
BLACK   = (  0,  0,  0)

GRAY    = (139,139,139)
LGRAY   = (199,199,199)
GOLD    = (199,147, 22)

TRANSPARENT = (0, 0, 0, 0)

#Supercar

SPEEDLIMIT = 10
WIDTH = 40
LENGTH = 50
CAR_ROTATION = 270
ROTATION_STEP = 10  #Degrees per cycle of player input

#Keys

KEYTEXT = ['turn left', 'turn right', 'thrust']
IMAGE = 0

#Animation

FPS = 30        #Frames per second during driving
QPS = 1.0 / 10  #FPS after finishing the race
