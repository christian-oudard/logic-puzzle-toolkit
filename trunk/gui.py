#! /usr/bin/env python

import pygame
from pygame import draw
from pygame import event
from pygame.locals import *

def graphical_main():
    # init    
    pygame.init()
    screen = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)    

    # program loop #
    done = False
    while not done:
        # events #
        for e in event.get():
            if e.type == QUIT: done = True
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE: event.post(event.Event(QUIT))

        # draw #
        screen.fill((50,100,200))
        draw(screen)
        pygame.display.flip()

    pygame.quit()    


# board drawing constants
BOX_COLOR = (255,255,255)
GRID_COLOR = (150, 150, 255)
CELL_HALF_BASE = 8
CELL_HEIGHT = 14

def draw_board(board, screen, pos):
    # TODO:
    #   fix off-by-one graphical errors, possibly by drawing each cell individually

    size = board.size
    rect = Rect(pos, (size*CELL_HALF_BASE*6, size*CELL_HEIGHT*2))

    # bounding box
    pygame.draw.rect(screen, BOX_COLOR, rect, 1)

    # horizontal grid lines
    for i in range(1, size*2):
        y = rect.top + i*CELL_HEIGHT
        pygame.draw.line(screen, GRID_COLOR, (rect.left, y), (rect.right, y))

    # diagonal grid lines
    x1 = rect.left + size*CELL_HALF_BASE*2
    x2 = rect.left + size*CELL_HALF_BASE*4
    pygame.draw.line(screen, GRID_COLOR, rect.bottomleft, (x1, rect.top))
    pygame.draw.line(screen, GRID_COLOR, rect.topleft, (x1, rect.bottom))
    pygame.draw.line(screen, GRID_COLOR, rect.bottomright, (x2, rect.top))
    pygame.draw.line(screen, GRID_COLOR, rect.topright, (x2, rect.bottom))
    pygame.draw.line(screen, GRID_COLOR, (x1, rect.top), (x2, rect.bottom))
    pygame.draw.line(screen, GRID_COLOR, (x1, rect.bottom), (x2, rect.top))


def draw(screen):
    for i in range(1,4):
        t = TriBoard(i)
        draw_board(t, screen, (20, 20*i*i))

if __name__ == '__main__':
    graphical_main()


