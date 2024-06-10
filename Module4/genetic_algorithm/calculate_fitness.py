import numpy as np

def calculate_fitness(route, distance_matrix):
    return 1 / np.sum([distance_matrix[route[i - 1], route[i]] for i in range(len(route))])
