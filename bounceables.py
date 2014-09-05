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
#If we were to keep this realistic, the only rule in place would be angle
#of incidence equals angle of reflection, but this is video games!  Physics
#is just a suggestion!

#AIAR: Angle of incidence equals angle of reflection, or in this 
#case, we multiply one of the dx's or dy's by -1

#WARP; adjust according to where the ball collided. If the ball collides with
#the left half of the paddle, it should make the ball move left, and vice versa.

#SPEED: colliding object imparts some speed to the ball when it collides.
#increase the frame rate or scale up the ball movement speed?
#I'm leaving this one to the player.  You'll have to refactor 
#Ball.process_collision and Paddle.on_collide, and see what adding it does to
#the game.

#CORNER_ENABLED: If the ball hits in a small space designated the corner, 
#it will multiply both dx and dy by -1.

from __future__ import division #needed in Python 2.7 so we can divide floats without rounding off
from constants import *
import pygame

#Nothing special here, just a surface to bounce off of.
#All we're concerned with is what axis to reflect on
class Wall():
    def __init__(self, x, y, width, height, axis):
        self.axis = axis
        self.color = BLACK
        self.rect = pygame.Rect(x,y,width,height)

    def on_collide(self):
        return {'AIAR': self.axis}

class Paddle():
    def __init__(self, color, x, y):
        self.color = color
        self.rect = pygame.Rect(y,x, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ul_corner = pygame.Rect(y, x + (BALL_WIDTH - 2), 2, 2)       
        self.ur_corner = pygame.Rect(y, x + (BALL_WIDTH - 2), 2, 2)
    #probably unnecessary abstraction around paddle.rect
    def paddle_rect(self):
        return self.rect
    #handles collision.  implements the three main physics rules we want: corner collisions, AIAR, and the warped paddle
    def on_collide(self, ball):
        if pygame.Rect.colliderect(self.ul_corner,ball.lr_corner) or pygame.Rect.colliderect(self.ur_corner,ball.ll_corner):
            return {'CORNER_ENABLED': ''}
        #calculate the warp offset by dividing the difference between the middle of the ball and the middle of the paddle by the block width
        ball_center = ball.rect.midbottom[0]
        warp_offset = (ball_center - self.rect.midtop[0]) / BLOCK_WIDTH
#        print 'in on_collide, warp_offset = ' + str(warp_offset)
        #the fact that this doesn't handle AIAR collisions the same way might lead to a weird bug where 
        #you can hold the ball in the paddle as it jiggles around a little.  Someone should file a 
        #ticket in the Github repo about that
        return {'WARP': warp_offset,'AIAR': 'y'}

#Handles paddle movement.  Checks to make sure the paddle isn't at the left or 
#right-hand sides of the screen first
    def move_paddle(self,direction):
        if direction == '-' and self.rect.x > PADDLE_SPEED and self.rect.x > 0:
            self.rect.move_ip((PADDLE_SPEED*-1),0)
            self.ul_corner.move_ip((PADDLE_SPEED*-1),0)
            self.ur_corner.move_ip((PADDLE_SPEED*-1),0)
        elif direction == '+' and (self.rect.x + PADDLE_WIDTH) < SCREENWIDTH:
            self.rect.move_ip(PADDLE_SPEED,0)
            self.ul_corner.move_ip((PADDLE_SPEED),0)
            self.ur_corner.move_ip((PADDLE_SPEED),0)

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

        #This is the rectangle that gets drawn in the game loop
        self.rect = rct
        #This is worked out to handle the corner collision rule
        self.ul_corner = pygame.Rect(self.rect.y, self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)
        self.ll_corner = pygame.Rect(self.rect.y + (BALL_HEIGHT - CORNER_CONSTANT), self.rect.x, CORNER_CONSTANT, CORNER_CONSTANT)
        self.ur_corner = pygame.Rect(self.rect.y, self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)
        self.lr_corner = pygame.Rect(self.rect.y + (BALL_HEIGHT - CORNER_CONSTANT), self.rect.x + (BALL_WIDTH - CORNER_CONSTANT), CORNER_CONSTANT, CORNER_CONSTANT)

#return CORNER_ENABLED if it hit the corner squares
#else we just do straight angle of incidence equals angle of reflection
#to figure out which axis to reflect the ball on, calculate the ball's position
#one dx in the opposite direction.  If that collides with the block, then it means
#we need to go dy y coordinates back, else we reflect on the x axis.

#This comes with one constraint
#1. We can't let the ball move so far into the block before calling on_collide that it screws with the logic, so we constrain BALL_SPEED to +- the smallest dimension of the block.


#Hey, here's an idea: In some Breakout/Arkanoid games, they play a short
#beep whenever a collision occurs.  If a bunch of collisions happen in 
#close succession, it's like wind chimes.  Maybe you should add that.

    def on_collide(self,ball):
        self.ccounter-=1
        self.change_color()
        if pygame.Rect.colliderect(self.ll_corner, ball.ur_corner) or pygame.Rect.colliderect(self.ul_corner,ball.lr_corner) or pygame.Rect.colliderect(self.ur_corner, ball.ll_corner) or pygame.Rect.colliderect(self.lr_corner,ball.ul_corner):
            return {'CORNER_ENABLED': ''}
        else: 
            if self.rect.colliderect(ball.rect.move(ball.dx*-1,ball.dy)):
                return {'AIAR': 'y'}
            else:
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
#        pass                    ballrect.move(0,1)
