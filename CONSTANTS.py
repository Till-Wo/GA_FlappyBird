
HEIGHT = 700
WIDTH = 700
POPULATION_SIZE = 200

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 120, 120)
ORANGE = (250, 159, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Data:
    def __init__(self):
        self.best_round_score = 0
        self.generation = 0
        self.n_alive = 0
        self.mutation_strength = 0.8
        self.population = None
        self.speed = 1
        self.crossover_active = False
        self.learing_rate = 0.8


def reset():
    global VARIABLES
    VARIABLES = Data()


VARIABLES = Data()