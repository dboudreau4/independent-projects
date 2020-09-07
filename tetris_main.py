import pygame
import random

pygame.font.init()

# GLOBAL VARIABLES
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
PLAYAREA_WIDTH = 350
PLAYAREA_HEIGHT = 700
SHAPE_SIZE = 35

UPPER_LEFT_X = (WINDOW_WIDTH - PLAYAREA_WIDTH)//2
UPPER_LEFT_Y = WINDOW_HEIGHT - PLAYAREA_HEIGHT

# COLORS-------------------
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (153, 0, 153)
PINK = (255, 51, 153)
PURPLE = (102, 0, 204)

# SHAPES-------------------
rL = [['*****',
       '***X*',
       '*XXX*',
       '*****',
       '*****'],
      ['*****',
       '**X**',
       '**X**',
       '**XX*',
       '*****'],
      ['*****',
       '*****',
       '*XXX*',
       '*X***',
       '*****'],
      ['*****',
       '*XX**',
       '**X**',
       '**X**',
       '*****']]

lL = [['*****',
       '*X***',
       '*XXX*',
       '*****',
       '*****'],
      ['*****',
       '**XX*',
       '**X**',
       '**X**',
       '*****'],
      ['*****',
       '*****',
       '*XXX*',
       '***X*',
       '*****'],
      ['*****',
       '**X**',
       '**X**',
       '*XX**',
       '*****']]

T = [['*****',
      '**X**',
      '*XXX*',
      '*****',
      '*****'],
     ['*****',
      '**X**',
      '**XX*',
      '**X**',
      '*****'],
     ['*****',
      '*****',
      '*XXX*',
      '**X**',
      '*****'],
     ['*****',
      '**X**',
      '*XX**',
      '**X**',
      '*****']]

square = [['*****',
           '*****',
           '*XX**',
           '*XX**',
           '*****']]

rZ = [['*****',
       '******',
       '**XX**',
       '*XX***',
       '*****'],
      ['*****',
       '**X**',
       '**XX*',
       '***X*',
       '*****']]

lZ = [['*****',
       '*****',
       '*XX**',
       '**XX*',
       '*****'],
      ['*****',
       '**X**',
       '*XX**',
       '*X***',
       '*****']]

bar = [['**X**',
        '**X**',
        '**X**',
        '**X**',
        '*****'],
       ['*****',
        'XXXX*',
        '*****',
        '*****',
        '*****']]

shapes = [rL, lL, T, square, rZ, lZ, bar]
colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PINK, PURPLE]

class Shape(object): 

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.rot = 0

def grid_lines(surface, grid):

    for i in range(len(grid)):
        pygame.draw.line(surface, BLUE, (UPPER_LEFT_X, UPPER_LEFT_Y + i * SHAPE_SIZE), (UPPER_LEFT_X + PLAYAREA_WIDTH, UPPER_LEFT_Y + i * SHAPE_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, BLUE, (UPPER_LEFT_X + j * SHAPE_SIZE, UPPER_LEFT_Y), (UPPER_LEFT_X + j * SHAPE_SIZE, UPPER_LEFT_Y + PLAYAREA_HEIGHT))

def set_window(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsansms', 50)
    label = font.render('Tetris', 1, YELLOW)

    surface.blit(label, (UPPER_LEFT_X + PLAYAREA_WIDTH/2 - (label.get_width()/2), 40))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (UPPER_LEFT_X + j * SHAPE_SIZE, UPPER_LEFT_Y + i * SHAPE_SIZE, SHAPE_SIZE, SHAPE_SIZE), 0)

    pygame.draw.rect(surface, RED, (UPPER_LEFT_X, UPPER_LEFT_Y, PLAYAREA_WIDTH, PLAYAREA_HEIGHT), 5)

    grid_lines(surface, grid)

def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                key = locked_pos[(j, i)]
                grid[i][j] = key
    return grid

def get_block():
    return Shape(5, 0, random.choice(shapes))

def shape_format(shape):
    positions = []
    form = shape.shape[shape.rot % len(shape.shape)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, YELLOW)

    sx = UPPER_LEFT_X + PLAYAREA_WIDTH + 50
    sy = UPPER_LEFT_Y + PLAYAREA_HEIGHT/2 - 100
    form = shape.shape[shape.rot % len(shape.shape)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                pygame.draw.rect(surface, shape.color, (sx + j*SHAPE_SIZE, sy + i*SHAPE_SIZE, SHAPE_SIZE, SHAPE_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def main(win):

    locked_pos = {}
    grid = create_grid(locked_pos)
    
    change_piece = False
    game_running = True
    curr_piece = get_block()
    next_piece = get_block()
    timer = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while game_running:

        grid = create_grid(locked_pos)
        fall_time += timer.get_rawtime()
        timer.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            curr_piece.y += 1
            if not(valid_space(curr_piece, grid)) and curr_piece.y > 0:
                curr_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    curr_piece.x -= 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.x += 1
                
                if event.key == pygame.K_RIGHT:
                    curr_piece.x += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.x -= 1
                
                if event.key == pygame.K_UP:
                    curr_piece.rot += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.rot -= 1
                
                if event.key == pygame.K_DOWN:
                    curr_piece.y += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.y -= 1
                
                
        
        shape_pos = shape_format(curr_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = curr_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = curr_piece.color
            curr_piece = next_piece
            next_piece = get_block()
            change_piece = False
            clear_rows(grid, locked_pos)

        
        set_window(win, grid)
        next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_pos):
            game_running = False
    #pygame.display.quit()



window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

main(window)
