###############################################################################
#                                                                             #
# levels.py                                                                   #
#                                                                             #
# Contains all the code for reading and generating levels.  Later developers  #
# could add code to load these as a CSV file, or tweak it so the blocks have  #
# special properties other than changing color.                               #
#                                                                             #
# Important classes:                                                          #
# LevelFactory: Takes an array of numbers and "manufactures" Block objects.   #
#                                                                             #
#                                                                             #
###############################################################################

from constants import *
from bounceables import *

#Think of this as two coordinate systems.  There is the 
#coordinate system we have to draw pixels on the screen, and there is the 
#coordinate system of the blocks.  A block with coordinates (1,1), or the 
#second from the left and one down, in the block system will have coordinates 
#(BLOCK_WIDTH,BLOCK_HEIGHT) in the regular pixel drawing system.  Sometimes 
#games in Pygame will switch between the two systems, but in this game, while 
#the block system is implied when reading the level data, the LevelFactory class 
#immediately converts to the pixel drawing system.

level = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,6,0,
0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,6,0,
0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,6,0,
0,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,6,0,6,0,6,0,0,
0,0,0,0,0,0,6,0,0,0,6,6,6,0,6,6,6,0,0,0,6,0,6,0,6,0,6,0,0,
0,0,0,0,0,0,6,0,0,0,6,0,6,0,6,0,6,0,0,0,6,0,6,0,6,0,6,0,0,
0,0,0,0,0,0,6,0,0,0,6,6,6,0,6,6,6,0,0,0,0,6,0,0,0,6,0,0,0,
0,6,6,6,6,6,6,0,0,0,0,6,0,0,0,6,0,0,0,0,0,6,0,0,0,6,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,6,6,6,6,6,6,0,0,6,6,6,6,6,6,6,6,6,0,0,0,6,6,6,6,6,0,0,0,
0,6,0,0,0,0,6,0,0,6,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,6,0,0,0,
0,6,0,0,0,0,6,0,0,6,0,0,0,6,0,0,0,6,0,0,0,6,0,0,0,6,0,0,0,
0,6,0,0,0,0,6,0,0,6,0,0,6,0,6,0,0,6,0,0,0,6,0,0,0,6,0,0,0,
0,6,0,0,6,0,6,0,0,6,0,6,0,0,0,6,0,6,0,0,0,6,6,6,6,6,0,0,0,
0,6,0,0,0,6,6,0,0,6,0,6,0,0,0,6,0,6,0,0,0,6,0,0,6,0,0,0,0,
0,6,6,6,6,6,6,0,0,6,0,6,0,0,0,6,0,6,0,0,0,6,0,0,0,6,0,0,0,
0,0,0,0,0,0,0,6,0,6,6,6,0,0,0,6,6,6,0,0,0,6,0,0,0,0,6,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

#Simple "factory" class to read an array of numbers and 
#generate matching Block classes.
#The numbers correspond to the value of the "color counter"
#on the block.  As defined in bounceables.py,
#6 = CYAN
#5 = BLUE
#4 = GREEN
#3 = YELLOW
#2 = ORANGE
#1 = RED
#0 = BLACK (the background color)
class LevelFactory:

    def __init__(self):
        self.block_array = []
        vertical_offset_index = 0
        for x in range(0,len(level)):
            if (x % BLOCKS_ACROSS) == 0:
                vertical_offset_index+=1 #This gets us an idea of how far down the y coordinate of the block should be without another for loop

#This creates a new Block object and appends it to the block array.  The arguments are generated like this:
#1. Color, as indicated by the mapping above
#2. A rectangle object, which has:
#2.a. A left-hand x coordinate computed by the block's block x coordinate times the block width
#2.b. A top y coordinate computed from the block's y coordinate (vertical_offset_index) times the block height
#3. the block width
#4. the block height
            self.block_array.append(Block(level[x],pygame.Rect(((x % (BLOCKS_ACROSS))*BLOCK_WIDTH,(vertical_offset_index*BLOCK_HEIGHT),BLOCK_WIDTH,BLOCK_HEIGHT))))

