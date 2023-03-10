# À compléter
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

class Test_Reachability(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.min_power(1, 4)[1],11)
if __name__ == '__main__':
    unittest.main()
