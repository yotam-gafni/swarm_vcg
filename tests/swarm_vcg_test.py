import sys
sys.path.insert(0, "..")
sys.path.insert(0, ".")

from simulator import SwarmVCG
import unittest


class TestCalculate(unittest.TestCase):

    def test_1(self):
        BUYERS = [
            ['2$', '3mbps', 'B'], 
            ['2$', '3mbps', 'A'],
            ['5$', '3mbps', 'B']
            ]

        SELLERS = [
            ['0.5$', '4mbps', set(['B'])],
            ['0.5$', '3mbps', set(['B'])],
            ['0.5$', '2mbps', set(['A','B'])]
            ]
        final_matching_set, prices = SwarmVCG(BUYERS, SELLERS).compute()
        self.assertEqual(final_matching_set, [[0, 1, 1], [2, 2], [0, 0, 0]])
        self.assertEqual(prices, [1.5,1.0,1.5])

    def test_2(self):
        BUYERS = [
            ['2$', '3mbps', 'B'], 
            ['2$', '3mbps', 'A'],
            ['5$', '3mbps', 'B']
            ]

        SELLERS = [
            ['0$', '4mbps', set(['B'])],
            ['0$', '3mbps', set(['B'])],
            ['0$', '2mbps', set(['A','B'])]
            ]
        final_matching_set, prices = SwarmVCG(BUYERS, SELLERS).compute()
        self.assertEqual(final_matching_set, [[0, 1, 1], [2, 2], [0, 0, 0]])
        self.assertEqual(prices, [0,0,0])

    def test_3(self):
        BUYERS = [
            ['2$', '5mbps', 'B'], 
            ['2$', '3mbps', 'A'],
            ['5$', '5mbps', 'B']
            ]

        SELLERS = [
            ['0$', '4mbps', set(['B'])],
            ['0$', '3mbps', set(['B'])],
            ['0$', '2mbps', set(['A','B'])]
            ]
        final_matching_set, prices = SwarmVCG(BUYERS, SELLERS).compute()
        self.assertEqual(final_matching_set, [[1, 1, 2], [2], [0, 0, 0, 0, 1]])
        self.assertEqual(prices, [2,2,6])

    def test_4(self):
        BUYERS = [
            ['2$', '5mbps', 'B'], 
            ['2$', '3mbps', 'A'],
            ['2$', '5mbps', 'B']
            ]

        SELLERS = [
            ['0$', '4mbps', set(['B'])],
            ['3$', '3mbps', set(['B'])],
            ['0$', '2mbps', set(['A','B'])]
            ]
        final_matching_set, prices = SwarmVCG(BUYERS, SELLERS).compute()
        self.assertEqual(final_matching_set, [[2], [2], [0, 0, 0, 0]])
        self.assertEqual(prices, [2,2,8])

    def test_5(self):
        BUYERS = [
            ['2$', '5mbps', 'B'], 
            ['2$', '3mbps', 'A'],
            ['5$', '5mbps', 'B']
            ]

        SELLERS = [
            ['0$', '4mbps', set(['B'])],
            ['3$', '3mbps', set(['B'])],
            ['0$', '2mbps', set(['A','B'])]
            ]
        final_matching_set, prices = SwarmVCG(BUYERS, SELLERS).compute()
        self.assertEqual(final_matching_set, [[0, 0, 2], [2], [0, 0, 1, 1, 1]])
        self.assertEqual(prices, [2,2,9])


if __name__ == '__main__':
    unittest.main()