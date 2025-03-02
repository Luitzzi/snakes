from sprites.sprite_utils import load_spritesheet
from sprites.sprite_utils import Sprite, SpriteVariant, SpriteVariantList


class SnakeSprite:
    def __init__(self):
        sprites = load_spritesheet("snake")
        self.head = SpriteVariant(sprites[0][0])
        self.mouth = SpriteVariant(sprites[0][1])
        self.tongue = SpriteVariant(sprites[0][2])
        self.body = Sprite(sprites[0][3])
        self.curve = SpriteVariant(sprites[0][4])
        self.tail = Sprite(sprites[0][5])
        self.hit_body = SpriteVariant(sprites[1][0])
        self.hit_tail = Sprite(sprites[1][1])
        self.hit_curve = Sprite(sprites[1][2])
        self.hit_wall = SpriteVariant(sprites[1][3])
        self.hit_side = Sprite(sprites[1][4])
        self.eyelids = SpriteVariant(sprites[1][5])
        self.dizzy_eyes = SpriteVariantList(sprites[2])
