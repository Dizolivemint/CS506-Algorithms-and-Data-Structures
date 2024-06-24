def calculate_fitness(route, distance_matrix):
    """
    Calculates the fitness of a given route based on the provided distance matrix.
    Fitness is defined as the inverse of the total distance of the route.

    Parameters:
    route (list): The route for which the fitness is to be calculated.
    distance_matrix (ndarray): A 2D array where element [i, j] represents the distance from city i to city j.

    Returns:
    float: The fitness of the route.
    """
    # Calculate the total distance of the route by summing up the distances between consecutive cities
    total_distance = 0
    for (i, j) in zip(route, route[1:]):
        total_distance += distance_matrix[i][j]
            
    # Handle the case where the total distance is zero
    if total_distance == 0:
        return float('inf')
    
    # Fitness is defined as the inverse of the total distance
    fitness = 1 / total_distance
    
    return fitness
