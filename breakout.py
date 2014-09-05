###############################################################################
#                                                                             #
# breakout.py                                                                 #
#                                                                             #
# Contains the main game loop and handles events involving all the other game #
# objects.                                                                    #
#                                                                             #
#                                                                             #
###############################################################################

#    A Breakout clone made for a workshop at the Squidwrench hackerspace
#    All original content Copyright (C) 2014 Peter Bourgelais

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
import sys
from time import *
from bounceables import *
from levels import * 
from pygame.locals import *
from ball import *
from constants import *
#Set up pygame, the display, the window, and the FPS clock
pygame.init()
DISPLAY = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('SquidWrench Breakout - prototyped by Peter Bourgelais')
FPSCLOCK = pygame.time.Clock()

def main():
    #load and draw the first level, create the paddle and ball,
    #set the frame rate and a boolean variable to tell whether 
    #we should end the game (misnamed reset).
    level_array = load_and_draw_level()
    pdl = Paddle(WHITE, PADDLE_TOP, PADDLE_LEFT)
    bl = Ball(WHITE, BALL_TOP, BALL_LEFT, 0, -BALL_SPEED)
    game_speed = 60
    #speedup = 0
    reset = False

    #build walls for the game screen that the ball can reflect off of
    left_wall = Wall(0,1,1,SCREENHEIGHT,'x')
    top_wall = Wall(0,0,SCREENWIDTH,1,'y')
    right_wall = Wall(SCREENWIDTH-1,1,1,SCREENHEIGHT,'x')
    walls = [left_wall, top_wall, right_wall]
        
    #draw all the things (ball and paddle)
    pygame.draw.rect(DISPLAY, bl.color, bl.ball_rect())
    pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())
    pygame.display.update()

    game_started = False
    left_key_pressed = False
    right_key_pressed = False
    while game_started == False:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                game_started = True
        pygame.display.update()

    while reset == False:
        #clear the old screen
        DISPLAY.fill(BLACK)
        collided = False

        #draw the level and update the position of the ball
        draw_level(level_array)
        bl.update_position()

        #draw the (moved) ball and paddle
        pygame.draw.rect(DISPLAY, bl.color, bl.ball_rect())
        pygame.draw.rect(DISPLAY, pdl.color, pdl.paddle_rect())

        # check for collisions against...
        #     the walls
        for wall in walls:
            if pygame.Rect.colliderect(wall.rect,bl.ball_rect()):
                bl.process_collision(wall.on_collide())
        #     the blocks
        #Why reversed?  It's probably the case that the blocks towards the 
        #end of the array (and therefore closer to the paddle) are more likely
        #to collide with the ball on an arbitrary check, so I start from the 
        #end and work my way back to save some iterations.  We also do short-circuit
        #evaluation via the color counter to spare some colliderect calls

        for block in reversed(level_array):
            if block.ccounter > 0 and collided == False and pygame.Rect.colliderect(block.rect,bl.ball_rect()):
                bl.process_collision(block.on_collide(bl))
                collided = True
            if collided: #make sure we only process one collision with a block per animation frame
                break
    
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
                elif event.key == K_RIGHT:
                     right_key_pressed = True
                elif event.key == K_ESCAPE:
                    reset = True
            #This extra if is required to move the paddle by holding down 
            #the left or right cursors instead of repeatedly tapping them.
            #The loop continues to move the paddle until it sees that the key is 
            #released.
            if event.type == KEYUP:
                if event.key == K_LEFT:
                     left_key_pressed = False
                elif event.key == K_RIGHT:
                     right_key_pressed = False
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

#Loads the (currently one) level, draws it, and returns it
#This might have to be refactored for multiple levels
def load_and_draw_level():
    lf = LevelFactory()
    level_array = lf.block_array
    for block in level_array:
        pygame.draw.rect(DISPLAY, block.color, block.rect)
    return level_array

#Iterates over the block array and draws the blocks to the 
#screen with their current color
def draw_level(arr):
    for block in arr:
        pygame.draw.rect(DISPLAY, block.color, block.rect)

if __name__ == '__main__':
    main()




























#Here's a little easter egg for those of you who paid enough attention to the 
#source code.  I wrote this clone not long after quitting a promising job 
#that got so bad it nearly took the fun out of programming.  I owe the folks at 
#the Squidwrench hackerspace a big thanks for providing a place where I could 
#work on something low-pressure yet technical at a time when I was seriously
#burned out.  Richard Feynman spoke to this better than I can:

#From ``Surely you're joking, Mr. Feynman'', by Richard Feynman, 
#Copyright 1985, pg. 157-158.

#"Then I had another thought: Physics disgusts me a little bit now, but I used to 
#enjoy doing physics. Why did I enjoy it? I used to play with it. I used to do 
#whatever I felt like doing - it didn't have to do with whether it was important for the 
#development of nuclear physics, but whether it was interesting and amusing for me to 
#play with. When I was in high school, I'd see water running out of a faucet growing 
#narrower, and wonder if I could figure out what determines that curve. I found it was 
#rather easy to do. I didn't have to do it; it wasn't important for the future of 
#science; somebody else had already done it. That didn't make any difference. 
#I'd invent things and play with things for my own entertainment.

#So I got this new attitude. Now that I am burned out and I'll never accomplish anything, 
#I've got this nice position at the university teaching classes which I rather enjoy, 
#and just like I read the Arabian Nights for pleasure, I'm going to play with physics, 
#whenever I want to, without worrying about any importance whatsoever.

#Within a week I was in the cafeteria and some guy, fooling around, throws a plate in 
#the air. As the plate went up in the air I saw it wobble, and I noticed the red 
#medallion of Cornell on the plate going around. It was pretty obvious to me that 
#the medallion went around faster than the wobbling.

#I had nothing to do, so I start to figure out the motion of the rotating plate. I 
#discover that when the angle is very slight, the medallion rotates twice as fast 
#as the wobble rate - two to one. It came out of a complicated equation! Then I 
#thought, ``Is there some way I can see in a more fundamental way, by looking at 
#the forces or the dynamics, why it's two to one?''

#I don't remember how I did it, but I ultimately worked out what the motion of 
#the mass particles is, and how all the accelerations balance to make it come out 
#two to one.

#I still remember going to Hans Bethe and saying, ``Hey, Hans! I noticed something 
#interesting. Here the plate goes around so, and the reason it's two to one is ...'' 
#and I showed him the accelerations.

#He says, ``Feynman, that's pretty interesting, but what's the importance of it? 
#Why are you doing it?''

#``Hah!'' I say. ``There's no importance whatsoever. I'm just doing it for the 
#fun of it.'' His reaction didn't discourage me; I had made up my mind I was 
#going to enjoy physics and do whatever I liked.

#I went on to work out equations of wobbles. Then I thought about how electron 
#orbits start to move in relativity. Then there's the Dirac Equation in 
#electrodynamics. And then quantum electrodynamics. And before I knew it (it 
#was a very short time) I was ``playing'' - working, really - with the same 
#old problem that I loved so much, that I had stopped working on when I went
# to Los Alamos: my thesis-type problems; all those old-fashioned, wonderful things.

#It was effortless. It was easy to play with these things. It was like uncorking 
#a bottle: Everything flowed out effortlessly. I almost tried to resist it! 
#There was no importance to what I was doing, but ultimately there was. The 
#diagrams and the whole business that I got the Nobel Prize for came from 
#that piddling around with the wobbling plate."

#Now go find your wobbling plate.
