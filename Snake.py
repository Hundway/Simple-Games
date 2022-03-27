import pygame, sys
from pygame.locals import*
from random import randint, randrange

WIDTH, HEIGHT = 800, 500
FPS = 10
BASE = WIDTH//20

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.size = BASE/2
        self.head_pos = []
        self.body_pos = []
        self.direction = "RIGHT"
    
    def Spawn(self):
        self.head_pos = [randrange(0, WIDTH // self.size) * self.size,
                         randrange(0, HEIGHT // self.size) * self.size]
        self.body_pos = [self.head_pos]
    
    def Move(self):
        # Movement
        if self.direction == "UP":
            self.head_pos[1] -= self.size
        if self.direction == "DOWN":
            self.head_pos[1] += self.size
        if self.direction == "RIGHT":
            self.head_pos[0] += self.size
        if self.direction == "LEFT":
            self.head_pos[0] -= self.size
        
        # Arena Collisions
        if self.head_pos[1] > HEIGHT - self.size:
            self.head_pos[1] = 0
        if self.head_pos[1] < 0:
            self.head_pos[1] = HEIGHT - self.size
        if self.head_pos[0] > WIDTH - self.size:
            self.head_pos[0] = 0
        if self.head_pos[0] < 0:
            self.head_pos[0] = WIDTH - self.size
    
        self.body_pos.insert(0, list(self.head_pos))
        self.body_pos.pop()
    
    def Grow(self):
        self.body_pos.insert(0, list(self.head_pos))
    
class Apple:
    def __init__(self):
        self.size = BASE/2
        self.pos = []
        self.spawned = False
    
    def Spawn(self):
        self.pos = [randrange(0, WIDTH // self.size) * self.size,
                    randrange(0, HEIGHT // self.size) * self.size]
        self.spawned = True

player = Snake()
player.Spawn()

apple = Apple()
apple.Spawn()

pygame.init()

display = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("couriernew", BASE//2)

while True:
    clock.tick(FPS + len(player.body_pos))

    display.fill(WHITE)

    score = (len(player.body_pos) - 1) * (10 + len(player.body_pos) )
    score_msg = font.render(f"Score : {score}", True, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_w and player.direction != "DOWN":
                player.direction = "UP"
            elif event.key == K_s and player.direction != "UP":
                player.direction = "DOWN"
            elif event.key == K_a and player.direction != "RIGHT":
                player.direction = "LEFT"
            elif event.key == K_d and player.direction != "LEFT":
                player.direction = "RIGHT"
        
    player.Move()

    if apple.spawned == False:
        apple.Spawn()

    for pos in player.body_pos[1:]:
        # Body collision
        if player.head_pos[0] == pos[0] and player.head_pos[1] == pos[1]:
            player.Spawn()
            apple.Spawn()
        pygame.draw.rect(display, BLACK, (pos[0], pos[1], player.size, player.size), BASE // 8)  

    apple_rect = pygame.draw.rect(display, BLACK, (apple.pos[0], apple.pos[1] , apple.size, apple.size))
    snake_head = pygame.draw.rect(display, BLACK, (player.body_pos[0][0], player.body_pos[0][1], player.size, player.size), BASE // 8)

    if apple_rect.colliderect(snake_head):
        apple.spawned = False
        player.Grow()

    display.blit(score_msg, (0, 0))

    pygame.display.flip()