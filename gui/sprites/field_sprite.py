from gui.sprites.sprite_utils import load_spritesheet


class FieldSprite:
    """
    Holds all Sprites for the field.
    .
    """

    def __init__(self):
        sprites = load_spritesheet("field")
        self.light = sprites[0][0]
        self.dark = sprites[0][1]
