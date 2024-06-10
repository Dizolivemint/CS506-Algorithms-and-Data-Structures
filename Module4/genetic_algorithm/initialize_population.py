import numpy as np

def initialize_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        individual = np.random.permutation(num_cities)
        population.append(individual)
    return population