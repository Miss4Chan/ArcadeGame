import pygame
import sys
from pygame.locals import *
from memorypuzzle import main as memorypuzzlemain
from slidepuzzle import main as slidepuzzlemain
from simulate import main as simulatemain
from wormy import main as wormymain
from tetromino import main as tetrominomain
from broken import main as brokenmain

#import os
#print("Current Working Directory:", os.getcwd())
##for future reference -- 
# 1.each machine gives a piece of the broken one and at the end it unlocks 
# 2. add a bar in the bottom left corner 
# 3. 
#The setuppp :))
pygame.init()
from config import FPS, WINDOWHEIGHT, WINDOWWIDTH, APATH
from config import WHITE, GREEN, BLACK
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

HALF_WINWIDTH = int(WINDOWWIDTH / 2)
HALF_WINHEIGHT = int(WINDOWHEIGHT / 2)
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSCLOCK = pygame.time.Clock()
WALLBORDER = 10
MACHINE_WIDTH = 80 
MACHINE_HEIGHT = 120
DOOR_WIDTH = 120
SCORE = 0 
SCOREBOARD = pygame.Rect(595, 340, 205, 160)
CHARACTER =  pygame.image.load(APATH + "/character.png")
BROKEN_TEXT = "/╲/\༼ ʘ̆~◞ꔢ◟~ʘ̆ ༽/\╱\\"



player_start_position = (WINDOWWIDTH // 2 - 20, WINDOWHEIGHT - 100)
player = (pygame.Rect(player_start_position, (50, 70)),APATH+"/character.png") #TODO: treba da e pogolem forsure 
entrance = pygame.Rect(HALF_WINWIDTH - DOOR_WIDTH/2, WINDOWHEIGHT - 11, DOOR_WIDTH, WALLBORDER+1)

WALLS = [
    (0, 0, WINDOWWIDTH, WALLBORDER),
    (0, 0, WALLBORDER, WINDOWHEIGHT),
    (0, WINDOWHEIGHT - WALLBORDER, WINDOWWIDTH, WALLBORDER),
    (WINDOWWIDTH - WALLBORDER, 0, WALLBORDER, WINDOWHEIGHT)
]

#mislam deka touple e odgovorot za da znam koja mashina e ;')
MACHINES = [
    ##levo
    (pygame.Rect(WALLBORDER+25, 200, MACHINE_WIDTH, MACHINE_HEIGHT), "memorypuzzle"),  
    #gore
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH-10, WALLBORDER+70, MACHINE_WIDTH, MACHINE_HEIGHT),"slidepuzzle"),
    (pygame.Rect(HALF_WINWIDTH, WALLBORDER+70, MACHINE_WIDTH, MACHINE_HEIGHT),"simulate"),
    #desno -- ovaa treba da ne raboti  scriot that shows errror when interactеd
    (pygame.Rect(WINDOWWIDTH-WALLBORDER-MACHINE_WIDTH-30, 200, MACHINE_WIDTH, MACHINE_HEIGHT),BROKEN_TEXT),
    #sredina
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH-10, 300, MACHINE_WIDTH, MACHINE_HEIGHT),"wormy"),
    (pygame.Rect(HALF_WINWIDTH, 300, MACHINE_WIDTH, MACHINE_HEIGHT),"tetromino")
]


