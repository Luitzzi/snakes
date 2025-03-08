
from agent import Agent
from game_ai import GameAI

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0

    agent = Agent()
    game = GameAI

    # Training loop
    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)
        reward = game.play_step(action)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new)
        agent.remember(state_old, action, reward, state_new)
        '''
        if done:
            # Train long memory and plot the results
            game.reset()
            agent.count_games += 1
            agent.train_long_memory()

            if score > best_score
                best_score = best_score
                agent.model.save()

            print(f"Game: {agent.count_games}, Score: {score}, Record: {best_score}")

            # TODO: Plot


if __name__ == '__main__':
    train()
    """
