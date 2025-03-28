import pygame

import config
from gui.gui import Gui
from defs import Collision, Direction
from game.food_logic import FoodLogic
from game.game_states import GameStates
from game.snake_logic import SnakeLogic
from gui.drawers.snake_drawer import calc_direction


class Game:
    """
    Class implementing the base logic of the game.
    - The run method implements the game loop calculating and drawing on frame per loop.
    - Score of the game is determined by the time the snake is alive.
    - Game states: game_active, game_over, TODO Landing Page
    """

    def __init__(self, field_width, field_height):
        self.field_size = (field_width, field_height)
        # Setup game logic
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.game_state = GameStates.title_screen
        self.start_time = None

        # Setup game elements
        self.snake_starting_position = Game.calc_starting_position(
            self.field_size[0], self.field_size[1]
        )
        self.snake_logic = SnakeLogic(self.snake_starting_position)
        self.food_logic = FoodLogic(
            self.snake_starting_position, self.field_size[0], self.field_size[1]
        )
        self.gui = Gui(self)

    def run(self):
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

            self.gui.draw()
        pygame.quit()

    #########
    # Game states logic
    ########

    def __title_screen_logic(self):
        self.game_state = GameStates.game_active
        self.start_time = (
            pygame.time.get_ticks()
        )  # Necessary after the change to game_active to evaluate the score

    def __game_active_logic(self):
        self._update_state()
        self._draw_field_objects()
        self.clock.tick(config.FPS)

    def __game_over_logic(self):
        self._draw_field_objects()
        self.clock.tick(config.FPS)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake_logic.set_direction(Direction.WEST)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake_logic.set_direction(Direction.EAST)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake_logic.set_direction(Direction.NORTH)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake_logic.set_direction(Direction.SOUTH)

    def __handle_game_over_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Restart the game
                self.snake_logic = SnakeLogic(self.snake_starting_position)
                self.gui.game_restarted()
                self.game_state = GameStates.game_active
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                self.game_running = False

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
        old_tail = self._handle_eating()
        if self._is_collision(new_head):
            self.game_state = GameStates.game_over
            # moving snake back when hitting wall, so it does not clip into wall
            if self.snake_logic.collided_with not in (
                Collision.TAIL,
                Collision.BODY,
                Collision.CURVE,
            ):
                self.snake_logic.body.pop(0)
                self.snake_logic.body.append(old_tail)

    def _is_collision(self, new_head):
        """
        Check if the new_head results in a collision.
        Also passes collision information to SnakeLogic.
        The parameter is necessary to get the danger-moves in the training of the ai.
        :param new_head: position of the new head
        :return: bool: True if collision occurred, False if not
        """
        if new_head in self.snake_logic.body[1:]:
            if new_head == self.snake_logic.body[-1]:
                self.snake_logic.collide(Collision.TAIL)
            else:
                i = self.snake_logic.body[1:].index(new_head) + 1
                first_dir = calc_direction(
                    self.snake_logic.body[i - 1], self.snake_logic.body[i]
                )
                second_dir = calc_direction(
                    self.snake_logic.body[i], self.snake_logic.body[i + 1]
                )
                if first_dir == second_dir:
                    self.snake_logic.collide(Collision.BODY)
                else:
                    self.snake_logic.collide(Collision.CURVE)
        elif new_head[0] < 0:
            self.snake_logic.collide(Collision.LEFT)
        elif new_head[0] >= self.field_size[0]:
            self.snake_logic.collide(Collision.RIGHT)
        elif new_head[1] < 0:
            self.snake_logic.collide(Collision.TOP)
        elif new_head[1] >= self.field_size[1]:
            self.snake_logic.collide(Collision.BOTTOM)
        else:
            return False
        return True

    def _draw_field_objects(self):
        """
        Draw all objects located on the field.
        Snake, food.
        """

    #########
    # Helper methods
    ########

    def calc_starting_position(width, height):
        x_pos = (width // 4, height // 2)
        y_pos = (width // 4 - 1, height // 2)
        return (x_pos, y_pos)

    def _handle_eating(self):
        self.snake_logic.set_food_pos(self.food_logic.location)
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.food_logic.respawn(self.snake_logic.body)
            return None
        else:
            return self.snake_logic.body.pop()

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
