import pygame
import sys
from pygame.locals import *
from memorypuzzle import main as memorypuzzlemain
from slidepuzzle import main as slidepuzzlemain

#The setuppp :))
pygame.init()
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 650
HALF_WINWIDTH = int(SCREEN_WIDTH / 2)
HALF_WINHEIGHT = int(SCREEN_HEIGHT / 2)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPSCLOCK = pygame.time.Clock()
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
WALLBORDER = 10
MACHINE_WIDTH = 80
MACHINE_HEIGHT = 120
DOOR_WIDTH = 120
SCORE = 0 

CHARACTER =  pygame.image.load('character.png')

WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0) 
BLACK = (0,0,0)

player_start_position = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100)
player = (pygame.Rect(player_start_position, (50, 70)),"character.png") #TODO: treba da e pogolem forsure 
entrance = pygame.Rect(HALF_WINWIDTH - DOOR_WIDTH/2, SCREEN_HEIGHT - 11, DOOR_WIDTH, WALLBORDER+1)

WALLS = [
    (0, 0, SCREEN_WIDTH, WALLBORDER),
    (0, 0, 10, SCREEN_HEIGHT),
    (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, WALLBORDER),
    (SCREEN_WIDTH - WALLBORDER, 0, WALLBORDER, SCREEN_HEIGHT)
]

#mislam deka touple e odgovorot za da znam koja mashina e ;')
#TODO: variables za brojchinjava plz 
MACHINES = [
    ##levo
    (pygame.Rect(WALLBORDER+25, 200, MACHINE_WIDTH, MACHINE_HEIGHT), "memorypuzzle"),  
    #gore
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH-10, WALLBORDER+70, MACHINE_WIDTH, MACHINE_HEIGHT),"slidepuzzle"),
    (pygame.Rect(HALF_WINWIDTH, WALLBORDER+70, MACHINE_WIDTH, MACHINE_HEIGHT),"dva"),
    #desno
    (pygame.Rect(SCREEN_WIDTH-WALLBORDER-MACHINE_WIDTH-30, 200, MACHINE_WIDTH, MACHINE_HEIGHT),"tri"),
    #sredina
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH-10, 300, MACHINE_WIDTH, MACHINE_HEIGHT),"4"),
    (pygame.Rect(HALF_WINWIDTH, 300, MACHINE_WIDTH, MACHINE_HEIGHT),"5")
]

##TODO: 
# Score/ score calculation -- separate module for ticket calculation -- each win of game gives 10 tickets, consecutive wins increase by factor of 1.25 
#make it funkyyy

#TODO: 
#Stats board -- tuka vlaga movement constraint za vrz toj area, treba da ima text in multiple lines -  mozhe da e clickable ala button 
#help? - samo render mozhe na boardot jhahahaahha 

#TODO: 
#Bar with a figure that says hi in a message box when near hahahah just for the plot 
def draw_interaction_text(text, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (500, 90)
    background = pygame.image.load('message.png')
    if "G" not in text:
        surface.blit(textobj, [textrect.left+30,textrect.top+20])
    else:
        surface.blit(background, [textrect.left-100, textrect.top-45])
        surface.blit(textobj, textrect)

#TODO: Add the rest of the games and configure their gameplay 
def start_game(game_name):
    global SCORE
    if game_name == "memorypuzzle":
        print(f"Starting game: {game_name}")
        player[0].x,player[0].y, SCORE = memorypuzzlemain(player[0].x, player[0].y, SCORE)
    if game_name == "slidepuzzle":
        player[0].x,player[0].y, SCORE = slidepuzzlemain(player[0].x, player[0].y, SCORE)

#TODO: proximity za chovecheto na shankot 
def check_proximity(player, machines, distance=20):
    for machine in machines:
        if player[0].colliderect(machine[0].inflate(distance, distance)):
            return machine
    return None


def handle_player_interaction(keys, player, machines):
    close_machine = check_proximity(player, machines)
    if close_machine and keys[K_g]:
        # Placeholder for activating something
        #TODO: ova tuka mn bitno vo zavisnost od koja mashina e 
        print("Activated machine!") 
        start_game(close_machine[1])
        pygame.event.clear() #so start game go reshavame choiceot na script
        

def draw_menu():
    SCREEN.fill((0, 0, 0))
    welcome_text = BASICFONT.render("Welcome! Press Enter to start or Escape to quit", True, WHITE)
    SCREEN.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, SCREEN_HEIGHT // 2 - welcome_text.get_height() // 2))
    pygame.display.flip()
  

def handle_player_movement(keys, player_speed=9):
    global CHARACTER

    PLAYER_R = pygame.image.load('character.png')
    PLAYER_L = pygame.transform.flip(PLAYER_R, True, False)

    original_x, original_y = player[0].x, player[0].y

    if keys[K_LEFT]:
        player[0].x -= player_speed
        CHARACTER = PLAYER_L
    if keys[K_RIGHT]:
        player[0].x += player_speed
        CHARACTER = PLAYER_R
    for machine in MACHINES:
        if player[0].colliderect(machine[0]):
            player[0].x = original_x
            break  

    if keys[K_UP]:
        player[0].y -= player_speed
    if keys[K_DOWN]:
        player[0].y += player_speed

    for machine in MACHINES:
        if player[0].colliderect(machine[0]):
            player[0].y = original_y
            break 
        
    if player[0].left <= WALLBORDER: player[0].left = WALLBORDER
    if player[0].right >= SCREEN_WIDTH - WALLBORDER: player[0].right = SCREEN_WIDTH - WALLBORDER
    if player[0].top <= WALLBORDER+MACHINE_HEIGHT: player[0].top = WALLBORDER + MACHINE_HEIGHT
    if player[0].bottom >= SCREEN_HEIGHT - WALLBORDER: player[0].bottom = SCREEN_HEIGHT - WALLBORDER


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
            #pygame.draw.rect(SCREEN, BLUE, player[0])
            pygame.draw.rect(SCREEN, GREEN, entrance)
            img = pygame.image.load("bg_wall.png").convert()
            img2= pygame.image.load("bg_floor.png").convert()
            img3=pygame.image.load("bg_lights.png").convert()
            SCREEN.blit(img, (WALLBORDER, WALLBORDER+50))
            SCREEN.blit(img2, (WALLBORDER, WALLBORDER+150))
            SCREEN.blit(img3, (WALLBORDER, WALLBORDER))
            for machine in MACHINES:
               #Convert alpha ni treba radi pngto da e transparent ugh ;(
               m = pygame.image.load("machine.PNG").convert_alpha()
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

            if player[0].colliderect(entrance):
                game_state = "menu"

            SCREEN.blit(CHARACTER, player[0])
            pygame.display.update()
        
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()
