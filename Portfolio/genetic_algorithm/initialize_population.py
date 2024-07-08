import numpy as np

def initialize_population(pop_size, num_cities):
    """
    Initializes a population of routes for the genetic algorithm.

    Parameters:
    pop_size (int): The size of the population.
    num_cities (int): The number of cities in the TSP.

    Returns:
    list: A list of routes, where each route is a permutation of city indices.
    """
    population = []  # List to store the population of routes
    for _ in range(pop_size):
        # Create a random permutation of city indices
        individual = np.random.permutation(np.arange(1, num_cities))
        # Add the individual route to the population
        population.append(individual)
    return population
