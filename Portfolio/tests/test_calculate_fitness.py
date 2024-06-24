import unittest
import numpy as np
from genetic_algorithm.calculate_fitness import calculate_fitness

class TestCalculateFitness(unittest.TestCase):

    def test_calculate_fitness(self):
        route = [0, 1, 2, 3]
        distance_matrix = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0]
        ])
        fitness = calculate_fitness(route, distance_matrix)
        expected_fitness = 1 / 6
        self.assertAlmostEqual(fitness, expected_fitness)

if __name__ == '__main__':
    unittest.main()