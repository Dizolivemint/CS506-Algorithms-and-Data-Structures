import pandas as pd
import numpy as np
import argparse
from genetic_algorithm import genetic_algorithm

def print_route(best_route, best_distance, best_fitness):
  print(f"Best route: {best_route}\nBest Distance: {best_distance} km\nFitness: {best_fitness}\n")

def main(file_name):
    # Load the distance matrix from the specified CSV file
    df = pd.read_csv(file_name, index_col=0)
    distance_matrix = df.to_numpy()
    
    # Convert distances from meters to kilometers
    distance_matrix = distance_matrix / 1000
    
    # Ensure the distance matrix is valid
    if np.any(np.isnan(distance_matrix)) or np.any(distance_matrix < 0):
        raise ValueError("Distance matrix contains invalid values.")

    # Ensure diagonal is zero and no other zeros
    np.fill_diagonal(distance_matrix, 0)
    if np.any((distance_matrix == 0) & (np.eye(len(distance_matrix)) == 0)):
        raise ValueError("Distance matrix contains zero values off the diagonal.")
    
    # Check for any invalid values in the distance matrix
    if np.any(np.isnan(distance_matrix)) or np.any(distance_matrix < 0):
        raise ValueError("Distance matrix contains invalid values.")

    # Run the genetic algorithm with different configurations
    print("Running GA without PMX, OX, or Elitism:")
    best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=100, num_generations=1000, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=False, use_elitism=False)
    print_route(best_route, best_distance, best_fitness)
    
    # print("Running GA with PMX:")
    # best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=True, use_ox=False, use_elitism=False)
    # print_route(best_route, best_distance, best_fitness)
    
    # print("Running GA with OX:")
    # best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=True, use_elitism=False)
    # print_route(best_route, best_distance, best_fitness)
    
    # print("Running GA with Elitism:")
    # best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=False, use_elitism=True)
    # print_route(best_route, best_distance, best_fitness)
    
    # print("Running GA with PMX and Elitism:")
    # best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=True, use_ox=False, use_elitism=True)
    # print_route(best_route, best_distance, best_fitness)
    
    # print("Running GA with OX and Elitism:")
    # best_route, best_fitness, best_distance = genetic_algorithm(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.01, crossover_rate=0.7, use_pmx=False, use_ox=True, use_elitism=True)
    # print_route(best_route, best_distance, best_fitness)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the genetic algorithm with a specified distance matrix file.')
    parser.add_argument('file_name', type=str, help='The CSV file containing the distance matrix')
    args = parser.parse_args()
    main(args.file_name)