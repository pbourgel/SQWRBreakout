###############################################################################
#                                                                             #
# bounceables.py                                                              #
#                                                                             #
# Class definitions for obhects off of which the ball can bounce              #
#                                                                             #
# Important classes                                                           #
# Wall                                                                        #
# Paddle                                                                      #
# Block                                                                       #
#                                                                             #
# Note also three rules for the game physics.                                 #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################
#AIAR: Angle of incidence equals angle of reflection, or in this 
#case, we multiply one of the dx's or dy's by -1

#WARP; adjust according to where the ball collided

#SPEED: colliding object imparts some speed to the ball when it collides.
#increase the frame rate or scale up the ball movement speed?

#CORNER_ENABLED: If the ball hits in a small space designated the corner, 
#it will multiply both dx and dy by -1.

from constants import *
import pygame

#class Bounceable:
#    def __init__(self):
#        self.prect = pygame.Rect(x, y, width, height)
#        self.color = color

#    def on_collide(self):
#        pass


class Wall():
    def __init__(self, x, y, width, height, axis):
        self.axis = axis
        self.color = BLACK
        self.rect = pygame.Rect(x,y,width,height)

    def on_collide(self):
        return ['AIAR', self.axis]

class Paddle():
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.y, self.x, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ul_corner = pygame.Rect(self.y, self.x + (BALL_WIDTH - 2), 2, 2)       
        self.ur_corner = pygame.Rect(self.y, self.x + (BALL_WIDTH - 2), 2, 2)

    def paddle_rect(self):
        return self.rect

    def on_collide(self, ballrect):
        if pygame.Rect.colliderect(self.ul_corner,ballrect.lr_corner) or pygame.Rect.colliderect(self.ur_corner,ballrect.ll_corner):
            return {'CORNER_ENABLED': ''}
        ball_center = int((ballrect.x + BALL_WIDTH) / 2)
        warp_offset = ball_center - (self.x + (INSIDE_PADDLE_WIDTH / 2))
        return {'WARP': warp_offset / BLOCK_WIDTH}

    def move_paddle(self,direction):
        if direction == '-' and self.x > PADDLE_SPEED:
            self.x -= PADDLE_SPEED
            self.rect.move(PADDLE_SPEED,0)
        elif direction == '+' and (self.x + PADDLE_WIDTH) < (SCREENWIDTH - PADDLE_SPEED):
            self.x += PADDLE_SPEED
            self.rect.move(PADDLE_SPEED,0)

class Block():
    def __init__(self, ccounter, rct):
        self.ccounter = ccounter
        if self.ccounter == 6:
            self.color = CYAN  #Yes, this should be indigo.  I didn't make it indigo because video games.
        elif self.ccounter == 5:
            self.color = BLUE
        elif self.ccounter == 4:
            self.color = GREEN
        elif self.ccounter == 3:
            self.color = YELLOW
        elif self.ccounter == 2:
            self.color = ORANGE
        elif self.ccounter == 1:
            self.color = RED
        elif self.ccounter == 0:
            self.color = BLACK

        self.rect = rct
        self.ul_corner = pygame.Rect(self.rect.y, self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)
        self.ll_corner = pygame.Rect(self.rect.y + (BALL_HEIGHT - CORNER_CONSTANT), self.rect.x, CORNER_CONSTANT, CORNER_CONSTANT)
        self.ur_corner = pygame.Rect(self.rect.y, self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)
        self.lr_corner = pygame.Rect(self.rect.y + (BALL_HEIGHT - CORNER_CONSTANT), self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)

#return CORNER_ENABLED if it hit the corner squares
#else we just do straight angle of incidence equals angle of reflection
#               Now there are four cases we need to test for here
#
#                                 --- I
#                                 | |
#                                 ---
#                            -------------
#                            |           |
#                      IV ---|           |--- II
#                         | ||           || |
#                         ---|           |---
#                            |           |
#                            -------------
#                                 --- III
#                                 | |
#                                 ---
#
# Where (ball.left, ball.top) are the (x, y) coordinates of the ball's upper left corner
# and (paddle.left, paddle.top are the (x, y) coordinates of the block's upper left corner,
# in cases 

#This comes with two constraints
#1. We can't let the ball move so far into the block before calling on_collide that it screws with the logic, so we constrain dx to +- the corner constant
#2. We treat the pixels just inside of the "corner squares" as the edges of the block 

#Hey, here's an idea: In some Breakout/Arkanoid games, they play a short
#beep whenever a collision occurs.  If a bunch of collisions happen in 
#close succession, it's like wind chimes.  Maybe you should add that.

    def on_collide(self,ballrect):
        self.ccounter-=1
        self.change_color()
        if ballrect.collidelist([self.ul_corner,self.ll_corner,self.ur_corner,self.lr_corner]) > -1:
            return {'CORNER_ENABLED': ''}
        else: 
            inner_left_edge = self.x + CORNER_CONSTANT
            inner_right_edge = self.x + BLOCK_WIDTH - CORNER_CONSTANT 
            inner_upper_edge = self.y + CORNER_CONSTANT
            #Not only have I not tested this, I haven't even proved it correct!
            #TO THE BLACKBOARD!!!
            #Case I
            if ballrect.x + BALL_WIDTH >= inner_left_edge and ballrect.x <= inner_right_edge and ballrect.y < inner_upper_edge:
                return {'AIAR': 'y'} # Case I
            elif ballrect.x + BALL_WIDTH >= inner_left_edge and ballrect.x <= inner_right_edge and ballrect.y > inner_upper_edge:
                return {'AIAR': 'y'} # Case III
            else: #Cases II and IV, since the only case that is not a corner collision but is still a collision  is a case where we would reflect on the x axis.
                return {'AIAR': 'x'}

    #Changes the brick color in response to a collision.
    def change_color(self):
        if self.ccounter == 5:
            self.color = BLUE
        elif self.ccounter == 4:
            self.color = GREEN
        elif self.ccounter == 3:
            self.color = YELLOW
        elif self.ccounter == 2:
            self.color = ORANGE
        elif self.ccounter == 1:
            self.color = RED
        elif self.ccounter == 0:
            self.color = BLACK

    #Intentionally leaving this blank
    #Hey, I gotta leave something for other people to build on, right?
    #You might want to create a separate powerup class for this
#    def drop_powerup(self): 
#        pass
