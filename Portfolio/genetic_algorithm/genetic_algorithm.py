import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
from genetic_algorithm.initialize_population import initialize_population
from genetic_algorithm.calculate_fitness import calculate_fitness
from genetic_algorithm.select_parents import select_parents
from genetic_algorithm.pmx_crossover import pmx_crossover
from genetic_algorithm.ox_crossover import ox_crossover
from genetic_algorithm.mutate import mutate
from optimizations.ant_colony_optimization import initialize_pheromones, update_pheromones, adjust_mutation_rate
from optimizations.simulated_annealing import simulated_annealing

def calculate_total_distance(route, distance_matrix):
    distance = np.sum([distance_matrix[route[i - 1], route[i]] for i in range(len(route))])
    distance += distance_matrix[route[-1], route[0]]  # Add distance to return to the start city
    return distance

def process_aco_child(child, pheromones, mutation_rate, pheromone_threshold):
    mutation_rate = adjust_mutation_rate(child, pheromones, mutation_rate, pheromone_threshold)
    return mutate(child, mutation_rate)

def is_unique_route(route, population):
    for existing_route in population:
        if np.array_equal(route, existing_route):
            return False
    return True
  
def genetic_algorithm(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations, use_aco=False, pheromone_threshold=5, use_sa=False, sa_initial_temp=1000, sa_cooling_rate=0.995, sa_num_iterations=1000):
    num_cities = len(distance_matrix)
    start_city = 0  # Assuming "New York, NY" is the first city in the distance matrix
    
    # Initialize the population with random routes that start and end with the same city
    population = initialize_population(pop_size, num_cities)
    population = [np.insert(route, 0, start_city) for route in population]
    population = [np.append(route, start_city) for route in population]

    best_route = None
    best_fitness = float('-inf')
    best_distance = float('inf')
    generations_no_improvement = 0
    
    # Initialize pheromones
    pheromones = initialize_pheromones(num_cities) if use_aco else None

    def parallel_fitness(route):
        return calculate_fitness(route, distance_matrix)

    num_threads = os.cpu_count()

    generation = 0
    while True:
        generation += 1
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            fitness_scores = np.array(list(executor.map(parallel_fitness, population)))
        
        best_gen_fitness = np.max(fitness_scores)
        best_gen_route = population[np.argmax(fitness_scores)]

        if best_gen_fitness > best_fitness:
            best_fitness = best_gen_fitness
            best_route = best_gen_route
            best_distance = calculate_total_distance(best_route, distance_matrix)
            generations_no_improvement = 0
        else:
            generations_no_improvement += 1
            
        # Apply simulated annealing to refine the best route found so far
        if use_sa:
          best_route, best_distance = simulated_annealing(best_route, distance_matrix, sa_initial_temp, sa_cooling_rate, sa_num_iterations)

        yield {
            'generation': generation,
            'route': best_route.tolist() if isinstance(best_route, np.ndarray) else best_route,
            'distance': best_distance,
            'fitness': best_fitness
        }

        if fitness_threshold is not None and best_fitness >= fitness_threshold:
            break

        if generations_no_improvement >= no_improvement_generations:
            break

        parents = select_parents(population, fitness_scores, pop_size)
        next_population = []

        for i in range(0, pop_size, 2):
            if np.random.rand() < crossover_rate:
                crossover_point1, crossover_point2 = sorted(np.random.choice(range(1, num_cities - 1), 2, replace=False))

                if use_pmx:
                    child1 = pmx_crossover(parents[i][1:-1], parents[i+1][1:-1], crossover_point1 - 1, crossover_point2 - 1)
                    child2 = pmx_crossover(parents[i+1][1:-1], parents[i][1:-1], crossover_point1 - 1, crossover_point2 - 1)
                elif use_ox:
                    child1 = ox_crossover(parents[i][1:-1], parents[i+1][1:-1])
                    child2 = ox_crossover(parents[i+1][1:-1], parents[i][1:-1])
                else:
                    child1, child2 = parents[i][1:-1], parents[i+1][1:-1]
            else:
                child1, child2 = parents[i][1:-1], parents[i+1][1:-1]

            if use_aco:
                child1 = process_aco_child(child1, pheromones, mutation_rate, pheromone_threshold)
                child2 = process_aco_child(child2, pheromones, mutation_rate, pheromone_threshold)
            else:
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)

            child1 = np.insert(child1, 0, start_city)
            child1 = np.append(child1, start_city)
            child2 = np.insert(child2, 0, start_city)
            child2 = np.append(child2, start_city)

            next_population.extend([child1, child2])

        if use_elitism:
            next_population[0] = best_gen_route
            
        # Ensure the start city appears only at the beginning and end
        next_population = [
            route for route in next_population
            if list(route).count(start_city) == 2 and route[0] == start_city and route[-1] == start_city
        ]

        population = next_population
        
        if use_aco:
          update_pheromones(pheromones, population, fitness_scores)
