import numpy as np

def ox_crossover(parent1, parent2):
    """
    Performs Order Crossover (OX) on two parent routes to produce a child route.

    Parameters:
    parent1 (list): The first parent route.
    parent2 (list): The second parent route.

    Returns:
    list: The child route produced by applying OX to the parents.
    """
    size = len(parent1)
    child = [-1] * size  # Initialize the child with -1 (indicating empty positions)

    # Select two crossover points
    start, end = sorted(np.random.choice(range(size), 2, replace=False))

    # Copy the segment from the first parent to the child
    child[start:end] = parent1[start:end]

    # Pointer for filling in the child from the second parent
    pointer = end
    for i in range(size):
        # Check the elements in parent2 in order, starting from the 'end' position
        if parent2[(i + end) % size] not in child:
            while child[pointer] != -1:
                pointer = (pointer + 1) % size
            # Place the element in the next available position in the child
            child[pointer] = parent2[(i + end) % size]

    return child