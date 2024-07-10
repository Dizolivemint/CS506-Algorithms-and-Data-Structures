import numpy as np

def initialize_pheromones(num_cities):
    return np.ones((num_cities, num_cities))

def update_pheromones(pheromones, routes, fitness_scores, decay=0.1):
    pheromones *= (1 - decay)  # Apply decay
    for route, fitness in zip(routes, fitness_scores):
        for i in range(len(route) - 1):
            pheromones[route[i], route[i+1]] += fitness
        pheromones[route[-1], route[0]] += fitness  # Closing the loop

def adjust_mutation_rate(route, pheromones, base_mutation_rate, pheromone_threshold):
    pheromone_strength = np.mean([pheromones[route[i], route[i+1]] for i in range(len(route) - 1)])
    pheromone_strength += pheromones[route[-1], route[0]]  # Closing the loop
    if pheromone_strength > pheromone_threshold:
        return base_mutation_rate * 2  # Increase mutation rate for strong pheromone trails
    return base_mutation_rate
