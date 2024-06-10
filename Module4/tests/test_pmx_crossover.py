import unittest
from genetic_algorithm.pmx_crossover import pmx_crossover

class TestPMXCrossover(unittest.TestCase):

    def test_pmx_crossover(self):
        parent1 = [1, 2, 3, 4, 5]
        parent2 = [5, 4, 3, 2, 1]
        crossover_point1 = 1
        crossover_point2 = 3
        child = pmx_crossover(parent1, parent2, crossover_point1, crossover_point2)
        self.assertEqual(len(child), len(parent1))
        self.assertNotEqual(child, parent1)
        self.assertNotEqual(child, parent2)

if __name__ == '__main__':
    unittest.main()
