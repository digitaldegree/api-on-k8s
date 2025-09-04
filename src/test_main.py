import os
import unittest

from fastapi.testclient import TestClient

from main import app


class TestSystemInfoAPI(unittest.TestCase):
    """Test cases for the System Info API."""

    def setUp(self):
        """Set up test client before each test."""
        self.client = TestClient(app)

    def test_get_system_info(self):
        """Test the main system info endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Check required fields
        self.assertIn("host", data)
        self.assertIn("node", data)
        self.assertIn("ip", data)
        self.assertIn("platform", data)
        self.assertIn("system", data)
        self.assertIn("release", data)
        self.assertIn("version", data)
        self.assertIn("machine", data)
        self.assertIn("python_version", data)
        self.assertIn("timestamp", data)

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)

    def test_kubernetes_environment_variables(self):
        """Test that Kubernetes environment variables are included."""
        # Set test environment variables
        test_env = {
            "HOSTNAME": "test-host",
            "NODE_NAME": "test-node",
            "POD_IP": "10.0.0.1",
        }

        # Store original values
        original_env = {}
        for key in test_env:
            original_env[key] = os.environ.get(key)
            os.environ[key] = test_env[key]

        try:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)

            data = response.json()

            self.assertEqual(data["node"], test_env["NODE_NAME"])
            self.assertEqual(data["ip"], test_env["POD_IP"])
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    if key in os.environ:
                        del os.environ[key]
                else:
                    os.environ[key] = value

    def test_hostname_fields(self):
        """Test that host and hostname fields are present and have correct format."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Check host and hostname exist
        self.assertIn("host", data)

        # hostname should always be a string (platform.node() or "unknown")
        hostname = data["host"]
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)  # Should not be empty


if __name__ == "__main__":
    unittest.main()
