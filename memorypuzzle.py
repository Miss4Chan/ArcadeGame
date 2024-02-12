# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys #sys e za runtime environment 
from pygame.locals import *
from config import FPS, WINDOWHEIGHT, WINDOWWIDTH
from config import GRAY, NAVYBLUE, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN
from config import DONUT, SQUARE, DIAMOND, LINES, OVAL


REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
##Staveni se tuka mali brojchinja za polesno testiraje
BOARDWIDTH = 3 # number of columns of icons
BOARDHEIGHT = 2 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
SCORE = 0 
X = 0
Y = 0

#immutable
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

#avoid crashes ;)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."
#Think of assert poishe kako requirement ideata tuka e da mozhe da se napravat dovolno 
#unique combinacii to est dali so brojot na boi/shapes * 2 mozhe da se popolni tablata (at least enough)

PLAYING = True

def main(x, y, score):
    global PLAYING
    PLAYING = True
    if PLAYING:
        global FPSCLOCK, DISPLAYSURF
        pygame.init()

        #defined once pred da pochne loopot
        FPSCLOCK = pygame.time.Clock()
        #surface area kaj shto se grafikite i elementite 
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event
        pygame.display.set_caption('Memory Game')

        mainBoard = getRandomizedBoard()
        revealedBoxes = generateRevealedBoxesData(False)

        firstSelection = None # stores the (x, y) of the first box clicked.

        DISPLAYSURF.fill(BGCOLOR)
        startGameAnimation(mainBoard)
        possible_moves = BOARDHEIGHT*BOARDWIDTH+(BOARDHEIGHT*BOARDWIDTH)/3
        while PLAYING: # main game loop
            mouseClicked = False
            DISPLAYSURF.fill(BGCOLOR) # drawing the window
            drawBoard(mainBoard, revealedBoxes)
            displayPossibleMoves(possible_moves)
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    PLAYING = False
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
                ##aj da vidime bash
                elif event.type == K_g:
                   PLAYING = False
            

            boxx, boxy = getBoxAtPixel(mousex, mousey)

            if boxx != None and boxy != None:
                # The mouse is currently over a box.
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                    if firstSelection == None: # the current box was the first box clicked
                        firstSelection = (boxx, boxy)
                    else: # the current box was the second box clicked
                        # Check if there is a match between the two icons.

                        #promena
                        possible_moves -= 1

                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # Icons don't match. Re-cover up both selections.
                            pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False

                            if possible_moves == 0:
                                mainBoard = getRandomizedBoard()
                                revealedBoxes = generateRevealedBoxesData(False)
                                drawBoard(mainBoard, revealedBoxes)
                                possible_moves = BOARDHEIGHT*BOARDWIDTH+(BOARDHEIGHT*BOARDWIDTH)/3
                                pygame.display.update()
                                pygame.time.wait(1000)
                                startGameAnimation(mainBoard)

                        elif hasWon(revealedBoxes): # check if all pairs found
                            gameWonAnimation(mainBoard)
                            bling(BGCOLOR)
                            pygame.time.wait(2000)
                            # Reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)

                            # Show the fully unrevealed board for a second.
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            possible_moves = BOARDHEIGHT*BOARDWIDTH+(BOARDHEIGHT*BOARDWIDTH)/3
                            # Replay the start game animation.
                            startGameAnimation(mainBoard)
                        firstSelection = None # reset firstSelection variable

            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    return x,y, score

def displayPossibleMoves(possible_moves):
    font =pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f"Possible Moves: {possible_moves}", True, WHITE)
    textRect = text.get_rect()
    textRect.topleft = (10, 10)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()

#pravi lista od listi so boolean za dali treba da se pokazhat polinjata
#inicijalno site se false
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

#lista od listi od (color,shape) 
def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons) # randomize the order of the icons list

    #broj na potrebni sliki
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result



#pomoshni funkcii -- reuse this za selection :)))
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)



def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            #RectValue -- (where the rect appears and whats its size) - X, Y, Width, Height == x,y - gorno desno kjoshe, shirina , visina
            #se crta od levo na desno 
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left+BOXSIZE-coverage, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)



COLOR1 =  (255, 182, 193)
COLOR2 = (128, 0, 128)
COLORS = (COLOR1,COLOR2)    
#tuka treba da se napravi izmena --  funkcija koja shto pravi site polinja da trepkaat

#Направете измена во анимацијата што се појавува кога играчот успешно ќе ги отвори сите полиња така 
#што ќе се појават квадрати околу секое поле и ќе се менува нивната боја во две бои по ваш избор. 
def bling(border_color):
    for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                    #za sekoja zemi gi pochetnite koordinati i nacrtaj okolu niv (-2/+2) so chosen border_color
                    left, top = leftTopCoordsOfBox(x,y)
                    pygame.draw.rect(DISPLAYSURF, border_color, (left-2, top-2, BOXSIZE+2, BOXSIZE+2), 3)

def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    
    for i in range(4):
        border_color = COLORS[i % 2]
        bling(border_color)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(100)
        pygame.display.update()
    

def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main(X, Y, SCORE)