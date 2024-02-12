# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
from config import WINDOWHEIGHT, WINDOWWIDTH
from config import WHITE,BLACK, RED, GREEN, DARKGREEN,DARKGRAY, BLUE,YELLOW
from config import UP, DOWN, LEFT, RIGHT

FPS = 5
HEAD = 0 # syntactic sugar: index of the worm's head
BLUE_APPLE_TIMER = 5
SECOND_SNAKE_INTERVAL = 5
FPS_STEP_INTERVAL = 5
SPAWN_SECOND = False
SCORE = 0
SPEED_CHANGE = 2
CELLSIZE = 25
BGCOLOR = BLACK
X=0
Y=0
PLAYING = True

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)


def showMenu():
    global PLAYING
    while PLAYING:
        DISPLAYSURF.fill(BGCOLOR)
        
        font = pygame.font.Font(None, 36)
        text_go = font.render("Game Over", True, WHITE)
        text_score = font.render("Score: " + str(SCORE), True, WHITE)
        text_quit = font.render("Quit", True, WHITE)
        text_continue = font.render("Try again", True, WHITE)
        
        go_rect = text_go.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 100))
        score_rect = text_score.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50))
        quit_rect = text_quit.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50))
        continue_rect = text_continue.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 100))

        DISPLAYSURF.blit(text_go, go_rect)
        DISPLAYSURF.blit(text_score, score_rect)
        DISPLAYSURF.blit(text_quit, quit_rect)
        DISPLAYSURF.blit(text_continue, continue_rect)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if quit_rect.collidepoint(mousex, mousey):
                    terminate()
                elif continue_rect.collidepoint(mousex, mousey):
                    return

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main(x,y,score):
    global PLAYING
    PLAYING = True
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, OLD_SECONDS, SPAWN_SECOND, SCORE

    SCORE = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while PLAYING:
        runGame()
        score += SCORE
        #Change 1
        FPS = 5
        OLD_SECONDS = 0
        SPAWN_SECOND = False
        pygame.time.delay(100)
        showGameOverScreen()
        showMenu()
    return x, y, score


