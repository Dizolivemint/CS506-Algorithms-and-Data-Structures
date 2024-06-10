import numpy as np

def pmx_crossover(parent1, parent2, crossover_point1, crossover_point2):
    """
    Performs Partially Mapped Crossover (PMX) on two parent routes to produce a child route.

    Parameters:
    parent1 (list): The first parent route.
    parent2 (list): The second parent route.
    crossover_point1 (int): The first crossover point.
    crossover_point2 (int): The second crossover point.

    Returns:
    list: The child route produced by applying PMX to the parents.
    """
    size = len(parent1)
    child = [-1] * size  # Initialize the child with -1 (indicating empty positions)

    # Copy the segment from the first parent to the child
    child[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]

    # Create a mapping of values between parent1 and parent2 for the crossover segment
    mapping = {}
    for i in range(crossover_point1, crossover_point2):
        mapping[parent2[i]] = parent1[i]

    # Fill the remaining positions in the child
    for i in range(size):
        if child[i] == -1:
            candidate = parent2[i]
            while candidate in mapping:
                candidate = mapping[candidate]
            child[i] = candidate

    return child