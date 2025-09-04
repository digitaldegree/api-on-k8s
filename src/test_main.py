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
        self.assertIn("node_name", data)
        self.assertIn("pod_name", data)
        self.assertIn("pod_ip", data)
        self.assertIn("instance_id", data)
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
            "NODE_NAME": "test-node",
            "POD_NAME": "test-pod",
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

            self.assertEqual(data["node_name"], test_env["NODE_NAME"])
            self.assertEqual(data["pod_name"], test_env["POD_NAME"])
            self.assertEqual(data["pod_ip"], test_env["POD_IP"])
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    if key in os.environ:
                        del os.environ[key]
                else:
                    os.environ[key] = value

    def test_instance_id_uniqueness(self):
        """Test that instance_id is generated and has correct format."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Check instance_id exists and has correct format
        self.assertIn("instance_id", data)
        instance_id = data["instance_id"]
        self.assertIsInstance(instance_id, str)
        self.assertEqual(len(instance_id), 8)  # Should be 8 characters
        self.assertTrue(instance_id.isalnum())  # Should be alphanumeric


if __name__ == "__main__":
    unittest.main()
