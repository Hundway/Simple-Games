import pygame
from pygame.locals import *
import random

WIDTH, HEIGHT = 640, 480
BASE = HEIGHT//20
FPS = 60

COLISION_TOLERANCE = BASE//6

BLACK = (0,0,0)
WHITE = (255,255,255)

def random_sign():
    num_list = [-1, 1]
    return random.choice(num_list)

def random_speed(minimum = 0):
    return random_sign() * random.uniform(minimum, 1) * BASE//4

class bar:
    def __init__(self, x):
        self.height = BASE*4
        self.thickness = BASE//2
        self.top = (HEIGHT - self.height)//2
        self.bottom = self.top + self.height
        self.x_pos = x        
        self.speed = BASE//5
        self.rect = pygame.Rect((self.x_pos, self.top, self.thickness, self.height))
    
    def Move(self, direction):
        if direction == "UP":
            self.top -= self.speed
            self.bottom -= self.speed
        if direction == "DOWN":
            self.top += self.speed
            self.bottom += self.speed
        self.rect = pygame.Rect((self.x_pos, self.top, self.thickness, self.height))

class ball:
    def __init__(self):
        self.radius = BASE//2
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_sp = random_sign() * (BASE//4)
        self.y_sp = random_speed(0)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
        self.is_paused = True
        self.ticks_after_pause = 0

    def Move(self):
        self.x += self.x_sp
        self.y += self.y_sp
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
    
    def Restart(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_sp = random_sign() * (BASE//4)
        self.y_sp = random_speed(0)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
    
    def Pause(self):
        self.is_paused = True
        self.ticks_after_pause = 0
    
    def UnPause(self):
        self.is_paused = False

player_1 = bar(BASE*2)
player_2 = bar(WIDTH - BASE*2 - player_1.thickness)
ball = ball()
score = {"p1" : 0, "p2" : 0}

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("couriernew", int(BASE*1.5))
pygame.display.set_caption("Pong")

while True:
    clock.tick(FPS)

    display.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Player Movements
    if pygame.key.get_pressed()[K_w] and player_1.top > 0:
        player_1.Move("UP")
    if pygame.key.get_pressed()[K_s] and player_1.bottom < HEIGHT:
        player_1.Move("DOWN")
    if pygame.key.get_pressed()[K_UP] and player_2.top > 0:
        player_2.Move("UP")
    if pygame.key.get_pressed()[K_DOWN] and player_2.bottom < HEIGHT:
        player_2.Move("DOWN")

    # Ball Movement
    if ball.y - ball.radius < 0 and ball.y_sp < 0:
        ball.y_sp *= -1
    if ball.y + ball.radius > HEIGHT and ball.y_sp > 0:
        ball.y_sp *= -1
    if ball.x - ball.radius < 0 and ball.x_sp < 0:
        score['p2'] += 1
        ball.Restart()
        ball.Pause()
    if ball.x + ball.radius > WIDTH and ball.x_sp > 0:
        score['p1'] += 1
        ball.Restart()
        ball.Pause()
    
    # Collisions
    # Player_1
    if player_1.rect.colliderect(ball.rect) and ball.x_sp <= 0:
        ball.x_sp *= -1
        if abs(player_1.rect.right - ball.rect.left) <= COLISION_TOLERANCE: 
            ball.y_sp = random_speed()
        if abs(player_1.rect.top - ball.rect.bottom) <= COLISION_TOLERANCE:
            ball.y_sp = -abs(random_speed(0.8))
        if abs(player_1.rect.bottom - ball.rect.top) <= COLISION_TOLERANCE:
            ball.y_sp = abs(random_speed(0.8))
    # Player_2
    if player_2.rect.colliderect(ball.rect) and ball.x_sp >= 0:
        ball.x_sp *= -1
        if abs(player_2.rect.right - ball.rect.left) <= COLISION_TOLERANCE: 
            ball.y_sp = random_speed()
        if abs(player_2.rect.top - ball.rect.bottom) <= COLISION_TOLERANCE:
            ball.y_sp = -abs(random_speed(0.8))
        if abs(player_2.rect.bottom - ball.rect.top) <= COLISION_TOLERANCE:
            ball.y_sp = abs(random_speed(0.8))

    # Only move ball if aren't paused
    if ball.is_paused == False:
        ball.Move()
    # Unpause 1 Second after ball is paused
    elif ball.ticks_after_pause == FPS:
        ball.UnPause()
    # Count ticks after pause
    else:
        ball.ticks_after_pause += 1

    score_txt = font.render(f"{score['p1']}-{score['p2']}", True, BLACK)
    display.blit(score_txt, ((WIDTH - score_txt.get_width())//2, BASE))
    
    pygame.draw.rect(display, (0,0,0), player_1.rect, player_1.thickness//5)
    pygame.draw.rect(display, (0,0,0), player_2.rect, player_1.thickness//5)
    pygame.draw.circle(display, (0,0,0), (int(ball.x), int(ball.y)), ball.radius, ball.radius//5)

    pygame.display.flip()