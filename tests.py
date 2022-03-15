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

    def test_output_validity(self):
        nodes_a, nodes_b, edges = part.main_function("ass2_files/apex4.txt")
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