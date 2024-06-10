def pmx_crossover(parent1, parent2, crossover_point1, crossover_point2):
    size = len(parent1)
    child = [-1] * size

    child[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]

    mapping = {}
    for i in range(crossover_point1, crossover_point2):
        if parent2[i] not in child:
            mapping[parent2[i]] = parent1[i]

    for i in range(size):
        if child[i] == -1:
            candidate = parent2[i]
            while candidate in mapping:
                candidate = mapping[candidate]
            child[i] = candidate

    return child
