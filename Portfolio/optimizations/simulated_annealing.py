import numpy as np
import random

def simulated_annealing(route, distance_matrix, initial_temp, cooling_rate, num_iterations):
    """
    Performs the simulated annealing algorithm to optimize the route.
    
    Parameters:
    route (list): The initial route.
    distance_matrix (ndarray): The distance matrix.
    initial_temp (float): The initial temperature.
    cooling_rate (float): The rate at which the temperature decreases.
    num_iterations (int): The number of iterations to perform.
    
    Returns:
    list: The optimized route.
    """
    def calculate_route_distance(route):
        distance = np.sum([distance_matrix[route[i - 1], route[i]] for i in range(len(route))])
        distance += distance_matrix[route[-1], route[0]]  # Add distance to return to the start city
        return distance

    current_temp = initial_temp
    current_route = route.copy()
    best_route = route.copy()
    best_distance = calculate_route_distance(route)
    
    for _ in range(num_iterations):
        # Create a new neighboring route by swapping two cities
        new_route = current_route.copy()
        i, j = random.sample(range(1, len(route) - 1), 2)  # Avoid swapping the first and last city
        new_route[i], new_route[j] = new_route[j], new_route[i]
        
        current_distance = calculate_route_distance(current_route)
        new_distance = calculate_route_distance(new_route)
        
        # Determine if we should accept the new route
        if new_distance < current_distance or random.random() < np.exp((current_distance - new_distance) / current_temp):
            current_route = new_route.copy()
            current_distance = new_distance
        
        # Update the best route found so far
        if current_distance < best_distance:
            best_route = current_route.copy()
            best_distance = current_distance
        
        # Decrease the temperature
        current_temp *= cooling_rate
    
    return best_route, best_distance
