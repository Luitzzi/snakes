import pygame
import config
from game_utils.snake import Snake
from game_utils.direction import Direction
from game_utils.food import Food


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.snake = Snake()
        self.food = Food()

    def run(self):
        self.screen.fill(config.BG_COLOR)
        while self.running:
            pygame.draw.rect(self.screen, config.FIELD_COLOR, config.FIELD_RECT)
            self.__handle_events()
            self.__update_state()
            self.__is_state_valid()
            self.__draw()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.set_direction(Direction.left)
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction(Direction.right)
                elif event.key == pygame.K_UP:
                    self.snake.set_direction(Direction.up)
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction(Direction.down)

    def __update_state(self):
        self.snake.move()
        self.__handle_eating()

    def __is_state_valid(self):
        new_head = self.snake.body[0]
        if (
            new_head in self.snake.body[1:]
            or new_head[0] < 0
            or new_head[0] >= config.WIDTH
            or new_head[1] < 0
            or new_head[1] >= config.HEIGHT
        ):
            self.running = False

    def __draw(self):
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

    # Helper methods (not called from the run method directly)

    def __handle_eating(self):
        new_head = self.snake.body[0]
        if new_head == self.food.location:
            self.food.respawn()
        else:
            self.snake.body.pop()
