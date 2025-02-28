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
            self._handle_events()  # Always necessary for the QUIT event

            # Process the logic for the current state
            # TODO: Restrict the logic of the game_active state to 10 fps (more and the snake took speed)
            if self.game_state == GameStates.title_screen:
                self.__title_screen_logic()
            elif self.game_state == GameStates.game_active:
                self.__game_active_logic()
            elif self.game_state == GameStates.game_over:
                self.__game_over_logic()
        pygame.quit()

    #########
    # Game states logic
    ########

    def __title_screen_logic(self):
        self.game_state = GameStates.game_active
        self.start_time = pygame.time.get_ticks()  # Necessary to evaluate the score

    def __game_active_logic(self):
        pygame.draw.rect(self.screen, config.FIELD_COLOR, config.FIELD_RECT)
        self._update_state()
        self._draw()
        pygame.display.flip()
        self.clock.tick(config.FPS)

    def __game_over_logic(self):
        pass

    #########
    # Handle input events
    ########

    def _handle_events(self):
        """
        Handles all input events:
        - Always checks for QUIT
        - Afterward, it checks specifically the inputs from the different game states.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            if self.game_state == GameStates.game_active:
                self.__handle_game_active_input(event)
            if self.game_state == GameStates.game_over:
                self.__handle_game_over_input(event)

    def __handle_game_active_input(self, event):
        """
        Handles the input that occurs during the time the player plays the game.
        Input possibilities are w/UP , s/DOWN , a/LEFT , d/RIGHT
        :param event: Input event from the player
        """
        new_direction = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                new_direction = Direction.WEST
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                new_direction = Direction.EAST
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                new_direction = Direction.NORTH
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                new_direction = Direction.SOUTH
        if new_direction:
            self.snake_logic.set_direction(new_direction)

    def __handle_game_over_input(self, event):
        pass

    #########
    # Other game-loop methods
    ########

    def _update_state(self):
        """
        Update the game-state:
        - Make the move based on the direction saved in snake_logic
        - Check if the move results in a collision
        - Check if snake eats
        """
        new_head = self.snake_logic.move()
        if self._is_collision(new_head):
            self.game_state = GameStates.game_over
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

    #########
    # Helper methods
    ########

    def _handle_eating(self):
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.food_logic.respawn(self.snake_logic.body)
        else:
            self.snake_logic.body.pop()

    def get_time_since_start(self):
        """
        Returns how long the player is playing in the game_active state
        :return: int representing the time in seconds
        """
        if self.start_time is None:
            return None
        else:
            running_time_millis = pygame.time.get_ticks() - self.start_time
            return running_time_millis // 1000
