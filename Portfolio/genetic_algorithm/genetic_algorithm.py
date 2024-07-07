import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
from genetic_algorithm.initialize_population import initialize_population
from genetic_algorithm.calculate_fitness import calculate_fitness
from genetic_algorithm.select_parents import select_parents
from genetic_algorithm.pmx_crossover import pmx_crossover
from genetic_algorithm.ox_crossover import ox_crossover
from genetic_algorithm.mutate import mutate

def genetic_algorithm(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations):
    # Number of cities in the distance matrix
    num_cities = len(distance_matrix)
    
    # Initialize the population with random routes
    population = initialize_population(pop_size, num_cities)
    
    # Variables to store the best route and its fitness score
    best_route = None
    best_fitness = float('-inf')
    best_distance = float('inf')
    generations_no_improvement = 0

    # Function to calculate fitness in parallel
    def parallel_fitness(route):
        return calculate_fitness(route, distance_matrix)

    # Determine the number of threads dynamically
    num_threads = os.cpu_count()

    generation = 0
    while True:
        generation += 1
        
        # Calculate fitness scores for the current population in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            fitness_scores = np.array(list(executor.map(parallel_fitness, population)))
        
        # Find the best fitness score and the corresponding route in the current generation
        best_gen_fitness = np.max(fitness_scores)
        best_gen_route = population[np.argmax(fitness_scores)]

        # Update the best route and fitness if the current generation has a better route
        if best_gen_fitness > best_fitness:
            best_fitness = best_gen_fitness
            best_route = best_gen_route
            best_distance = np.sum([distance_matrix[best_route[i - 1], best_route[i]] for i in range(len(best_route))])
            generations_no_improvement = 0
        else:
            generations_no_improvement += 1

        # Yield the current best solution
        yield {
            'generation': generation,
            'route': best_route.tolist() if isinstance(best_route, np.ndarray) else best_route,
            'distance': best_distance,
            'fitness': best_fitness
        }

        # Check convergence criteria
        if fitness_threshold is not None and best_fitness >= fitness_threshold:
            break

        if generations_no_improvement >= no_improvement_generations:
            break

        # Select parents based on their fitness scores
        parents = select_parents(population, fitness_scores, pop_size)
        next_population = []

        # Create the next generation through crossover and mutation
        for i in range(0, pop_size, 2):
            if np.random.rand() < crossover_rate:
                # Randomly select crossover points
                crossover_point1, crossover_point2 = sorted(np.random.choice(range(num_cities), 2, replace=False))
                
                # Apply the selected crossover method
                if use_pmx:
                    child1 = pmx_crossover(parents[i], parents[i+1], crossover_point1, crossover_point2)
                    child2 = pmx_crossover(parents[i+1], parents[i], crossover_point1, crossover_point2)
                elif use_ox:
                    child1 = ox_crossover(parents[i], parents[i+1])
                    child2 = ox_crossover(parents[i+1], parents[i])
                else:
                    child1, child2 = parents[i], parents[i+1]
            else:
                # If crossover does not occur, children are copies of the parents
                child1, child2 = parents[i], parents[i+1]

            # Apply mutation to the children
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            # Ensure mutation produces valid routes
            if len(set(child1)) != len(child1) or len(set(child2)) != len(child2):
                raise ValueError("Mutation produced invalid route with duplicate cities.")
            
            next_population.extend([child1, child2])
            
        # Apply elitism by carrying the best route to the next generation
        if use_elitism:
            next_population[0] = best_gen_route

        # Replace the old population with the new one
        population = next_population

