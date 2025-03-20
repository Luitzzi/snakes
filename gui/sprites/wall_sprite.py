from gui.sprites.sprite_utils import load_spritesheet


class WallSprite:
    """
    Holds all Sprites for the walls.
    .
    """

    def __init__(self):
        sprites = load_spritesheet("walls")
        self.top_left = sprites[0][0]
        self.top = sprites[0][1]
        self.top_right = sprites[0][2]
        self.left = sprites[1][0]
        self.bg = sprites[1][1]
        self.right = sprites[1][2]
        self.bot_left = sprites[2][0]
        self.bot = sprites[2][1]
        self.bot_right = sprites[2][2]
