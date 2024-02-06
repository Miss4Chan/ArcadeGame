import pygame
import sys
from pygame.locals import *

#The setuppp :))
pygame.init()
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
HALF_WINWIDTH = int(SCREEN_WIDTH / 2)
HALF_WINHEIGHT = int(SCREEN_HEIGHT / 2)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPSCLOCK = pygame.time.Clock()
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
WALLBORDER = 10
MACHINE_WIDTH = 80
MACHINE_HEIGHT = 120
DOOR_WIDTH = 120

WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0) 

player_start_position = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100)
player = pygame.Rect(player_start_position, (40, 40))
entrance = pygame.Rect(HALF_WINWIDTH - DOOR_WIDTH/2, SCREEN_HEIGHT - 11, DOOR_WIDTH, WALLBORDER+1)

WALLS = [
    (0, 0, SCREEN_WIDTH, WALLBORDER),
    (0, 0, 10, SCREEN_HEIGHT),
    (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, WALLBORDER),
    (SCREEN_WIDTH - WALLBORDER, 0, WALLBORDER, SCREEN_HEIGHT)
]

#mislam deka touple e odgovorot za da znam koja mashina e ;')
MACHINES = [
    (pygame.Rect(WALLBORDER, 150, MACHINE_WIDTH, MACHINE_HEIGHT), "scriptName"),  
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH, WALLBORDER+10, MACHINE_WIDTH, MACHINE_HEIGHT),"eden"),
    (pygame.Rect(HALF_WINWIDTH+10, WALLBORDER+10, MACHINE_WIDTH, MACHINE_HEIGHT),"dva"),
    (pygame.Rect(SCREEN_WIDTH-WALLBORDER-MACHINE_WIDTH, 150, MACHINE_WIDTH, MACHINE_HEIGHT),"tri"),
    (pygame.Rect(HALF_WINWIDTH-MACHINE_WIDTH, 270, MACHINE_WIDTH, MACHINE_HEIGHT),"4"),
    (pygame.Rect(HALF_WINWIDTH+10, 270, MACHINE_WIDTH, MACHINE_HEIGHT),"5")
]


def draw_interaction_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if x > HALF_WINHEIGHT: 
        textrect.topleft = (x-150, y-20)
    else:
        textrect.topleft = (x+50, y-20)

    surface.blit(textobj, textrect)


def check_proximity(player, machines, distance=20):
    for machine in machines:
        if player.colliderect(machine[0].inflate(distance, distance)):
            return machine
    return None


def handle_player_interaction(keys, player, machines):
    close_machine = check_proximity(player, machines)
    if close_machine and keys[K_g]:
        # Placeholder for activating something
        #TODO: ova tuka mn bitno vo zavisnost od koja mashina e 
        print("Activated machine!") 
        


def draw_menu():
    SCREEN.fill((0, 0, 0))
    welcome_text = BASICFONT.render("Welcome! Press Enter to start or Escape to quit", True, WHITE)
    SCREEN.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, SCREEN_HEIGHT // 2 - welcome_text.get_height() // 2))
    pygame.display.flip()


def handle_player_movement_ez(keys, player_speed=9):
    if keys[K_LEFT]:
        player.x -= player_speed
    if keys[K_RIGHT]:
        player.x += player_speed
    if keys[K_UP]:
        player.y -= player_speed
    if keys[K_DOWN]:
        player.y += player_speed

    ## ova 10 mozhe da e static var 
    if player.left <= WALLBORDER: player.left = WALLBORDER
    if player.right >= SCREEN_WIDTH-WALLBORDER: player.right = SCREEN_WIDTH -WALLBORDER
    if player.top <= WALLBORDER: player.top = WALLBORDER
    if player.bottom >= SCREEN_HEIGHT-WALLBORDER: player.bottom = SCREEN_HEIGHT-WALLBORDER

    for machine in MACHINES:
        if player.left  <= machine[0].left+machine[0].width: player.left = machine[0].left+machine[0].width
        if player.right >= machine[0].left: player.right = machine[0].left
        if player.top   <= machine[0].bottom : player.top = machine[0].bottom
        if player.bottom>= machine[0].bottom +machine[0].height: player.bottom = machine[0].bottom +machine[0].height
           

def handle_player_movement(keys, player_speed=9):
    original_x, original_y = player.x, player.y

    if keys[K_LEFT]:
        player.x -= player_speed
    if keys[K_RIGHT]:
        player.x += player_speed
    for machine in MACHINES:
        if player.colliderect(machine[0]):
            player.x = original_x
            break  

    if keys[K_UP]:
        player.y -= player_speed
    if keys[K_DOWN]:
        player.y += player_speed

    for machine in MACHINES:
        if player.colliderect(machine[0]):
            player.y = original_y
            break 
        
    if player.left <= WALLBORDER: player.left = WALLBORDER
    if player.right >= SCREEN_WIDTH - WALLBORDER: player.right = SCREEN_WIDTH - WALLBORDER
    if player.top <= WALLBORDER+MACHINE_HEIGHT: player.top = WALLBORDER + MACHINE_HEIGHT
    if player.bottom >= SCREEN_HEIGHT - WALLBORDER: player.bottom = SCREEN_HEIGHT - WALLBORDER


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
                        player.left, player.top = player_start_position 
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        elif game_state == "playing":
            SCREEN.fill((0, 0, 0))
            for wall in WALLS:
                pygame.draw.rect(SCREEN, WHITE, wall)
            pygame.draw.rect(SCREEN, BLUE, player)
            pygame.draw.rect(SCREEN, GREEN, entrance)
            imp = pygame.image.load("bg_wall.png").convert()
            #TODO: 
            #imp2= pygame.image.load("bg_floor.png").convert()
            SCREEN.blit(imp, (WALLBORDER, WALLBORDER))
 
            for machine in MACHINES:
               #pygame.draw.rect(SCREEN, RED, machine[0])
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
                draw_interaction_text("Press 'G' to activate " + close_machine[1], BASICFONT, WHITE, SCREEN, player.x, player.y)

            #TODO: 
            # PLAYER_L = pygame.image.load('squirrel.png')
            # PLAYER_R = pygame.transform.flip(PLAYER_L, True, False)
            # TODO: up and down
            if player.colliderect(entrance):
                game_state = "menu"

            ##TODO: proximity detection and machine interaction 

            pygame.display.update()
        
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()
