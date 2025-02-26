from sprites.snake_sprite import SnakeSprite
from sprites.sprite_utils import get_sprite_dir, get_sprite_wiggle


class SnakeDrawer:
    def __init__(self, gui, snake_logic):
        self.gui = gui
        self.logic = snake_logic
        self.sprites = SnakeSprite()

    def draw(self, screen):
        last_index = len(self.logic.body) - 1
        for i, segment in enumerate(self.logic.body):
            wiggle = (self.logic.wiggle_offset + i) % 2

            if i == 0:
                spr = get_sprite_wiggle(wiggle, self.sprites.head)
                spr = get_sprite_dir(self.logic.direction, spr)
            elif i == last_index:
                spr = get_sprite_wiggle(wiggle, self.sprites.tail)
                spr = get_sprite_dir(self.logic.direction, spr)
            else:
                spr = get_sprite_wiggle(wiggle, self.sprites.body)
                spr = get_sprite_dir(self.logic.direction, spr)

            self.gui.draw_sprite(screen, spr, segment[0], segment[1])