#TODO: help? - samo render mozhe na boardot jhahahaahha 
def draw_stats_board(text, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (595, 340)
    background = pygame.image.load(APATH+'/scoreboard.png')
    if "Score" in text:
        surface.blit(background,textrect)
        surface.blit(textobj, [textrect.left + 40,textrect.top+50])
    else:
        surface.blit(textobj, [textrect.left + 60,textrect.top+80])

def draw_interaction_text(text, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (500, 90)
    background = pygame.image.load(APATH+'/message.png')
    if "G" not in text:
        surface.blit(textobj, [textrect.left+30,textrect.top+20])
    else:
        surface.blit(background, [textrect.left-100, textrect.top-45])
        surface.blit(textobj, textrect)

def start_game(game_name):
    global SCORE
    if game_name == "memorypuzzle":
        print(f"Starting game: {game_name}")
        player[0].x,player[0].y, SCORE = memorypuzzlemain(player[0].x, player[0].y, SCORE)
    if game_name == "slidepuzzle":
        player[0].x,player[0].y, SCORE = slidepuzzlemain(player[0].x, player[0].y, SCORE)
    if game_name == "simulate":
        player[0].x,player[0].y, SCORE = simulatemain(player[0].x, player[0].y, SCORE)
    if game_name == "wormy":
        player[0].x,player[0].y, SCORE = wormymain(player[0].x, player[0].y, SCORE)
    if game_name == "tetromino":
        player[0].x,player[0].y, SCORE = tetrominomain(player[0].x, player[0].y, SCORE)
    if game_name == BROKEN_TEXT:
        brokenmain()



def check_proximity(player, machines, distance=20):
    for machine in machines:
        if player[0].colliderect(machine[0].inflate(distance, distance)):
            return machine
    return None


def handle_player_interaction(keys, player, machines):
    close_machine = check_proximity(player, machines)
    if close_machine and keys[K_g]:
        print("Activated machine!") 
        start_game(close_machine[1])
        pygame.event.clear() #so start game go reshavame choiceot na script
        

def draw_menu():
    SCREEN.fill((0, 0, 0))
    welcome_text = BASICFONT.render("Welcome! Press Enter to start or Escape to quit", True, WHITE)
    SCREEN.blit(welcome_text, (WINDOWWIDTH // 2 - welcome_text.get_width() // 2, WINDOWHEIGHT // 2 - welcome_text.get_height() // 2))
    pygame.display.flip()
  

def handle_player_movement(keys, player_speed=9):
    global CHARACTER

    PLAYER_R = pygame.image.load(APATH+'/character.png')
    PLAYER_L = pygame.transform.flip(PLAYER_R, True, False)

    original_x, original_y = player[0].x, player[0].y

    if keys[K_LEFT]:
        player[0].x -= player_speed
        CHARACTER = PLAYER_L
    if keys[K_RIGHT]:
        player[0].x += player_speed
        CHARACTER = PLAYER_R

    if keys[K_UP]:
        player[0].y -= player_speed
    if keys[K_DOWN]:
        player[0].y += player_speed
    
    #go vikame ova R, ako e touple za mashina ni treba od [0] ako e scoreboard samoto toa e rect 
    for r in MACHINES + [SCOREBOARD]:
        if player[0].colliderect(r[0] if isinstance(r, tuple) else r): 
            player[0].x = original_x
            break
    for r in MACHINES + [SCOREBOARD]: 
        if player[0].colliderect(r[0] if isinstance(r, tuple) else r): 
            player[0].y = original_y
            break
        
    if player[0].left <= WALLBORDER: player[0].left = WALLBORDER
    if player[0].right >= WINDOWWIDTH - WALLBORDER: player[0].right = WINDOWWIDTH - WALLBORDER
    if player[0].top <= WALLBORDER+MACHINE_HEIGHT: player[0].top = WALLBORDER + MACHINE_HEIGHT
    if player[0].bottom >= WINDOWHEIGHT - WALLBORDER: player[0].bottom = WINDOWHEIGHT - WALLBORDER




def main():
    game_state = "menu"
    # TODO:
    # pygame.display.set_icon(pygame.image.load('gameicon.png'))
    # ke go stavam ova at some point
    
    while True:
        if game_state == "menu":
            draw_menu()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        game_state = "playing"
                        player[0].left, player[0].top = player_start_position 
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        elif game_state == "playing":
            SCREEN.fill((0, 0, 0))
            for wall in WALLS:
                pygame.draw.rect(SCREEN, WHITE, wall)
            pygame.draw.rect(SCREEN, GREEN, entrance)
            img = pygame.image.load(APATH+"/bg_wall.png").convert()
            img2= pygame.image.load(APATH+"/bg_floor.png").convert()
            img3=pygame.image.load(APATH+"/bg_lights.png").convert()
            SCREEN.blit(img, (WALLBORDER, WALLBORDER+50))
            
            SCREEN.blit(img2, (WALLBORDER, WALLBORDER+150))
            SCREEN.blit(img3, (WALLBORDER, WALLBORDER))
            for machine in MACHINES:
               #Convert alpha ni treba radi pngto da e transparent ugh ;(
                if machine[1]==BROKEN_TEXT:
                    m =  pygame.image.load(APATH+"/broken_machine.png").convert_alpha()
                else:
                    m = pygame.image.load(APATH+"/machine.PNG").convert_alpha()
               
                SCREEN.blit(m, (machine[0].left, machine[0].top))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            handle_player_movement(keys)
            handle_player_interaction(keys, player, MACHINES)

            close_machine = check_proximity(player, MACHINES)
            if close_machine:
                draw_interaction_text("Press 'G' to activate ", BASICFONT, BLACK, SCREEN)
                draw_interaction_text(close_machine[1], BASICFONT, BLACK, SCREEN)

            draw_stats_board("Score:", BASICFONT, WHITE,SCREEN)
            draw_stats_board(str(SCORE), BASICFONT, WHITE,SCREEN)

            if player[0].colliderect(entrance):
                game_state = "menu"

            SCREEN.blit(CHARACTER, player[0])
            pygame.display.update()
        
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()
