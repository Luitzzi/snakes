import pygame

import config
import ai.ai_config as ai_config
from ai.agent import Agent
from ai.game_ai import GameAI
from ai.plotter import Plotter

def train():
    pygame.init()
    game = GameAI(ai_config.FIELD_WIDTH,ai_config.FIELD_HEIGHT)
    game.gui.screen.fill(config.BG_COLOR)
    agent = Agent(game)
    plotter = Plotter()

    while True:
        # Training loop
        state_old = agent.get_state()
        action = agent.get_action(state_old)
        reward = game.play_step(action)
        state_new = agent.get_state()
        terminated = game.terminated

        agent.train_short_memory(state_old, action, reward, state_new, terminated)
        agent.safe_experience(state_old, action, reward, state_new, terminated)

        if terminated:
            game.num_episodes += 1
            plotter.update_score(game.score, game.num_episodes)
            agent.train_long_memory()

            print(f"Game: {game.num_episodes}, Score: {game.score}, Record: {plotter.best_score}")

            game.reset()
            plotter.plot(agent.epsilon)
