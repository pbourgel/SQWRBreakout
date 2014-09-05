###############################################################################
#                                                                             #
# ball.py                                                                     #
#                                                                             #
# Contains much of the important code for the ball collison                   #
# could add code to load these as a CSV file, or tweak it so the blocks have  #
# special properties other than changing color.                               #
#                                                                             #
# Important classes:                                                          #
# LevelFactory: Takes an array of numbers and "manufactures" Block objects.   #
#                                                                             #
#                                                                             #
###############################################################################


import pygame
import math
from constants import *

#AIAR: Angle of incidence equals angle of reflection, or in this 
#case, we multiply one of the dx's or dy's by -1

#WARP; adjust according to where the ball collided

#SPEED: colliding object imparts some speed to the ball when it collides.
#increase the frame rate or scale up the ball movement speed?
#I'm leaving this one to the player.  You'll have to refactor 
#Ball.process_collision and Paddle.on_collide, and see what adding it does to
#the game.

#CORNER_ENABLED: If the ball hits in a small space designated the corner, 
#it will multiply both dx and dy by -1.


class Ball:
    def __init__(self, color, x, y, dx, dy):
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(self.y, self.x, BALL_WIDTH, BALL_HEIGHT)
        
        self.ul_corner = pygame.Rect(self.y, self.x, CORNER_CONSTANT, CORNER_CONSTANT)
        self.ll_corner = pygame.Rect(self.y + (BALL_HEIGHT - CORNER_CONSTANT), self.x, CORNER_CONSTANT, CORNER_CONSTANT)
        self.ur_corner = pygame.Rect(self.y, self.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)
        self.lr_corner = pygame.Rect(self.y + (BALL_HEIGHT - CORNER_CONSTANT), self.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)

    #move the x and y coordinates by dx and dy
    #update a few other things 
    #a quick note, since the pygame documentation confused me a little:
    #move returns a new rectangle object with the new position
    #move_ip changes the state of the existing rectangle object so that the top left corner has coordinates (x+dx,y+dy)
    def update_position(self):
         self.rect.move_ip(self.dx,self.dy)
         self.ul_corner.move_ip(self.dx,self.dy)
         self.ll_corner.move_ip(self.dx,self.dy)
         self.ur_corner.move_ip(self.dx,self.dy)
         self.lr_corner.move_ip(self.dx,self.dy)

    #Probably unnecessary abstraction
    def ball_rect(self):
        return self.rect    

    #Handles the change in ball slope when we just need to 
    #reflect it according to the rule that angle of incidence
    #equals angle of reflection.  This will involve multiplying
    #either dx or dy by -1.
    def reflect_aiar(self, axis):
        if axis == 'x':
            self.dx *= -1
            #self.update_position()
        elif axis == 'y':
            self.dy *= -1
            #self.update_position()        
        #And if you ever use this code as the basis for 3D Breakout,
        #I guess your code to reflect on the z axis might be here too.
        #I'm too dumb for >2D Breakout.

    #This is to handle a collison with the paddle.  Since the 
    #paddle is a pixel-perfectly flat surface, we want it to
    #warp it a little bit, else we'll just have a ball going straight
    #up and straight down, and that's no fun.
    #However, for reasons discussed over in the block collision code in bounceables.py,
    # we need to restrict dx to -BALL_SPEED < dx < BALL_SPEED.
    def reflect_warp(self,adjustment):
        if adjustment > -1 and adjustment < 0 and self.dx == 0:
            adjustment = math.floor(adjustment)
        if adjustment > 0 and adjustment < 1 and self.dx == 0:
            adjustment = math.ceil(adjustment)

        if self.dx + adjustment > -BALL_SPEED and self.dx + adjustment < BALL_SPEED:
            self.dx += adjustment
        elif self.dx + adjustment < -BALL_SPEED:
            self.dx = -BALL_SPEED
        elif self.dx + adjustment > BALL_SPEED:
            self.dx = BALL_SPEED

        if self.dx < 0 and self.dx > -1:
            self.dx = -1
        if self.dx > 0 and self.dx < 1:
            self.dx = 1
        #print 'in reflect_warp:' + str(self.dx)

    #If it reflects off a specific corner (defined in the block collide code),
    #we want it to completely reverse dx and dy
    def reflect_corner(self):
        self.dx *= -1
        self.dy *= -1

    #Handles calls to the different reflection functions.
    #You will want to handle paddle speed reflection here
    def process_collision(self,rules):
        if 'AIAR' in rules:
            self.reflect_aiar(rules['AIAR'])
        if 'WARP' in rules:
            #print 'In WARP, offset value: ' + str(rules['WARP'])
            self.reflect_warp(rules['WARP'])
        if 'CORNER_ENABLED' in rules:
            self.reflect_corner()

