# draw a board

import random, sys, pygame
from pygame.locals import *

# There are different box sizes, number of boxes, and
# life depending on the "board size" setting selected.
SIZE_MULTI = 1.7

SMALLBOXSIZE  = int(60 * SIZE_MULTI)  # size is in pixels
MEDIUMBOXSIZE = int(20 * SIZE_MULTI)
LARGEBOXSIZE  = int(11 * SIZE_MULTI)

SMALLBOARDSIZE  = int(6 * SIZE_MULTI) # size is in boxes
MEDIUMBOARDSIZE = int(17 * SIZE_MULTI)
LARGEBOARDSIZE  = int(30 * SIZE_MULTI)

SMALLMAXLIFE  = 10 # number of turns
MEDIUMMAXLIFE = int(30 * SIZE_MULTI)
LARGEMAXLIFE  = int(64 * SIZE_MULTI) 

FPS = 30
WINDOWWIDTH = int(640 * SIZE_MULTI)
WINDOWHEIGHT = int(720 * SIZE_MULTI)
boxSize = MEDIUMBOXSIZE
pegGAPSIZE = int(10 * SIZE_MULTI)
pegSIZE = int(45 * SIZE_MULTI)
EASY = 0   # arbitrary but unique value
MEDIUM = 1 # arbitrary but unique value
HARD = 2   # arbitrary but unique value

difficulty = MEDIUM # game starts in "medium" mode
maxLife = MEDIUMMAXLIFE
boardWidth = MEDIUMBOARDSIZE
boardHeight = MEDIUMBOARDSIZE

#            R    G    B
WHITE    = (255, 255, 255)
DARKGRAY = ( 70,  70,  70)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)

bgColor = (200, 200, 200) 

pegColors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE)

print("debug one")


def main():
    print("debug 2")
    global FPSCLOCK, DISPLAYSURF, LOGOIMAGE, SPOTIMAGE, SETTINGSIMAGE, SETTINGSBUTTONIMAGE, RESETBUTTONIMAGE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Draw Board')
    print("debug 3")

    while True: # main game loop
        pegClicked = None
        resetGame = False

        # Draw the screen.
        DISPLAYSURF.fill(bgColor)
        drawpegs()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        checkForQuit()
        # events

        pygame.display.update()

def checkForQuit():
    # Terminates the program if there are any QUIT or escape key events.
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit() # terminate if any QUIT events are present
        sys.exit()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit() # terminate if the KEYUP event was for the Esc key
            sys.exit()
        pygame.event.post(event) # put the other KEYUP event objects back

def drawpegs():
    # Draws the six color pegs at the bottom of the screen.
    numColors = len(pegColors)
    xmargin = int((WINDOWWIDTH - ((pegSIZE * numColors) + (pegGAPSIZE * (numColors - 1)))) / 2)
    for i in range(numColors):
        left = xmargin + (i * pegSIZE) + (i * pegGAPSIZE)
        top = WINDOWHEIGHT - pegSIZE - 10
        pygame.draw.rect(DISPLAYSURF, pegColors[i], (left, top, pegSIZE, pegSIZE))
        pygame.draw.rect(DISPLAYSURF, bgColor,   (left + 2, top + 2, pegSIZE - 4, pegSIZE - 4), 2)
 
if __name__ == '__main__':
    main()
