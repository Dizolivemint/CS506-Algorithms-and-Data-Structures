import unittest
import numpy as np
from genetic_algorithm.select_parents import select_parents

class TestSelectParents(unittest.TestCase):

    def test_select_parents(self):
        population = [[0, 1, 2, 3], [3, 2, 1, 0], [1, 2, 3, 0], [2, 3, 0, 1]]
        fitness_scores = np.array([1, 2, 3, 4])
        num_parents = 2
        parents = select_parents(population, fitness_scores, num_parents)
        self.assertEqual(len(parents), num_parents)

if __name__ == '__main__':
    unittest.main()