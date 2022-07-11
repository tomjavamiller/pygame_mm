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
MARGEN_LEFT   = 100
MARGEN_TOP    = 20

pegGAPSIZE = int(10 * SIZE_MULTI)
pegSIZE = int(45 * SIZE_MULTI)
ROW_SIZE = int(53 * SIZE_MULTI)

EASY = 0   # arbitrary but unique value
MEDIUM = 1 # arbitrary but unique value
HARD = 2   # arbitrary but unique value

difficulty = MEDIUM # game starts in "medium" mode
maxLife = MEDIUMMAXLIFE
boardWidth = MEDIUMBOARDSIZE
boardHeight = MEDIUMBOARDSIZE

numRows = 12
numPgPerRow = 5

#            R    G    B
WHITE    = (255, 255, 255)
DARKGRAY = ( 70,  70,  70)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (138,  43, 226)
BTGREEN  = (204, 255,   0)

bgColor  = (200, 200, 200)
rowBgColor=(160, 160, 160)
#rowBgCSel=(160, 160, 160)
checkColor=(180, 180, 180)

pegColors = (bgColor, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, BTGREEN, BLACK, WHITE)
pegColorStrs = ("00", "RD", "GR", "BL", "YW", "OR", "PR", "BG", "BK", "WH")


def main():
    global FPSCLOCK, DISPLAYSURF, LOGOIMAGE, SPOTIMAGE, SETTINGSIMAGE, SETTINGSBUTTONIMAGE, RESETBUTTONIMAGE, A_GUESS
    global currRow, currPos

    currRow=0
    currPos=0

    A_GUESS = [0, 0, 0, 0, 0]

    # create the blank board
    #   --------------------------
    # # | 0  1 ... numPgPerRow-1 |  numRows-1
    # .
    # .
    #
    # 3 | 0  1 ... numPgPerRow-1 |
    # 2 | 0  1 ... numPgPerRow-1 |
    # 1 | 0  1 ... numPgPerRow-1 |
    # 0 | 0  1 ... numPgPerRow-1 |
    #   --------------------------

    theBoard = [ [0]*numPgPerRow for _ in range(numRows)]

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Draw Board')
    life = maxLife
    lastPaletteClicked = None

    mousex = 0
    mousey = 0

    DISPLAYSURF.fill(bgColor)
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    #text_surface, rect = font.render("Hello World!", (0, 0, 0))

    drawBoard(theBoard)

    while True: # main game loop
        pegClicked = None
        rowPosClicked = None
        resetGame = False

        # Draw the screen.
        # DISPLAYSURF.fill(bgColor)
        drawColorChoices()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        checkForQuit()
        # events
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # check if a palette button was clicked
                pegClicked = getColorOfPaletteAt(mousex, mousey)

                # check if in current row
                if pegClicked == None:
                    rowPosClicked = getPossitionClicked(mousex, mousey)

            elif event.type == KEYDOWN:
                # support up to 9 palette keys
                try:
                    key = int(event.unicode)
                except:
                    key = None

                if key != None and key > 0 and key <= len(pegColors):
                    pegClicked = key - 1

        if pegClicked != None:  # and pegClicked != lastPaletteClicked:
            # a palette button was clicked that is different from the
            # last palette button clicked (this check prevents the player
            # from accidentally clicking the same palette twice)
            lastPaletteClicked = pegClicked

            theBoard[currRow][currPos] = pegClicked
            currPos = (currPos + 1) % numPgPerRow
            drawBoard(theBoard)
            #A_GUESS = A_GUESS[1:len(A_GUESS)] + [pegClicked]
            #drawOneGuess([150,150], A_GUESS)

            #floodAnimation(mainBoard, pegClicked)
            life -= 1

            resetGame = False
            # if hasWon(mainBoard):
            #     for i in range(4): # flash border 4 times
            #         flashBorderAnimation(WHITE, mainBoard)
            #     resetGame = True
            #     pygame.time.wait(2000) # pause so the player can bask in victory
            # elif life == 0:
            #     # life is zero, so player has lost
            #     drawLifeMeter(0)
            #     pygame.display.update()
            #     pygame.time.wait(400)
            #     for i in range(4):
            #         flashBorderAnimation(BLACK, mainBoard)
            #     resetGame = True
            #     pygame.time.wait(2000) # pause so the player can suffer in their defeat
        elif rowPosClicked != None:
            if rowPosClicked == numPgPerRow:
               # grade row
               currRow += 1
               currPos = 0
            else:
               currPos = rowPosClicked
            drawBoard(theBoard)

        if resetGame:
            # start a new game
            mainBoard = generateRandomBoard(boardWidth, boardHeight, difficulty)
            life = maxLife
            lastPaletteClicked = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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

def drawPeg(pos, color, size=40):
    pygame.draw.circle(DISPLAYSURF, color, pos, size)
    # for i in range(1,size):
    #    wvalue = int(i*250/size)
    #    pygame.draw.circle(DISPLAYSURF, (max(wvalue,color[0]),max(wvalue,color[1]),max(wvalue,color[2])), pos, size-i )

