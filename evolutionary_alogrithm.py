from enviroment import Individual, run_simulation
from CONSTANTS import VARIABLES
from neural_network import softmax
import random, numpy as np


def fitness(value):
    return value


class Population:
    def __init__(self, population_size):
        self.fitness = fitness
        self.population = [Individual() for _ in range(population_size)]

    def proceed(self, n_children):
        VARIABLES.generation += 1 
        for individual in self.population:
            individual.reset()
        run_simulation(self.population)
        fitnesslist = softmax(np.asarray([individual.score for individual in self.population]))
        
        if VARIABLES.crossover_active:
            weights = [
                random.choices(self.population, fitnesslist)[0].pair(random.choices(self.population, fitnesslist)[0])
                for _ in range(int(n_children / 2))]
        else:# Ohnecrossover
            weights = [(random.choices(self.population, fitnesslist)[0].NN.get_flatted(),
                        random.choices(self.population, fitnesslist)[0].NN.get_flatted()) for _ in
                       range(int(n_children / 2))]

        self.population.sort(key=lambda x: x.score) # Die Population wird sortiert. Vorsicht erst nach gebrauch der fitnesslist

        for i, weight_tuple in enumerate(weights):
            # neue gewichte werden gesetzt
            weight1, weight2 = weight_tuple
            self.population[i * 2].NN.set_weights(weight1)
            self.population[i * 2 - 1].NN.set_weights(weight2)
            # neue NN's werden mutiert
            self.population[i * 2].NN.mutate(VARIABLES.mutation_strength, VARIABLES.learing_rate)
            self.population[i * 2 - 1].NN.mutate(VARIABLES.mutation_strength, VARIABLES.learing_rate)
