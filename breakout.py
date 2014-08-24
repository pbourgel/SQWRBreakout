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

    bl = Ball(WHITE, BALL_TOP, BALL_LEFT, 0, -1)
    game_speed = 60
    speedup = 0
    reset = False

    left_wall = Wall(0,1,1,SCREENHEIGHT,'x')
    top_wall = Wall(0,0,SCREENWIDTH,1,'y')
    right_wall = Wall(SCREENWIDTH-1,1,1,SCREENHEIGHT,'x')
    walls = [left_wall, top_wall, right_wall]
    
    
    pygame.draw.rect(DISPLAY, bl.color, bl.ball_rect())
    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
    pygame.display.update()

    game_started = False
    left_key_pressed = False
    right_key_pressed = False
    while game_started == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                game_started = True
        pygame.display.update()

    while reset == False:
        # move the ball
        DISPLAY.fill(BLACK)
        draw_level(level_array)
        bl.update_position()
        pygame.draw.rect(DISPLAY, bl.color, bl.ball_rect())
        pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
        # check for collisions against...
        #     the walls
        for wall in walls:
            if pygame.Rect.colliderect(wall.rect,bl.ball_rect()):
                bl.process_collision(wall.on_collide())
        #     the blocks
        for block in reversed(level_array):
            if block.ccounter > 0 and pygame.Rect.colliderect(block.rect,bl.ball_rect()):
                bl.process_collision(block.on_collide(bl.ball_rect()))
        #Why reversed?  It's probably the case that the blocks towards the 
        #end of the array (and therefore closer to the paddle) are more likely
        #to collide with the ball on an arbitrary check, so I start from the 
        #end and work my way back to save some loops.  We also do short-circuit
        #evaluation via the color counter to spare some colliderect calls
    
    
        #     the paddle
        if pygame.Rect.colliderect(bl.ball_rect(),pdl.paddle_rect()):
            bl.process_collision(pdl.on_collide(bl))
    
        #     the bottom of the screen
        if bl.ball_rect().bottom >= SCREENHEIGHT:
            reset = True  
    
        # handle paddle movement
        #by the way, if you had a powerup where the paddle has little guns
        #attached to shoot the blocks, some keyboard handling code might be here.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                     left_key_pressed = True
#                    pdl.move_paddle('-')
#                    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
                elif event.key == K_RIGHT:
                     right_key_pressed = True
#                    pdl.move_paddle('+')
#                    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
                elif event.key == K_ESCAPE:
                    reset = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                     left_key_pressed = False
#                    pdl.move_paddle('-')
#                    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
                elif event.key == K_RIGHT:
                     right_key_pressed = False
#                    pdl.move_paddle('+')
#                    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
                #if you wanted to make the paddle move around the level, which I believe exists in exactly ZERO
                #Breakout/Arkanoid games (first time for everything, right?), you would add another conditional
                #and tweak Paddle.move_paddle()
        if left_key_pressed:
           pdl.move_paddle('-')
           pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
        if right_key_pressed:
           pdl.move_paddle('+')
           pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
        
        
        # check for victory condition (all blocks have ccounter == 0)
        # of course you would want to change this if you wanted multiple levels
        if len(filter(lambda block: block.ccounter > 0,level_array)) == 0:
            reset = True
    
        #tick the FPS clock
        pygame.display.update()
        FPSCLOCK.tick(game_speed)

def load_and_draw_level():
    lf = LevelFactory()
    level_array = lf.block_array
    vertical_offset = BLOCK_HEIGHT
    horizontal_offset = BLOCK_WIDTH
    for block in level_array:
        pygame.draw.rect(DISPLAY, block.color, block.rect)
    return level_array

def draw_level(arr):
    for block in arr:
        pygame.draw.rect(DISPLAY, block.color, block.rect)

if __name__ == '__main__':
    main()

