import pygame


class GUI:
    def __init__(self, field_width, field_height, screen_width, screen_height):
        self.field_width = field_width
        self.field_height = field_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.tile_size = self.calc_tile_size()
        self.offset_x = self.calc_offset_x()
        self.offset_y = self.calc_offset_y()
        self.field_rect = self.calc_field_rect()

    def draw_tile(self, screen, x, y, color):
        self.draw_rect(
            screen,
            self.calc_x(x),
            self.calc_y(y),
            self.tile_size,
            self.tile_size,
            color,
        )

    @staticmethod
    def draw_rect(screen, x, y, w, h, color):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, rect)

    def draw_image(self, screen, image, x, y):
        screen.blit(image, (self.calc_x(x), self.calc_y(y)))

    def scale_sprite(self, raw_image):
        return pygame.transform.scale(raw_image, (self.tile_size, self.tile_size))

    def draw_sprite(self, screen, sprite, x, y):
        screen.blit(self.scale_sprite(sprite), (self.calc_x(x), self.calc_y(y)))

    def overlay_sprite(base, top):
        base = base.copy()
        base.blit(top, (0, 0))
        return base

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
