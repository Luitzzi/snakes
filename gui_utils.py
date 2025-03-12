import pygame

import config


class GUI:

class GuiUtils:
    def __init__(self, field_width, field_height, screen_width, screen_height):
        self.field_width = field_width
        self.field_height = field_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.tile_size = self.__calc_tile_size()
        self.offset_x = self.__calc_offset_x()
        self.offset_y = self.__calc_offset_y()
        self.field_rect = self.__calc_field_rect()
        self.screen = self.__init_screen()
        self.__init_field()
        self.__init_fonts()


    def draw_tile(self, x, y, color):
        self.draw_rect(
            self.__calc_x(x),
            self.__calc_y(y),
            self.tile_size,
            self.tile_size,
            color,
        )

    def draw_rect(self, x, y, w, h, color):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, color, rect)

    def draw_image(self, screen, image, x, y):
        screen.blit(image, (self.__calc_x(x), self.__calc_y(y)))

    def scale_sprite(self, raw_image):
        return pygame.transform.scale(raw_image, (self.tile_size, self.tile_size))

    def draw_sprite(self, screen, sprite, x, y):
        screen.blit(self.scale_sprite(sprite), (self.__calc_x(x), self.__calc_y(y)))

    def overlay_sprite(self, base, top):
        base = base.copy()
        base.blit(top, (0, 0))
        return base

    def draw_element_field(self, element, x, y):
        """
        Draws an element onto a position on the field using the field coords.
        The element has to be a square
        :param element: Element that should be drawn
        :param x: X pos
        """
        if element.get_width() != element.get_height():
            raise ValueError(f'Excepted element, needs to be a square')
        self.screen.blit(element, (self.__calc_x(x), self.__calc_y(y)))

    def draw_element_screen(self, element, x, y):
        """
        Draws an element centered at (x,y) using screen pixel.
        :param element: Element that should be drawn
        :param x: X pos of the center of the image in pixel
        :param y: Y pos of the center of the image in pixel
        """
        rect = element.get_rect()
        rect.center = (x, y)
        self.screen.blit(element, rect)


    def __init_screen(self):
        return pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

    def __init_field(self):
        self.tile_size = self.__calc_tile_size()
        self.offset_x = self.__calc_offset_x()
        self.offset_y = self.__calc_offset_y()
        self.field_rect = self.__calc_field_rect()

    def __init_fonts(self):
        self.heading = pygame.font.Font(config.PIXEL_FONT_PATH, 32)
        self.subheading = pygame.font.Font(config.PIXEL_FONT_PATH, 20)
        self.text = pygame.font.Font(config.PIXEL_FONT_PATH, 15)

    def __calc_field_rect(self):
        return pygame.Rect(
            self.offset_x,
            self.offset_y,
            self.field_width * self.tile_size,
            self.field_height * self.tile_size,
        )

    def __calc_tile_size(self):
        return int(
            min(
                self.screen_width / self.field_width,
                self.screen_height / self.field_height,
            )
        )

    def __calc_offset_x(self):
        return int((self.screen_width - self.field_width * self.tile_size) / 2)

    def __calc_offset_y(self):
        return int((self.screen_height - self.field_height * self.tile_size) / 2)

    def __calc_x(self, x):
        """
        Calculate the pixel position from the position on the game field.
        """
        return self.offset_x + x * self.tile_size

    def __calc_y(self, y):
        """
        Calculate the pixel position from the position on the game field.
        """
        return self.offset_y + y * self.tile_size
