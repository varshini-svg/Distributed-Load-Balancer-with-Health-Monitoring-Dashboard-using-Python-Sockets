import unittest
import time
from core.health_checker import HealthChecker


# Sample servers (adjust ports based on running servers)
SERVERS = [
    {"host": "127.0.0.1", "port": 9001},  # should be UP
    {"host": "127.0.0.1", "port": 9999},  # should be DOWN
]


class TestHealthChecker(unittest.TestCase):

    def setUp(self):
        """Initialize HealthChecker before each test"""
        self.health_checker = HealthChecker(
            SERVERS,
            interval=2,
            timeout=1
        )
        self.health_checker.start()

        # Give time for initial health check
        time.sleep(3)

    def tearDown(self):
        """Stop HealthChecker after each test"""
        self.health_checker.stop()

    def test_server_status(self):
        """Check if UP and DOWN servers are detected correctly"""
        active_servers = self.health_checker.get_active_servers()

        # Server on 9001 should be UP (if running)
        up_ports = [s["port"] for s in active_servers]

        self.assertIn(9001, up_ports)

        # Server on 9999 should be DOWN
        self.assertNotIn(9999, up_ports)

    def test_active_server_list(self):
        """Ensure active server list is returned correctly"""
        active_servers = self.health_checker.get_active_servers()

        self.assertIsInstance(active_servers, list)
        self.assertTrue(len(active_servers) >= 1)

    def test_dynamic_update(self):
        """Check if health checker updates over time"""
        initial = self.health_checker.get_active_servers()

        # Wait for another health check cycle
        time.sleep(3)

        updated = self.health_checker.get_active_servers()

        # Lists should still be valid (may or may not change)
        self.assertIsInstance(updated, list)

    def test_empty_servers(self):
        """Test behavior with empty server list"""
        hc = HealthChecker([], interval=1)
        hc.start()

        time.sleep(2)

        active = hc.get_active_servers()
        self.assertEqual(active, [])

        hc.stop()


# -------------------------------
# Run Tests
# -------------------------------
if __name__ == "__main__":
    print("⚠️ Make sure at least one backend server is running on port 9001")
    unittest.main()