import numpy as np

def select_parents(population, fitness_scores, num_parents):
    """
    Selects parents from the population based on their fitness scores using a probabilistic approach.

    Parameters:
    population (list): The current population of routes.
    fitness_scores (ndarray): An array of fitness scores for the population.
    num_parents (int): The number of parents to select.

    Returns:
    list: A list of selected parents.
    """
    # Calculate selection probabilities proportional to fitness scores
    probabilities = fitness_scores / np.sum(fitness_scores)
    
    # Select parent indices based on the calculated probabilities
    parents_indices = np.random.choice(range(len(population)), size=num_parents, p=probabilities)
    
    # Retrieve the selected parents from the population
    parents = [population[i] for i in parents_indices]
    
    return parents