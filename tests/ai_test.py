import pygame
import unittest
from typing import override

import config
from ai.agent import Agent
from ai.game_ai import GameAI
from ai.agent_action import AgentAction

class GameAI_Test(GameAI):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.agent = Agent()

    @override
    def run(self):
        self.gui.screen.fill(config.BG_COLOR)
        self.time_alive = pygame.time.get_ticks()
        while self.game_running:
            self.__handle_events()
            # ai-agent interaction
            self.play_step(AgentAction.stay_straight)
            # draw the game
            self._game_active_logic()

            state = self.agent.get_state(self)
            print(f"headpos: {self.snake_logic.get_head()}"
                  f"dangerous positions: {state[:3]};"
                  f"current direction: {state[3:7]}"
                  f"food direction: {state[7:12]}")
            input()

        pygame.quit()


class TestAi(unittest.TestCase):

    def setUp(self):
        self.game = GameAI_Test(5,5)

    def test_get_state(self):
        self.game.run()


