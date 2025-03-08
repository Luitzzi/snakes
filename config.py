from pathlib import Path
from game_utils.direction import Direction

# General settings
FPS = 5
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
SNAKE_COLOR = (50, 100, 150)
FOOD_COLOR = (200, 60, 40)
FIELD_COLOR = (200, 220, 150)
BG_COLOR = (50, 50, 70)

# Images
ROOT_DIR = Path(__file__).resolve().parent # Gets the directory of the current script
TOMATO_IMAGE_PATH = ROOT_DIR / "assets" / "apple.png"

# Game starting position
SNAKE_DEFAULT_DIRECTION = Direction.EAST
def calc_starting_position(field_width, field_height):
    return ((field_width // 4, field_height // 2),
            (field_width // 4 - 1, field_height // 2))