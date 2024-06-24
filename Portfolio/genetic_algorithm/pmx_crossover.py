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
        mapping[parent1[i]] = parent2[i]

    # Fill the remaining positions in the child
    for i in range(size):
        if child[i] == -1:
            candidate = parent2[i]
            while candidate in child:
                candidate = mapping[candidate]
            child[i] = candidate

    return child

# Test the pmx_crossover function with sample data
parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
parent2 = [3, 7, 5, 1, 6, 8, 2, 4]
crossover_point1 = 2
crossover_point2 = 5

child = pmx_crossover(parent1, parent2, crossover_point1, crossover_point2)
print(f"Parent1: {parent1}")
print(f"Parent2: {parent2}")
print(f"Child: {child}")
