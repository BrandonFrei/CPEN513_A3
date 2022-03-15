import unittest
from copy import deepcopy
import os
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy as np
import Partitioning as part

class TestStringMethods(unittest.TestCase):
    # ensures that we do a proper swap
    def test_swap(self):
        nodes_a = {3: [[8], -1, 0], 11: [[9], -1, 0], 12: [[1, 2, 9, 15], 0.2666666666666666, 0], 14: [[12], -1, 0], 18: [[3], -1, 0], 19: [[13], -1, 0], 6: [[1, 2, 12, 14], 0, 1], 8: [[1, 2, 8, 14], 0, 1], 23: [[1, 2, 13, 15], 0, 1], 10: [[0, 3, 4, 5, 14], 0, 1], 17: [[0, 3, 4, 5, 15], 0, 1], 0: [[0], 0, 1]}
        nodes_b = {2: [[2], 0.3333333333333333, 0], 13: [[7], -1, 0], 15: [[1, 2, 6, 14], 0.2666666666666666, 0], 16: [[6], -1, 0], 20: [[10], -1, 0], 21: [[11], -1, 0], 7: [[1, 2, 7, 15], -1, 1], 9: [[1, 2, 11, 15], -1, 1], 22: [[1, 2, 10, 14], -1, 1], 4: [[4], 0, 1], 5: [[5], 0, 1], 1: [[1], 0, 1]}
        edges = {0: [[0, 10, 17], 0, 3], 1: [[1, 15, 7, 8, 12, 22, 9, 6, 23], 1, 4], 2: [[2, 15, 7, 8, 12, 22, 9, 6, 23], 1, 4], 3: [[18, 10, 17], 0, 3], 4: [[4, 10, 17], 1, 2], 
5: [[5, 10, 17], 1, 2], 6: [[15, 16], 0, 0], 7: [[7, 13], 0, 0], 8: [[8, 3], 0, 2], 9: [[12, 11], 0, 2], 10: [[22, 20], 0, 0], 11: [[9, 21], 0, 0], 12: [[6, 14], 
0, 2], 13: [[23, 19], 0, 2], 14: [[10, 15, 8, 22, 6], 1, 3], 15: [[17, 7, 12, 9, 23], 1, 3]}
        nodes_a, nodes_b = part.swap_nodes(nodes_a, nodes_b, edges, 3, 2)
        self.assertTrue(2 in nodes_a)
        self.assertTrue(3 in nodes_b)
        self.assertFalse(2 in nodes_b)
        self.assertFalse(3 in nodes_a)
    
    # ensures that the cost is properly calculated
    def test_output_validity(self):
        nodes_a, nodes_b, edges = part.main_function("ass2_files/paira.txt")
        for i in range(len(edges)):
            cost = 0
            for j in range(len(edges[i][0])):
                if(edges[i][0][j] in nodes_a):
                    cost += 1
            correct_output = 0
            # if all the nodes are in nodes_a
            if (len(edges[i][0]) == cost):
                correct_output = 1
            # if all the nodes are in nodes_b
            elif (cost == 0):
                correct_output = 1
            # if there is a cut in an edge
            elif (edges[i][1] == 1 and len(edges[i][0]) != cost):
                correct_output = 1
            # the broken edge
            if (correct_output == 0):
                print(edges[i][0])
            self.assertTrue(correct_output == 1)
    
if __name__ == '__main__':
    unittest.main()