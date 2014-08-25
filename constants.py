###############################################################################
#                                                                             #
# constants.py                                                                #
#                                                                             #
# contains config variables for the dimensions of the blocks, paddle, ball(s),#
# screen size, colors, number of blocks per level, and some constants for the #
# "physics"                                                                   #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

#FPS = 30
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN  = (0, 255, 255)
SCREENWIDTH = 870
SCREENHEIGHT = 700

BLOCKS_ACROSS = 29
BLOCKS_DOWN = 20

#It's all derived from the dimensions of the block.
#Ball should be 1/3rd block width x 1/3rd block width
#paddle 2 blocks by 1, but with enough area for 
#"corner squares"
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 15
CORNER_CONSTANT = 2

BALL_WIDTH = BLOCK_WIDTH / 3 
BALL_HEIGHT = BLOCK_WIDTH / 3

PADDLE_WIDTH = (BLOCK_WIDTH * 2) + (2 * CORNER_CONSTANT) + 1
INSIDE_PADDLE_WIDTH = (BLOCK_WIDTH * 2)
PADDLE_HEIGHT = BLOCK_HEIGHT
PADDLE_TOP = SCREENHEIGHT - (BLOCK_HEIGHT * 5)
PADDLE_LEFT = (SCREENWIDTH / 2) - BLOCK_WIDTH
PADDLE_SPEED = 5

BALL_TOP = PADDLE_TOP - (BLOCK_HEIGHT * 2)
BALL_LEFT = PADDLE_LEFT + (BLOCK_WIDTH - 5)