def drawTry(tryNum):
    # Draws one guessLine
    top = WINDOWHEIGHT - 2 * pegSIZE - 10
    left = 70 # + (i * pegSIZE) + (i * pegGAPSIZE)
    pygame.draw.circle(DISPLAYSURF, pegColors[tryNum], [left, top], 40 )
    #pygame.draw.rect(DISPLAYSURF, pegColors[i], (left, top, pegSIZE, pegSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def drawBoard(theBoard):
    """ Draws the main board from the matrix of ints
        :param theBoard is a 2 dim array of ints
    """
    end = len(theBoard) - 1
    for i in range(end+1):
       drawOneGuess([MARGEN_LEFT, MARGEN_TOP + (i*ROW_SIZE)], theBoard[end - i], (end - i) == currRow) # 0 at the bottom

def drawOneGuess(pos, pegsIdx, isCurrRow):
    """ Draws one sequence of pegsIdx (or blank space)
       Print a box around ~5 pegsIdx  -------------
                                      | * * * * * |

       :param pos: [left, top] where to put on screen
       :param pegsIdx: five ints. 5 peg color array offsets in pegColors
    """
    #print("-------------------")
    #print("| ", end="")
    #for i in range(len(pegsIdx)):
    #   print(pegColorStrs[pegsIdx[i]], end=" ")
    #print(" |")
    #print("-------------------")
    if isCurrRow:
       pygame.draw.rect(DISPLAYSURF, checkColor, [pos, [int(1.2*pegSIZE)*len(pegsIdx), pegSIZE]])
    else:
       pygame.draw.rect(DISPLAYSURF, rowBgColor, [pos, [int(1.2*pegSIZE)*len(pegsIdx), pegSIZE]])
    pegGSize = 30
    pegGRec = [pos[0] + int(1.5*pegGSize), pos[1] + pegGSize + int(pegSIZE/2 - pegGSize)]
    for i in range(len(pegsIdx)):
        if pegsIdx == 0:
           drawPeg([pegGRec[0] + i * int(2.8 * pegGSize), pegGRec[1]], bgColor, pegGSize)
        else:
           drawPeg([pegGRec[0] + i * int(2.8 * pegGSize), pegGRec[1]], pegColors[pegsIdx[i]], pegGSize)
        if isCurrRow and i == currPos:
           pygame.draw.line(DISPLAYSURF, GREEN, [pos[0] + i * int(1.13*pegSIZE), pos[1] + pegSIZE -4], [pos[0] + (i + 1) * int(1.13*pegSIZE), pos[1] + pegSIZE -4], 5)
    #draw check-button if currRow
    pegGRec = [pos[0] + int(1.5*pegGSize), pos[1] + pegGSize + int(pegSIZE/2 - pegGSize)]
    if isCurrRow:
        pygame.draw.rect(DISPLAYSURF, checkColor, (pegGRec[0] + (numPgPerRow * int(1.2 * pegSIZE)), pegGRec[1] - 35, pegSIZE, pegSIZE))

def drawColorChoices():
    # Draws the colors choices at the bottom of the screen.
    numPegs = len(pegColors)
    xmargin = int((WINDOWWIDTH - ((pegSIZE * numPegs) + (pegGAPSIZE * (numPegs - 1)))) / 2)
    for i in range(numPegs):
        left = xmargin + (i * pegSIZE) + (i * pegGAPSIZE)
        top = WINDOWHEIGHT - pegSIZE - 10
        pygame.draw.rect(DISPLAYSURF, pegColors[i], (left, top, pegSIZE, pegSIZE))
        pygame.draw.rect(DISPLAYSURF, bgColor,   (left + 2, top + 2, pegSIZE - 4, pegSIZE - 4), 2)

def getColorOfPaletteAt(x, y):
    # Returns the index of the color in pegColors that the x and y parameters
    # are over. Returns None if x and y are not over any palette.
    numColors = len(pegColors)
    xmargin = int((WINDOWWIDTH - ((pegSIZE * numColors) + (pegGAPSIZE * (numColors - 1)))) / 2)
    top = WINDOWHEIGHT - pegSIZE - 10
    for i in range(numColors):
        # Find out if the mouse click is inside any of the palettes.
        left = xmargin + (i * pegSIZE) + (i * pegGAPSIZE)
        r = pygame.Rect(left, top, pegSIZE, pegSIZE)
        if r.collidepoint(x, y):
            return i
    return None # no palette exists at these x, y coordinates

def getPossitionClicked(x, y):
    #print(" clicked " +str(x)+ ","+str(y))
    # check if x is in Row
    top = MARGEN_TOP + ((numRows - 1 - currRow)*ROW_SIZE)
    bottom = top + ROW_SIZE
    #print(" top and bottom " +str(top)+ ","+str(bottom))
    if y < bottom and y > top:
       for i in range(numPgPerRow):
          if x > MARGEN_LEFT + i * int(1.13*pegSIZE) and x < MARGEN_LEFT + (i+1) * int(1.13*pegSIZE):
             return i
       return numPgPerRow
    return None # no palette exists at these x, y coordinates

if __name__ == '__main__':
    main()
