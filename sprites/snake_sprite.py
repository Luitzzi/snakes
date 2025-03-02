from sprites.sprite_utils import load_spritesheet
from sprites.sprite_utils import Sprite, SpriteVariant, SpriteVariantList


class SnakeSprite:
    def __init__(self):
        sprites = load_spritesheet("snake")
        self.head = Sprite(sprites[0][0])
        self.tongue = Sprite(sprites[0][1])
        self.mouth = SpriteVariant(sprites[0][2])
        self.hit_body = SpriteVariant(sprites[0][3])
        self.hit_wall = SpriteVariant(sprites[1][0])
        self.hit_side = Sprite(sprites[1][1])
        self.body = Sprite(sprites[1][2])
        self.curve = SpriteVariant(sprites[1][3])
        self.tail = Sprite(sprites[2][0])
        self.eyelids = Sprite(sprites[2][1])
        self.dizzy = SpriteVariantList(sprites[2][2:] + sprites[3])
