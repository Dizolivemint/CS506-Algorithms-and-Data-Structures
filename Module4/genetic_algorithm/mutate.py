import numpy as np

def mutate(route, mutation_rate):
    """
    Mutates a given route with a specified mutation rate by swapping two cities.

    Parameters:
    route (list): The route to be mutated.
    mutation_rate (float): The probability of mutation for each city in the route.

    Returns:
    list: The mutated route.
    """
    for i in range(len(route)):
        if np.random.rand() < mutation_rate:
            swap_idx = np.random.randint(0, len(route))
            route[i], route[swap_idx] = route[swap_idx], route[i]
    return route