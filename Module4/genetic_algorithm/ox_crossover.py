import numpy as np

def ox_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    start, end = sorted(np.random.choice(range(size), 2, replace=False))

    child[start:end] = parent1[start:end]

    pointer = end
    for i in range(size):
        if parent2[(i + end) % size] not in child:
            if pointer >= size:
                pointer = 0
            child[pointer] = parent2[(i + end) % size]
            pointer += 1

    return child
