import random

def mutate(route, mutation_rate):
    """
    Mutate the route with a given mutation rate by swapping two cities.
    
    Parameters:
    route (list): The current route.
    mutation_rate (float): The probability of mutation for each city in the route.
    
    Returns:
    list: The mutated route.
    """
    route = route.copy()
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            # Swap city i with city j
            route[i], route[j] = route[j], route[i]
    return route
