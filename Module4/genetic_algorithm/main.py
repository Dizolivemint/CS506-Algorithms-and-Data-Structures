import numpy as np
from genetic_algorithm.genetic_algorithm import genetic_algorithm

# Load the distance matrix from CSV
distance_matrix = np.genfromtxt('data/distance_matrix.csv', delimiter=',', skip_header=1, usecols=range(1, 11))

# Run the genetic algorithm with different configurations
print("Running GA without PMX, OX, or Elitism:")
best_route, best_fitness = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=False, use_elitism=False)
print(f"Best route: {best_route}, Fitness: {best_fitness}\n")

print("Running GA with PMX:")
best_route, best_fitness = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=True, use_ox=False, use_elitism=False)
print(f"Best route: {best_route}, Fitness: {best_fitness}\n")

print("Running GA with OX:")
best_route, best_fitness = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=True, use_elitism=False)

