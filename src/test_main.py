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
        self.assertIn("hostname", data)
        self.assertIn("platform", data)
        self.assertIn("system", data)
        self.assertIn("release", data)
        self.assertIn("version", data)
        self.assertIn("machine", data)
        self.assertIn("processor", data)
        self.assertIn("python_version", data)
        self.assertIn("timestamp", data)
        self.assertIn("environment", data)

        # Check environment fields
        env = data["environment"]
        self.assertIn("node_name", env)
        self.assertIn("pod_name", env)
        self.assertIn("pod_namespace", env)
        self.assertIn("pod_ip", env)
        self.assertIn("service_account", env)

        # Verify hostname is not empty
        self.assertIsNotNone(data["hostname"])
        self.assertGreater(len(data["hostname"]), 0)

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)

    def test_hostname_from_environment(self):
        """Test that hostname is read from environment variable when available."""
        # Set a test hostname
        test_hostname = "test-hostname-123"
        os.environ["HOSTNAME"] = test_hostname

        try:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertEqual(data["hostname"], test_hostname)
        finally:
            # Clean up
            if "HOSTNAME" in os.environ:
                del os.environ["HOSTNAME"]

    def test_environment_variables(self):
        """Test that Kubernetes environment variables are included."""
        # Set test environment variables
        test_env = {
            "NODE_NAME": "test-node",
            "POD_NAME": "test-pod",
            "POD_NAMESPACE": "test-namespace",
            "POD_IP": "10.0.0.1",
            "SERVICE_ACCOUNT": "test-service-account",
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
            env = data["environment"]

            self.assertEqual(env["node_name"], test_env["NODE_NAME"])
            self.assertEqual(env["pod_name"], test_env["POD_NAME"])
            self.assertEqual(env["pod_namespace"], test_env["POD_NAMESPACE"])
            self.assertEqual(env["pod_ip"], test_env["POD_IP"])
            self.assertEqual(env["service_account"], test_env["SERVICE_ACCOUNT"])
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    if key in os.environ:
                        del os.environ[key]
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
