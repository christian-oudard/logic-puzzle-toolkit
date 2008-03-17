#! /usr/bin/env python

import pygame
from pygame import draw
from pygame import event
from pygame.locals import *

from board import *
from trianglegrid import TriangleGrid

# board drawing constants
screen_size = (640,480)
line_thickness = 3
bg_color = (220,220,200)
grid_color = (150,100,255)
highlight_color = (255,50,50)
colors = {
    BLACK:(32,32,64),
    WHITE:(240,240,255),
    UNKNOWN:(160,160,160)
    }
cell_half_base = 24
cell_height = 48

# drawing functions #
def draw_sym_line(surface, color, start, end):
    mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
    pygame.draw.line(surface, color, start, mid, line_thickness)
    pygame.draw.line(surface, color, end, mid, line_thickness)

class GUI(object):
    def __init__(self, board=None):
        if board is None:
            # debug board
            #self.board = Board(1)
            self.board = TriangleGrid('''
   1X.-Q
  ..X2.-.
  .3.X.56
   X.4..
''')
        self.selected_pos = None

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF)
        
        # set up numbers
        self.number_font = pygame.font.Font(None, 30)
        self.number_surfaces = {}
        for n in GIVENS:
            self.number_surfaces[n] = self.number_font.render(str(n), True, (0,0,0))
        
        self.graphical_main()

    def to_board(self, screen_pos):
        x, y = screen_pos
        cell_row = y // cell_height
        cell_column_right = (cell_height * x + cell_half_base * y) // (2 * cell_height * cell_half_base)
        cell_column_left = (cell_height * x - cell_half_base * y) // (2 * cell_height * cell_half_base)
        return (cell_column_left + cell_column_right, cell_row)

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
                    self.selected_pos = self.to_board(e.pos)
                elif e.type == MOUSEBUTTONDOWN:
                    click_pos = self.to_board(e.pos)
                    if e.button == 1: # left click
                        self.board.set_black(click_pos)
                    elif e.button == 2: # middle click
                        self.board.set_unknown(click_pos)
                    elif e.button == 3: # right click
                        self.board.set_white(click_pos)
    
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
            cell_number = None
            if self.board[pos] in GIVENS:
                cell_color = colors[WHITE]
                cell_number = self.board[pos]
            else:
                cell_color = colors[self.board[pos]]
            self.draw_cell(pos, cell_color, grid_color)
            if cell_number:
                self.draw_number(pos, cell_number)
        if self.selected_pos is not None:
            self.draw_cell(self.selected_pos, None, highlight_color)

    def draw_cell(self, pos, cell_color, line_color):
        x, y = pos
        screen_x, screen_y = self.to_screen(pos)
        if ((x + y) % 2 == 0): # triangle points down
            point = (screen_x + cell_half_base, screen_y + cell_height)
            left = (screen_x, screen_y)
            right = (screen_x + 2 * cell_half_base, screen_y)
        else: # triangle points up
            point = (screen_x + cell_half_base, screen_y)
            left = (screen_x, screen_y + cell_height)
            right = (screen_x + 2 * cell_half_base, screen_y + cell_height)
        if cell_color is not None:
            pygame.draw.polygon(self.screen, cell_color, (point, left, right))
        draw_sym_line(self.screen, line_color, left, point)
        draw_sym_line(self.screen, line_color, right, point)
        draw_sym_line(self.screen, line_color, left, right)

    def draw_number(self, pos, number):
        number_surface = self.number_surfaces[number]
        screen_x, screen_y = self.to_screen(pos)
        screen_x = screen_x + cell_half_base - number_surface.get_width() // 2
        screen_y = screen_y - number_surface.get_height() // 2
        x, y = pos
        if ((x + y) % 2 == 0): # triangle points down
            screen_y += cell_height // 3
        else: # triangle points up
            screen_y += 2 * cell_height // 3
        self.screen.blit(number_surface, (screen_x, screen_y))

    def to_screen(self, pos):
        x, y = pos
        x0, y0 = (0,0) #STUB
        return (x0 + x * cell_half_base, y0 + y * cell_height)

if __name__ == '__main__':
    GUI()


