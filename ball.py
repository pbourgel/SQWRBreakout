import pygame
from constants import *

#AIAR: Angle of incidence equals angle of reflection, or in this 
#case, we multiply one of the dx's or dy's by -1

#WARP; adjust according to where the ball collided

#SPEED: colliding object imparts some speed to the ball when it collides.
#increase the frame rate or scale up the ball movement speed?
#For this case I'm just going to increase the frame rate, which means
#it doesn't make much sense to handle it as a Ball class method.
#This will be handled in breakout.py

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
        self.ul_corner = pygame.Rect(self.y, self.x, 2, 2)
        self.ll_corner = pygame.Rect(self.y + (BALL_HEIGHT - 2), self.x, 2, 2)
        self.ur_corner = pygame.Rect(self.y, self.x + (BALL_WIDTH - 2), 2, 2)
        self.lr_corner = pygame.Rect(self.y + (BALL_HEIGHT - 2), self.x + (BALL_WIDTH - 2), 2, 2)

    def get_corners(self):
        return self.ul_corner

    #move the x and y coordinates by dx and dy
    #update a few other things 
    def update_position(self):
#        self.x += self.dx
#        self.y += self.dy
#        self.rect = pygame.Rect(self.y, self.x, BALL_WIDTH, BALL_HEIGHT)
#        self.ul_corner = pygame.Rect(self.y, self.x, 2, 2)
#        self.ll_corner = pygame.Rect(self.y + (BALL_HEIGHT - 2), self.x, 2, 2)
#        self.ur_corner = pygame.Rect(self.y, self.x + (BALL_WIDTH - 2), 2, 2)
#        self.lr_corner = pygame.Rect(self.y + (BALL_HEIGHT - 2), self.x + (BALL_WIDTH - 2), 2, 2)
         self.rect.move_ip(dx,dy)
         self.ul_corner.move_ip(dx,dy)
         self.ll_corner.move_ip(dx,dy)
         self.ur_corner.move_ip(dx,dy)
         self.lr_corner.move_ip(dx,dy)

    def ball_rect(self):
        return self.rect    

    #Handles the change in ball slope when we just need to 
    #reflect it according to the rule that angle of incidence
    #equals angle of reflection.  This will involve multiplying
    #either dx or dy by -1.
    def reflect_aiar(self, axis):
        if axis == 'x':
            self.dx *= -1
        elif axis == 'y':
            self.dy *= -1
        #And if you ever use this code as the basis for 3D Breakout,
        #I guess your code to reflect on the z axis might be here too.
        #I'm too dumb for >2D Breakout.

    #This is to handle a collison with the paddle.  Since the 
    #paddle is a pixel-perfectly flat surface, we want it to
    #warp it a little bit, else we'll just have a ball going straight
    #up and straight down, and that's no fun.
    #However, for reasons discussed over in the block collision code in bounceables.py,
    # we need to restrict dx to -2 < dx < 2.
    def reflect_warp(self,adjustment):
        if self.dx + adjustment >= (CORNER_CONSTANT*-1) and self.dx+ adjustment <= CORNER_CONSTANT:
            self.dx += adjustment

    def reflect_corner(self):
        self.dx *= -1
        self.dy *= -1

    def process_collision(self,rules,block=None):
        if 'AIAR' in rules:
            self.reflect_aiar(rules['AIAR'])
        if 'WARP' in rules:
            self.reflect_warp(rules['WARP'])
        if 'CORNER_ENABLED' in rules:
            self.reflect_corner()

