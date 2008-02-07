#! /usr/bin/env python

import pygame
from pygame import draw
from pygame import event
from pygame.locals import *

from board import Board, _black, _white, _unknown

screen = None
bg_color = (50,100,200)
size = (640,480)

def graphical_main():
    # init    
    pygame.init()
    global screen
    screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF)    

    # program loop #
    done = False
    while not done:
        # events #
        for e in event.get():
            if e.type == QUIT: done = True
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE: event.post(event.Event(QUIT))

        # draw #
        screen.fill(bg_color)
        draw(screen)
        pygame.display.flip()

    pygame.quit()    


# board drawing constants
grid_color = (150,150,255)
cell_half_base = 8
cell_height = 16

colors = {
    _black:(32,32,64),
    _white:(240,240,255),
    _unknown:bg_color,
    }

def draw_board(board, init_pos):
    x0, y0 = init_pos
    for pos in board.positions:
        x, y = pos
        up = ((x + y) % 2 == 1)
        color = colors[board[pos]]
        draw_cell(x0 + x * cell_half_base, y0 + y * cell_height, color, up)

def draw_sym_line(surface, color, start, end):
    mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
    pygame.draw.line(surface, color, start, mid)
    pygame.draw.line(surface, color, end, mid)
    
def draw_cell(x, y, color, up):
    if up:
        point = (x + cell_half_base, y)
        left = (x, y + cell_height)
        right = (x + 2 * cell_half_base, y + cell_height)
    else:
        point = (x + cell_half_base, y + cell_height)
        left = (x, y)
        right = (x + 2 * cell_half_base, y)
    pygame.draw.polygon(screen, color, (point, left, right))
    
    draw_sym_line(screen, grid_color, left, point)
    draw_sym_line(screen, grid_color, right, point)
    draw_sym_line(screen, grid_color, left, right)
    
test_board = Board('''
   .X. .
  ..X.. .
  . .X.X.
   X. ..
''')

def draw(screen):
    draw_board(test_board, (10,10))

if __name__ == '__main__':
    graphical_main()


