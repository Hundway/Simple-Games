import pygame, random
import numpy as np
import SudokuSolver as ss
from pygame.locals import *
from sys import exit      

WIDTH, HEIGHT = 500, 700
CELL = 50
FPS = 10

# Colors
BGC = (10, 25, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (230, 240, 255)
BLUE = (70, 110, 180)
DARK_BLUE = (8, 20, 24)
AIR_BLUE = (160, 190, 220)
GREEN = (0, 180, 0)

class Sudoku_grid:
    def __init__(self, x: int, y: int, color: tuple):
        self.__x = x
        self.__y = y
        self.__height = CELL
        self.__color = color
        self.__true_values = ss.create_sudoku("hard")
        self.__user_values = np.zeros((9, 9), dtype=int)

        self.__cell_pos = []
        for i in range(9):
            for j in range(9):
                self.__cell_pos.append((self.__x + i * self.__height,
                                      self.__y + j * self.__height))
        self.__cell_pos = np.reshape(self.__cell_pos, (9, 9, 2))
        
        self.__possible_values = []
        for i in range(9):
            self.__possible_values.append([])
        for i in range(9):
            for j in range(9):
                self.__possible_values[i].append([])
    
    def set_cell(self, position: tuple, value: int):
        i, j = position
        if self.__true_values[i][j] == 0:
            self.__user_values[i][j] = value
            self.__possible_values[i][j] = []
    
    def set_possible_value(self, value: int, position: tuple):
        if position == None:
            return None
        i, j = position
        if self.__user_values[i][j] != 0:
            return None
        if value in self.__possible_values[i][j]:
            self.__possible_values[i][j].remove(value)
        else:
            self.__possible_values[i][j].append(value)
            self.__possible_values[i][j].sort()
    
    def new_game(self, difficulty: str):
        self.__true_values = ss.create_sudoku(difficulty)
        self.__user_values = np.zeros((9, 9), dtype=int)
        self.__possible_values = []
        for i in range(9):
            self.__possible_values.append([])
        for i in range(9):
            for j in range(9):
                self.__possible_values[i].append([])
        self.__color = BLACK

    def solve(self):
        if ss.solved(self.__true_values):
            return None
            
        ss.solve_sudoku(self.__true_values)
        self.__user_values = np.zeros((9, 9))
    
    def check(self):
        solved_grid = self.__true_values.copy()
        ss.solve_sudoku(solved_grid)
        
        for i in range(9):
            for j in range(9):
                if solved_grid[i][j] == self.__user_values[i][j]:
                    self.__true_values[i][j] = solved_grid[i][j]
                self.__user_values[i][j] = 0
                
        if ss.solved(self.__true_values):
            self.__color = GREEN
            return True 

        return False
    
    def hint(self, position: tuple):
        if ss.solved(self.__true_values):
            return None

        if position == None:
            position = [(i,j) for i in range(9) for j in range(9)]
            random.shuffle(position)
            pos = position.pop()
            while self.__true_values[pos[0]][pos[1]] != 0:
                pos = position.pop()
            position = pos

        i, j = position
        self.__user_values[i][j] = 0
        self.__true_values[i][j] = ss.hint(self.__true_values, position)
    
    def draw(self, highlighted_cell):
        # 9x9 white cell
        pygame.draw.rect(display, WHITE, (self.__x, self.__y,
                                               self.__height * 9,
                                               self.__height * 9))
        if highlighted_cell != None:
            hgl_i, hgl_j = highlighted_cell
            # Highlight row
            for column in range(9):
                cell_rect = (self.__x + hgl_i * self.__height,
                             self.__y + column * self.__height, 
                             self.__height, self.__height)
                pygame.draw.rect(display, GREY, cell_rect)
            # Highlight column
            for row in range(9):
                cell_rect = (self.__x + row * self.__height,
                             self.__y + hgl_j * self.__height, 
                             self.__height, self.__height)
                pygame.draw.rect(display, GREY, cell_rect)
            # Highlight 3x3 grid
            i_row = (hgl_i // 3) * 3
            i_column = (hgl_j // 3) * 3
            for row in range(i_row, i_row + 3):
                for column in range(i_column, i_column + 3):
                    cell_rect = (self.__x + row * self.__height,
                                 self.__y + column * self.__height, 
                                 self.__height, self.__height)
                    pygame.draw.rect(display, GREY, cell_rect)
            # Highlight cell
            for column in range(9):
                cell_rect = (self.__x + hgl_i * self.__height,
                             self.__y + hgl_j * self.__height, 
                             self.__height, self.__height)
                pygame.draw.rect(display, AIR_BLUE, cell_rect)

            if self.__true_values[hgl_i][hgl_j] != 0:
                # Highlight true values selected
                value = self.__true_values[hgl_i][hgl_j]
                for row in range(9):
                    for column in range(9):
                        if(self.__true_values[row][column] == value
                          or self.__user_values[row][column] == value):
                            cell_rect = (self.__x + row * self.__height,
                                         self.__y + column * self.__height, 
                                         self.__height, self.__height)
                            pygame.draw.rect(display, AIR_BLUE, cell_rect)

            if self.__user_values[hgl_i][hgl_j] != 0:
                # Highlight selected values
                value = self.__user_values[hgl_i][hgl_j]
                for row in range(9):
                    for column in range(9):
                        if(self.__true_values[row][column] == value
                          or self.__user_values[row][column] == value):
                            cell_rect = (self.__x + row * self.__height,
                                         self.__y + column * self.__height, 
                                         self.__height, self.__height)
                            pygame.draw.rect(display, AIR_BLUE, cell_rect)

        # Individual cells
        for i in range(9):
            for j in range(9):
                cell_rect = (self.__x + i * self.__height,
                             self.__y + j * self.__height,
                             self.__height, self.__height)
                pygame.draw.rect(display, BLACK, cell_rect, 1)

        # 9x9 border
        pygame.draw.rect(display, BLACK, (self.__x, self.__y,
                                          self.__height * 9,
                                          self.__height * 9), 5)
        # 3x3 cells
        for i in range(3):
            for j in range(3):
                grid_rect = (self.__x + i * self.__height * 3,
                             self.__y + j * self.__height* 3,
                             self.__height * 3, self.__height * 3)
                pygame.draw.rect(display, BLACK, grid_rect, 3)

        # Draw true numbers
        for i in range(9):
            for j in range(9):
                if grid.__true_values[i][j] != 0:
                    value = num1_font.render(f"{grid.__true_values[i][j]}",
                                             True, self.__color)
                    display.blit(value, ((self.__x + 13) + i * self.__height,
                                         (self.__y + 3) + j * self.__height)) 

        # Draw user input numbers
        for i in range(9):
            for j in range(9):
                if grid.__user_values[i][j] != 0:
                    value = num1_font.render(f"{grid.__user_values[i][j]}",
                                             True, BLUE)
                    display.blit(value, ((self.__x + 13) + i * self.__height,
                                         (self.__y + 3) + j * self.__height))
        
        # Draw possible values
        for i in range(9):
            for j in range(9):
                for index, value in enumerate(self.__possible_values[i][j]):
                    value = num2_font.render(f"{value}", True, BLACK)
                    row = index % 3
                    column = index  // 3
                    dest = (self.__x + i * self.__height + row * self.__height / 3 + 4,
                            self.__y + j * self.__height + column * self.__height / 3)
                    display.blit(value, dest)

    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                if(mouse_pos[0] >= self.__cell_pos[i][j][0]
                   and mouse_pos[0] <= self.__cell_pos[i][j][0] + self.__height):
                    if(mouse_pos[1] >= self.__cell_pos[i][j][1]
                       and mouse_pos[1] <= self.__cell_pos[i][j][1] + self.__height):
                       return i, j
        return None
    
class Keyboard():
    def __init__(self, row, column):
        self.x = 20 + CELL * row
        self.y = (CELL * column) - 10
        self.width = CELL / 1.5
        self.height = CELL + 20
        self.numbers = [num for num in range(1,10)]
        self.rect = [(self.x * 1.5 + number * CELL, self.y,
                      self.width, self.height) for number in range(9)]
        self.num_pos = [((self.x + 15) + number * self.width * 1.5,
                          self.y + 10) for number in range(9)]

    def draw(self):
        for i in range(9):
            pygame.draw.rect(display, DARK_BLUE, self.rect[i])
            text = num1_font.render(str(i + 1), True, WHITE)
            display.blit(text, self.num_pos[i])
    
    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()
        for i in range(9):
            if(mouse_pos[0] >= self.rect[i][0]
              and mouse_pos[0] <= self.rect[i][0] + self.width):
                if(mouse_pos[1] >= self.rect[i][1]
                  and mouse_pos[1] <= self.rect[i][1] + self.height):
                   return i + 1
        return None
    
class Button():
    def __init__(self, text, row, column):
        self.text = text
        self.x = 20 + row * CELL
        self.y = column * CELL
        self.width = len(text) * CELL/2 - 15
        self.height = CELL

    def draw(self):
        # rect = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(display, BLACK, rect)
        # pygame.draw.rect(display, BGC, rect,3)
        text = text_font.render(self.text, True, WHITE)
        display.blit(text, (10 + self.x, 3 + self.y))

    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.x and mouse_pos[0] <= self.x + self.width:
            if mouse_pos[1] >= self.y and mouse_pos[1] <= self.y + self.height:
                return True
        return False

pygame.init()

pygame.display.set_caption("Sudoku")
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
num1_font = pygame.font.SysFont("calibri", CELL)
num2_font = pygame.font.SysFont("calibri", int(CELL/2.5))
text_font = pygame.font.SysFont("CopperplGothBdBT", CELL)

grid = Sudoku_grid(20, CELL, BLACK)
highlighted_cell = None


new_game_bt = Button("new game", 0, 0)
check_bt = Button("check", 0, 10)
hint_bt = Button("hint", 3.6, 10)
solve_bt = Button("solve", 6.8, 10)
keyboard_bts = Keyboard(0, 12)

while True:
    clock.tick(FPS)
    display.fill(BGC)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if grid.mouse_is_over():
                highlighted_cell = grid.mouse_is_over()
            elif new_game_bt.mouse_is_over():
                grid.new_game("hard")
            elif check_bt.mouse_is_over():
                grid.check()
            elif hint_bt.mouse_is_over():
                grid.hint(highlighted_cell)
            elif solve_bt.mouse_is_over():
                grid.solve()           
            elif keyboard_bts.mouse_is_over():
                value = keyboard_bts.mouse_is_over()
                grid.set_possible_value(value, highlighted_cell)
            else:
                highlighted_cell = None

        if event.type == pygame.KEYDOWN and highlighted_cell != None:
            if event.unicode.isnumeric():
                grid.set_cell(highlighted_cell, int(event.unicode))
            if pygame.key.name(event.key) == 'backspace':
                grid.set_cell(highlighted_cell, 0)
                  
    grid.draw(highlighted_cell)
    new_game_bt.draw()
    check_bt.draw()
    solve_bt.draw()
    hint_bt.draw()
    keyboard_bts.draw()

    pygame.display.flip()