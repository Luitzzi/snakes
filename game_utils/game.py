import pygame

import config
from game_utils.snake_logic import SnakeLogic
from game_utils.direction import Direction
from game_utils.game_states import GameStates
from game_utils.food_logic import FoodLogic
from sprites.food_sprite import FoodSprite
from sprites.snake_sprite import SnakeSprite

class Game:
    """
    Class implementing the base logic of the game.
    - The run method implements the game loop calculating and drawing on frame per loop.
    - Score of the game is determined by the time the snake is alive.
    - Game states: game_active, game_over, TODO Landing Page
    """

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.game_state = GameStates.title_screen
        self.start_time = None

        self.snake_logic = SnakeLogic()
        self.snake_sprite = SnakeSprite(self.snake_logic)
        self.food_logic = FoodLogic()
        self.food_sprite = FoodSprite(self.food_logic)

    def run(self):
        self.screen.fill(config.BG_COLOR)
        self.start_time = pygame.time.get_ticks()
        while self.game_running:
            # Game loop
            if self.game_state == GameStates.title_screen:
                pass

            elif self.game_state == GameStates.game_active:
                pygame.draw.rect(self.screen, config.FIELD_COLOR, config.FIELD_RECT)
                self._handle_events()
                self._update_state()
                self._draw()
                pygame.display.flip()
                self.clock.tick(config.FPS)

            elif self.game_state == GameStates.game_over:
                pass

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
        new_direction = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            if event.type == pygame.KEYDOWN:
                # Input for the movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    new_direction = Direction.left
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    new_direction = Direction.right
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    new_direction = Direction.up
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    new_direction = Direction.down
        if new_direction:
            self.snake_logic.set_direction(new_direction)

    def _update_state(self):
        """
        Update the game-state:
        - Make the move based on the direction saved in snake_logic
        - Check if the move results in a collision
        - Check if snake eats
        """
        new_head = self.snake_logic.move()
        if self._is_collision(new_head):
            self.GameStates.game_over
        self._handle_eating()

    def _is_collision(self, new_head):
        """
        Check if the new_head results in a collision.
        The parameter is necessary to get the danger-moves in the training of the ai.
        :param new_head: position of the new head
        :return: bool: True if collision occurred, False if not
        """
        if (
            new_head in self.snake_logic.body[1:]
            or new_head[0] < 0
            or new_head[0] >= config.WIDTH
            or new_head[1] < 0
            or new_head[1] >= config.HEIGHT
        ):
            return True
        else:
            return False

    def _draw(self):
        self.snake_sprite.draw(self.screen)
        self.food_sprite.draw(self.screen)

    # Helper methods (not called from the run method directly)

    def _handle_eating(self):
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.food_logic.respawn(self.snake_logic.body)
        else:
            self.snake_logic.body.pop()

