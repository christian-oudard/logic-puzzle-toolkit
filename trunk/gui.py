#! /usr/bin/env python

import pygame
from pygame import draw
from pygame import event
from pygame.locals import *

from board import Board, _black, _white, _unknown

# board drawing constants
screen_size = (640,480)
bg_color = (50,100,200)
grid_color = (125,125,175)
highlight_color = (200,255,255)
colors = {
    _black:(32,32,64),
    _white:(240,240,255),
    _unknown:bg_color,
    }
cell_half_base = 8
cell_height = 16

# drawing functions #
def draw_sym_line(surface, color, start, end):
    mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
    pygame.draw.line(surface, color, start, mid)
    pygame.draw.line(surface, color, end, mid)

class GUI(object):
    def __init__(self, board=None):
        if board is None:
            # debug board
            #self.board = Board(1)
            self.board = Board('''
   .X. .
  ..X.. .
  . .X.X.
   X. ..
''')
        self.selected_pos = None
        
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF)
        self.graphical_main()

    def graphical_main(self):
        # program loop #
        done = False
        while not done:
            # events #
            for e in event.get():
                if e.type == QUIT: done = True
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE: event.post(event.Event(QUIT))
                elif e.type == MOUSEMOTION:
                    x, y = e.pos
                    cell_row = y // cell_height
                    cell_column_right = (cell_height * x + cell_half_base * y) // (2 * cell_height * cell_half_base)
                    cell_column_left = (cell_height * x - cell_half_base * y) // (2 * cell_height * cell_half_base)
                    self.selected_pos = (cell_column_left + cell_column_right, cell_row)
    
            # draw #
            self.screen.fill(bg_color)
            self.draw()
            pygame.display.flip()
    
        pygame.quit()    
    
    def draw(self):
        self.draw_board((0,0))

    def draw_board(self, init_pos):
        x0, y0 = init_pos
        for pos in self.board.positions:
            x, y = pos
            cell_color = colors[self.board[pos]]
            self.draw_cell(pos, cell_color, grid_color)
        if self.selected_pos is not None:
            self.draw_cell(self.selected_pos, None, highlight_color)

    def draw_cell(self, pos, cell_color, line_color):
        x, y = pos
        screen_x, screen_y = self.to_screen(pos)
        if ((x + y) % 2 == 1):
            point = (screen_x + cell_half_base, screen_y)
            left = (screen_x, screen_y + cell_height)
            right = (screen_x + 2 * cell_half_base, screen_y + cell_height)
        else:
            point = (screen_x + cell_half_base, screen_y + cell_height)
            left = (screen_x, screen_y)
            right = (screen_x + 2 * cell_half_base, screen_y)
        if cell_color is not None:
            pygame.draw.polygon(self.screen, cell_color, (point, left, right))
        draw_sym_line(self.screen, line_color, left, point)
        draw_sym_line(self.screen, line_color, right, point)
        draw_sym_line(self.screen, line_color, left, right)

    def to_screen(self, pos):
        x, y = pos
        x0, y0 = (0,0) #STUB
        return (x0 + x * cell_half_base, y0 + y * cell_height)

if __name__ == '__main__':
    GUI()


