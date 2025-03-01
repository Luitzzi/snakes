from sprites.sprite_utils import Sprite, SpriteVariant, load_spritesheet


class SnakeSprite:
    def __init__(self):
        sprites = load_spritesheet("snake")
        self.head = Sprite(sprites[0][0])
        self.tongue = Sprite(sprites[0][1])
        self.mouth = SpriteVariant(sprites[0][2])
        self.body = Sprite(sprites[1][0])
        self.curve = SpriteVariant(sprites[1][1])
        self.tail = Sprite(sprites[1][2])
        self.eyelids = Sprite(sprites[2][0])
        self.eyelids_smushed = SpriteVariant(sprites[2][1])
        self.head_smushed = SpriteVariant(sprites[2][2])
