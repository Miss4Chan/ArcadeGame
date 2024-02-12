import random, pygame #sys e za runtime environment 
from pygame.locals import *
from config import FPS, WINDOWHEIGHT, WINDOWWIDTH, BLACK, WHITE

BGCOLOR = BLACK
PLAYING = True

def main():
    global PLAYING
    PLAYING = True
    if PLAYING:
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        while PLAYING: 
            DISPLAYSURF.fill(BGCOLOR)
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    PLAYING = False
            font =pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(f"THis / GamE iS bRokEn", True, WHITE)
            textRect = text.get_rect()
            textRect.topleft = (10, 10)
            DISPLAYSURF.blit(text, textRect)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
