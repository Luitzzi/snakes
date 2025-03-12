from networkx.algorithms.tournament import score_sequence

from agent import Agent
from game_ai import GameAI
from ai.plotter import plot

def train():
    # Statistical data
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
        reward, is_running = game.play_step(action)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, is_running)
        agent.remember(state_old, action, reward, state_new, is_running)

        if not is_running:
            # Train long memory and plot the results
            game.reset(game)
            agent.count_games += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = best_score
                agent.model.save()

            print(f"Game: {agent.count_games}, Score: {score}, Record: {best_score}")

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.count_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()

