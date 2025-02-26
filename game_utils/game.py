import pygame

import config
from game_utils.snake_logic import SnakeLogic
from game_utils.direction import Direction
from game_utils.food_logic import FoodLogic
from sprites.food_sprite import FoodSprite
from sprites.snake_sprite import SnakeSprite

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.start_time = None

        self.snake_logic = SnakeLogic()
        self.snake_sprite = SnakeSprite(self.snake_logic)
        self.food_logic = FoodLogic()
        self.food_sprite = FoodSprite(self.food_logic)

    def run(self):
        self.screen.fill(config.BG_COLOR)
        self.start_time = pygame.time.get_ticks()
        while self.running:
            pygame.draw.rect(self.screen, config.FIELD_COLOR, config.FIELD_RECT)
            self._handle_events()
            self._update_state()
            self._is_state_valid()
            self._draw()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()

    def get_time_since_start(self):
        """
        Returns the time until the game-loop, therefore the game started in milliseconds
        :return: int representing milliseconds
        """
        if self.start_time == None:
            return None
        else:
            running_time_milis = pygame.time.get_ticks() - self.start_time
            return running_time_milis // 1000

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake_logic.set_direction(Direction.left)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake_logic.set_direction(Direction.right)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake_logic.set_direction(Direction.up)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake_logic.set_direction(Direction.down)

    def _update_state(self):
        self.snake_logic.move()
        self._handle_eating()

    def _is_state_valid(self):
        new_head = self.snake_logic.body[0]
        if (
            new_head in self.snake_logic.body[1:]
            or new_head[0] < 0
            or new_head[0] >= config.WIDTH
            or new_head[1] < 0
            or new_head[1] >= config.HEIGHT
        ):
            self.running = False

    def _draw(self):
        self.snake_sprite.draw(self.screen)
        self.food_sprite.draw(self.screen)

    # Helper methods (not called from the run method directly)

    def _handle_eating(self):
        new_head = self.snake_logic.body[0]
        if new_head == self.food_logic.location:
            self.food_logic.respawn(self.snake_logic.body)
        else:
            self.snake_logic.body.pop()

