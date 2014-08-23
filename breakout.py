#    A Breakout clone made for a workshop at the Squidwrench hackerspace
#    Copyright (C) 2014 Peter Bourgelais

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program in the file LICESNSE.txt.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from time import *
from bounceables import *
from levels import * 
from pygame.locals import *
from ball import *
from constants import *


pygame.init()
DISPLAY = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('SquidWrench Breakout - prototyped by Peter Bourgelais')
FPSCLOCK = pygame.time.Clock()

def main():
    level_array = load_and_draw_level()
    pdl = Paddle(WHITE, PADDLE_TOP, PADDLE_LEFT)

    bl = Ball(WHITE, BALL_TOP, BALL_LEFT, 0, 1)
    game_speed = 30
    speedup = 0

    left_wall = Wall(0,1,1,SCREENHEIGHT,'x')
    top_wall = Wall(0,0,SCREENWIDTH,1,'y')
    right_wall = Wall(SCREENWIDTH-1,1,1,SCREENHEIGHT,'x')
    walls = [left_wall, top_wall, right_wall]
    
    pygame.draw.rect(DISPLAY, bl.color, bl.ball_rect())
    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
    pygame.display.update()

    game_started = False
    while game_started == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                game_started = True
        pygame.display.update()
    # move the ball
#    bl.update_position()
    # check for collisions against...
    #     the walls
#    for wall in walls:
#        if pygame.Rect.colliderect(wall,bl.ball_rect()):
#            bl.process_collision({'AIAR': wall.axis})
    #     the blocks
    #     the paddle
    #     the bottom of the screen
    # handle paddle movement
    # check for victory condition (all blocks have ccounter == 0)

    #tick the FPS clock
#    FPSCLOCK.tick(game_speed)

def load_and_draw_level():
    lf = LevelFactory()
    level_array = lf.block_array
    vertical_offset = BLOCK_HEIGHT
    horizontal_offset = BLOCK_WIDTH
    for block in level_array:
        pygame.draw.rect(DISPLAY, block.color, block.rect)
    return level_array

def draw_level(arr):
    pass

if __name__ == '__main__':
    main()

