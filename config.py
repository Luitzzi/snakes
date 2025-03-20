from pathlib import Path
from game.game_objects.direction import Direction

####################
# General settings #
####################

FPS = 50
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
SNAKE_COLOR = (50, 100, 150)
FOOD_COLOR = (200, 60, 40)
FIELD_COLOR = (200, 220, 150)
BG_COLOR = (50, 50, 70)
TEXT_COLOR = (0, 0, 0)


# Game starting position
SNAKE_DEFAULT_DIRECTION = Direction.EAST
def calc_starting_position(field_width, field_height):
    return ((field_width // 4, field_height // 2),
            (field_width // 4 - 1, field_height // 2))

#########
# Paths #
#########
ROOT_DIR = Path(__file__).resolve().parent # Gets the directory of the current script

# Images
TOMATO_IMAGE_PATH = ROOT_DIR / "assets" / "images" / "apple.png"

# Fonts
PIXEL_FONT_PATH = ROOT_DIR / "assets" / "fonts" / "PixelifySans-VariableFont_wght.ttf"

# AI model
SAVE_MODEL_PATH = ROOT_DIR / "ai" / "models"
