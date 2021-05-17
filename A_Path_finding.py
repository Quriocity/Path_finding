import pygame
import math
from queue import PriorityQueue
import random
import algo
width = 600
#Create a window with specified dimensions
pygame.init()
win = pygame.display.set_mode((width,width))
#Give a caption to the window
pygame.display.set_caption("A-star")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 125)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
#Initialise the spot with respective row, col
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = self.row * width
        self.y = self.col * width
        self.color = WHITE
        self.neighbour = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    def is_open(self):
        return self.color == WHITE
    def is_closed(self):
        return self.color == RED
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE

#Draw the spot in the display window
    def draw(self, win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width,self.width))
    def __lt__(self,other):
        return False
    def update_neighbour(self, grid):
        neighbour = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():   #Down
            self.neighbour.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():      #Up
            self.neighbour.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():   #Right
            self.neighbour.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbour.append(grid[self.row][self.col - 1])



def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Return the row and col position of point clicked by mouse
def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col

#Create grid with specified number of rows and cols
#Add the spots to grid(list)
def make_grid(width, rows):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

#Draw lines horizontally and vertically and it looks like a grid
def draw_grid(width, rows):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0, i * gap),(width,i * gap))
    for j in range(rows):
        pygame.draw.line(win,GREY,(j * gap, 0),(j * gap,width))

#Draw the spots and grid
def draw(win, width, rows, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(width, rows)
    pygame.display.update()


def main(width):
    ROWS = 50
    start = None
    end = None
    run = True
    started = True
    grid = make_grid(width,ROWS)
    def random_barrier():
        for i in range(5):
            r = random.randint(0,49)
            c = random.randint(0,49)
            spot = grid[r][c]
            if spot != start and spot != end:
                spot.make_barrier()
    while run:
        draw(win, width, ROWS, grid)
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                if not end and spot != start:
                    end = spot
                    end.make_end()
                if spot != start and spot != end:
                    #random_barrier()
                    spot.make_barrier()



            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width) 
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for rows in grid:
                        for spot in rows:
                            spot.update_neighbour(grid)
                    algo.algorithm(lambda: draw(win, width, ROWS, grid), grid, start, end,h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(width,ROWS)



    #pygame.quit()



main(width)
