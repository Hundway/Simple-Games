import pygame
from pygame.locals import *
from random import randint

WIDTH, HEIGHT = 1080, 720
BASE = 40
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)

class shooter:
    def __init__(self):
        self.x = (WIDTH - BASE) / 2
        self.y = HEIGHT - BASE * 2
        self.projectiles = []
    
    def shoot(self):
        if len(self.projectiles) < 4:
            self.projectiles.append({'x' : self.x, 'y' : self.y})

class enemy:
    def __init__(self):
        self.fleet = []
    
    def create_fleet(self):
        for y in range(int(BASE/2), BASE * 6, BASE*2):
            for x in range(BASE, WIDTH - BASE, BASE*2):
                self.fleet.append({'x' : x, 'y' : y})

pygame.init()

player_1 = shooter()
alliance = enemy()
alliance.create_fleet()

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("couriernew", int(BASE*1.5))
pygame.display.set_caption("Space Invaders")
win_msg = font.render("You Win !", True, BLACK) 

while True:
    clock.tick(FPS)

    display.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player_1.shoot()
      
    if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
        player_1.x -= 5
    if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
        player_1.x += 5

    for bullet in player_1.projectiles:
        bullet['y'] -= 5

        if bullet['y'] <= 0:
            player_1.projectiles.remove(bullet)

    for ship in alliance.fleet:
        for bullet in player_1.projectiles:
            
            shp = pygame.Rect((ship['x'], ship['y'], BASE, BASE))
            blt = pygame.Rect((bullet['x'] + BASE / 4, bullet['y'], BASE/2, BASE/2))
            
            if shp.colliderect(blt):
                player_1.projectiles.remove(bullet)
                alliance.fleet.remove(ship)

    p1 = pygame.draw.rect(display, BLACK, (player_1.x, player_1.y, BASE, BASE), BASE//6)

    for ship in alliance.fleet:
        pygame.draw.rect(display, BLACK, (ship['x'], ship['y'], BASE, BASE), BASE//6)

    for bullet in player_1.projectiles:
        pygame.draw.rect(display, BLACK, (bullet['x'] + BASE / 4, bullet['y'], BASE/2, BASE/2), BASE//6)

    if len(alliance.fleet) == 0:
        display.blit(win_msg, ((WIDTH - win_msg.get_width())//2, BASE))

    pygame.display.flip()