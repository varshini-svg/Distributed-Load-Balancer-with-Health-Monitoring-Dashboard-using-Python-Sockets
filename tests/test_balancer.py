import unittest
from core.algorithms import RoundRobin, LeastConnections, WeightedRoundRobin


# Sample test servers
SERVERS = [
    {"host": "127.0.0.1", "port": 9001, "weight": 1},
    {"host": "127.0.0.1", "port": 9002, "weight": 2},
    {"host": "127.0.0.1", "port": 9003, "weight": 1},
]


# -------------------------------
# Test Round Robin
# -------------------------------
class TestRoundRobin(unittest.TestCase):

    def test_round_robin_sequence(self):
        rr = RoundRobin(SERVERS)

        sequence = [rr.get_server()["port"] for _ in range(6)]

        expected = [9001, 9002, 9003, 9001, 9002, 9003]
        self.assertEqual(sequence, expected)


# -------------------------------
# Test Least Connections
# -------------------------------
class TestLeastConnections(unittest.TestCase):

    def test_least_connections(self):
        lc = LeastConnections(SERVERS)

        # First call → server 0
        server, idx = lc.get_server()
        self.assertEqual(idx, 0)

        # Second call → server 1
        server, idx = lc.get_server()
        self.assertEqual(idx, 1)

        # Third call → server 2
        server, idx = lc.get_server()
        self.assertEqual(idx, 2)

        # Now release server 0
        lc.release_server(0)

        # Next should be server 0 again
        server, idx = lc.get_server()
        self.assertEqual(idx, 0)


# -------------------------------
# Test Weighted Round Robin
# -------------------------------
class TestWeightedRoundRobin(unittest.TestCase):

    def test_weighted_distribution(self):
        wrr = WeightedRoundRobin(SERVERS)

        sequence = [wrr.get_server()["port"] for _ in range(8)]

        # Expected pattern: 9001, 9002, 9002, 9003 repeated
        expected = [9001, 9002, 9002, 9003,
                    9001, 9002, 9002, 9003]

        self.assertEqual(sequence, expected)


# -------------------------------
# Run Tests
# -------------------------------
if __name__ == "__main__":
    unittest.main()