import matplotlib.pyplot as plt
from IPython import display

class Plotter:

    def __init__(self):
        plt.ion()
        self.scores = []
        self.mean_scores = []
        self.total_score = 0
        self.best_score = 0
        self.epsilon = []

        self.new_record = False

    def update_score(self, score, num_episodes):
        if score > self.best_score:
            self.best_score = score
            self.new_record = True
        else:
            self.new_record = False

        self.total_score += score
        self.scores.append(score)
        mean_score = self.total_score / num_episodes
        self.mean_scores.append(mean_score)

    def plot(self, epsilon):
        self.epsilon.append(epsilon)

        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score and epsilon')
        plt.plot(self.scores)
        plt.plot(self.mean_scores)
        plt.plot(self.epsilon)
        plt.ylim(ymin=0)
        plt.text(len(self.scores)-1, self.scores[-1], str(self.scores[-1]))
        plt.text(len(self.mean_scores)-1, self.mean_scores[-1], str(self.mean_scores[-1]))
        plt.show(block=False)
        plt.pause(.1)
