from pathlib import Path
from defs import Direction

# General settings
FPS = 5
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_RES = (600, 400)

# Sprites
SPRITE_PATH = "./assets/sprites/"
SPRITE_FILE_ENDING = ".png"
SPRITE_SIZE = 16  # 16px x 16px

# Colors
SNAKE_COLOR = (50, 100, 150)
FOOD_COLOR = (200, 60, 40)
FIELD_COLOR = (200, 220, 150)
BG_COLOR = (50, 50, 70)
TEXT_COLOR = (0, 0, 0)

# Images
ROOT_DIR = Path(__file__).resolve().parent  # Gets the directory of the current script
TOMATO_IMAGE_PATH = ROOT_DIR / "assets" / "images" / "apple.png"

# Fonts
PIXEL_FONT_PATH = ROOT_DIR / "assets" / "fonts" / "PixelifySans-VariableFont_wght.ttf"

# Game starting position
SNAKE_DEFAULT_DIRECTION = Direction.EAST
