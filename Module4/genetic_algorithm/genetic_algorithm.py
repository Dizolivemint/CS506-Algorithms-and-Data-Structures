import numpy as np
from .initialize_population import initialize_population
from .calculate_fitness import calculate_fitness
from .select_parents import select_parents
from .pmx_crossover import pmx_crossover
from .ox_crossover import ox_crossover
from .mutate import mutate

def genetic_algorithm(distance_matrix, pop_size, num_generations, mutation_rate, crossover_rate, use_pmx=False, use_ox=False, use_elitism=False):
    num_cities = len(distance_matrix)
    population = initialize_population(pop_size, num_cities)
    best_route = None
    best_fitness = float('-inf')

    for generation in range(num_generations):
        fitness_scores = np.array([calculate_fitness(route, distance_matrix) for route in population])
        best_gen_fitness = np.max(fitness_scores)
        best_gen_route = population[np.argmax(fitness_scores)]

        if best_gen_fitness > best_fitness:
            best_fitness = best_gen_fitness
            best_route = best_gen_route

        parents = select_parents(population, fitness_scores, pop_size)
        next_population = []

        for i in range(0, pop_size, 2):
            if np.random.rand() < crossover_rate:
                crossover_point1, crossover_point2 = sorted(np.random.choice(range(num_cities), 2, replace=False))
                if use_pmx:
                    child1 = pmx_crossover(parents[i], parents[i+1], crossover_point1, crossover_point2)
                    child2 = pmx_crossover(parents[i+1], parents[i], crossover_point1, crossover_point2)
                elif use_ox:
                    child1 = ox_crossover(parents[i], parents[i+1])
                    child2 = ox_crossover(parents[i+1], parents[i])
                else:
                    child1, child2 = parents[i], parents[i+1]
            else:
                child1, child2 = parents[i], parents[i+1]

            next_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])

        if use_elitism:
            next_population[0] = best_gen_route

        population = next_population

    return best_route, best_fitness
