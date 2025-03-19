import pygame

from defs import TSize
from gui.gui_utils import coord_to_px
from gui.sprites.field_sprite import FieldSprite
from gui.sprites.wall_sprite import WallSprite
from gui.drawers.food_drawer import FoodDrawer
from gui.drawers.snake_drawer import SnakeDrawer
from gui.views.view import View


class GameView(View):
    field: pygame.Surface

    def __init__(self, field_size: TSize, snake_logic, food_logic):
        self.field_sprite = FieldSprite()
        self.wall_sprite = WallSprite()
        self.food_drawer = FoodDrawer(food_logic)
        self.snake_drawer = SnakeDrawer(snake_logic)
        self.field = self.__init_field(field_size)

    def capture(self, scaling_dim) -> pygame.Surface:
        surf = self.field.copy()
        self.food_drawer.draw(surf)
        self.snake_drawer.draw(surf)
        surf = pygame.transform.scale(surf, scaling_dim)
        return surf

    def __init_field(self, field_size) -> pygame.Surface:
        field_res = (
            coord_to_px(field_size.w + 2),
            coord_to_px(field_size.h + 2),
        )
        field = pygame.Surface(field_res)
        self.__draw_field(field, field_size)
        return field

    def __draw_field(self, field, size) -> None:
        # draw corners
        left = coord_to_px(0)
        top = coord_to_px(0)
        right = coord_to_px(size.w + 1)
        bottom = coord_to_px(size.h + 1)
        pos = (left, top)
        field.blit(self.wall_sprite.bg, pos)
        field.blit(self.wall_sprite.top_left, pos)
        pos = (right, top)
        field.blit(self.wall_sprite.bg, pos)
        field.blit(self.wall_sprite.top_right, pos)
        pos = (left, bottom)
        field.blit(self.wall_sprite.bg, pos)
        field.blit(self.wall_sprite.bot_left, pos)
        pos = (left, bottom)
        field.blit(self.wall_sprite.bg, pos)
        field.blit(self.wall_sprite.bot_right, pos)

        # draw top and bottom wall
        for i in range(size.w):
            y = coord_to_px(i + 1)
            pos_top = (left, y)
            field.blit(self.wall_sprite.bg, pos_top)
            field.blit(self.wall_sprite.left, pos_top)
            pos_bot = (right, y)
            field.blit(self.wall_sprite.bg, pos_bot)
            field.blit(self.wall_sprite.right, pos_bot)

        # draw left and right wall
        for i in range(size.h):
            x = coord_to_px(i + 1)
            pos_left = (x, top)
            field.blit(self.wall_sprite.bg, pos_left)
            field.blit(self.wall_sprite.left, pos_left)
            pos_right = (x, bottom)
            field.blit(self.wall_sprite.bg, pos_right)
            field.blit(self.wall_sprite.bot, pos_right)

        # draw grass
        for i in range(size.h):
            for j in range(size.w):
                if (i + j) % 2 == 0:
                    spr = self.field_sprite.dark
                else:
                    spr = self.field_sprite.light
                pos = (coord_to_px(j + 1), coord_to_px(i + 1))
                field.blit(spr, pos)

    ##########
    # Static #
    ##########