def runGame():
    global FPS, OLD_SECONDS, BLUE_APPLE_TIMER, BLUE_SECONDS, SECOND_SNAKE_INTERVAL, FPS_STEP_INTERVAL, SPAWN_SECOND, SCORE
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    
    secondWormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    
    direction = RIGHT

    secondDirection = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    #Change 2
    blue_apple = getRandomLocation()
    while blue_apple == apple:
        blue_apple = getRandomLocation()

    #Change 3
    yellow_apple = getRandomLocation()
    while yellow_apple == apple and yellow_apple == blue_apple:
        yellow_apple = getRandomLocation()

    #Change 1
    start_ticks = pygame.time.get_ticks()
    OLD_SECONDS = 0
    BLUE_SECONDS = 0
    
    YELLOWINTERVAL = 7
    showYellowAppple = False
    showBlueApple = False
    decrease_og = True
    decrease_second = True
    blink = False
    bblink = False
    while PLAYING: # main game loop
        #Change 1
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds - OLD_SECONDS > FPS_STEP_INTERVAL:
            FPS = FPS + SPEED_CHANGE
            print(str(FPS))
            OLD_SECONDS = seconds

        if seconds > YELLOWINTERVAL:
            showYellowAppple = True
        if seconds > 2*YELLOWINTERVAL:
            showYellowAppple = False
            yellow_apple = {'x': -1, 'y': -1}

        if seconds > SECOND_SNAKE_INTERVAL:
            #spawn second snake
            SPAWN_SECOND = True
        #Change 2
        if seconds - BLUE_SECONDS > BLUE_APPLE_TIMER:
            showBlueApple = not showBlueApple
            if showBlueApple:
                blue_apple = getRandomLocation()
                while blue_apple == apple:
                    blue_apple = getRandomLocation()
            else:
                blue_apple = {'x': -1, 'y': -1}
            BLUE_SECONDS = seconds


        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        while True:
            rnd = random.randint(1,4)
            if (rnd == 1) and secondDirection != RIGHT:
                secondDirection = LEFT
            elif (rnd == 2) and secondDirection != LEFT:
                secondDirection = RIGHT
            elif (rnd == 3) and secondDirection != DOWN:
                secondDirection = UP
            elif (rnd == 4) and secondDirection != UP:
                secondDirection = DOWN
            for wormBody in secondWormCoords[1:]:
                if wormBody['x'] == secondWormCoords[HEAD]['x'] and wormBody['y'] == secondWormCoords[HEAD]['y']:
                    continue
            if (secondWormCoords[HEAD]['x'] == 0 and secondDirection==LEFT) or (secondWormCoords[HEAD]['x'] == CELLWIDTH-1 and secondDirection==RIGHT) or (secondWormCoords[HEAD]['y'] == 0 and secondDirection==UP) or (secondWormCoords[HEAD]['y'] == CELLHEIGHT-1 and secondDirection==DOWN):
                continue
            else:
                break

            
        
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        #case koga og udril vo vtoriot bilo kade including glavata
        decrease_og = True
        if SPAWN_SECOND:
            for wormBody in secondWormCoords[0:]:
                if wormCoords[HEAD]['x'] == wormBody['x'] and wormCoords[HEAD]['y'] == wormBody['y']:
                    decrease_og = False
                    print("najdov")
                    break


        decrease_second = True
        if SPAWN_SECOND:
            for wormBody in wormCoords[0:]:
                if secondWormCoords[HEAD]['x'] == wormBody['x'] and secondWormCoords[HEAD]['y'] == wormBody['y']:
                    decrease_second = False
                    print("ME NAJDE")
                    break
                    
        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            SCORE+= 1
        #Change 2
        elif wormCoords[HEAD]['x'] == blue_apple['x'] and wormCoords[HEAD]['y'] == blue_apple['y']:
            blue_apple = getRandomLocation()
            while blue_apple == apple:
                blue_apple = getRandomLocation()
            FPS = FPS - SPEED_CHANGE
            SCORE += 3
            BLUE_SECONDS = seconds
        #Change 3
        elif wormCoords[HEAD]['x'] == yellow_apple['x'] and wormCoords[HEAD]['y'] == yellow_apple['y']:
            SCORE += 3
            print(SCORE)
            showYellowAppple = False
            yellow_apple = {'x': -1, 'y': -1}
        else:
            if decrease_og:
                del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        if secondDirection == UP:
            secondNewHead = {'x': secondWormCoords[HEAD]['x'], 'y': secondWormCoords[HEAD]['y'] - 1}
        elif secondDirection == DOWN:
            secondNewHead = {'x': secondWormCoords[HEAD]['x'], 'y': secondWormCoords[HEAD]['y'] + 1}
        elif secondDirection == LEFT:
            secondNewHead = {'x': secondWormCoords[HEAD]['x'] - 1, 'y': secondWormCoords[HEAD]['y']}
        elif secondDirection == RIGHT:
            secondNewHead = {'x': secondWormCoords[HEAD]['x'] + 1, 'y': secondWormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        secondWormCoords.insert(0, secondNewHead)
        if decrease_second:
            del secondWormCoords[-1]
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        if SPAWN_SECOND:
            drawWorm(secondWormCoords, RED)
        drawApple(apple)
        if showYellowAppple:
            if blink:
                drawApple(yellow_apple, YELLOW)
            else:
                drawApple(yellow_apple, BLACK)
            blink = not blink
        
        if bblink:
            drawApple(blue_apple, BLUE)
        else:
            drawApple(blue_apple, BLACK)
        bblink = not bblink
        
        drawScore(SCORE)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    global PLAYING
    PLAYING = False


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global SCORE
    SCORE = 0
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, color = GREEN):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)


def drawApple(coord, color = RED):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main(X,Y,SCORE)
