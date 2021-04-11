
from evolutionary_alogrithm import Population
from CONSTANTS import VARIABLES, POPULATION_SIZE

import time


def print_value(name, value):
    space = ""
    for _ in range(19 - len(name)):
        space += " "
    print(f"{name}:{space}{value}")


class TimeIt:
    def __init__(self):
        self.stared_at = time.time()
        self.history = []
        self.average = 0

    def reset(self):
        self.history.append(time.time() - self.stared_at)
        self.stared_at = time.time()

    def update(self):
        return time.time()-self.stared_at

    def update_and_reset(self):
        t = time.time()-self.stared_at
        self.reset()
        return t

    def print(self, seconds, name="Time"):
        minutes, hours, days = 0, 0, 0
        if seconds >= 60:
            minutes = seconds // 60
            seconds = seconds % 60
            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60
                if hours >= 24:
                    days = hours // 24
                    hours = hours % 24

        seconds = round(seconds, 2)
        print_value(name, f"{int(days)}d: {int(hours)}h: {int(minutes)}min: {seconds}s:")

    def print_Duration(self, reset=False):
        seconds = self.update()
        self.print(seconds, "Duration")
        if reset:
            self.reset()

    def print_Predict(self, number_of_future_cycles):
        self.average = sum(self.history)/len(self.history)
        self.print(self.average * number_of_future_cycles, "Predicted")


VARIABLES.population = Population(POPULATION_SIZE)
if __name__ == "__main__":
    bestlist = []
    for i in range(1000):
        VARIABLES.population.proceed(int(POPULATION_SIZE/2))
        score = VARIABLES.population.population[-1].score
        bestlist.append(score)
        print_value("Generation", f"{VARIABLES.generation}")
        print_value("Score", f"{score}")
