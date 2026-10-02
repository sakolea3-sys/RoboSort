import unittest

from app import app
from simulation import simulation


class TestAPI(unittest.TestCase):

    def setUp(self):

        # Reset the simulation before every test
        simulation.reset()

        # Flask test client
        self.client = app.test_client()


    def test_get_state(self):

        response = self.client.get(
            "/api/state"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertIsNotNone(
            data
        )

        self.assertIn(
            "position",
            data
        )

        self.assertIn(
            "direction",
            data
        )

        self.assertIn(
            "state",
            data
        )

        self.assertIn(
            "sensors",
            data
        )

        self.assertIn(
            "objects",
            data
        )

        self.assertIn(
            "statistics",
            data
        )


    def test_step(self):

        response = self.client.post(
            "/api/step"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["step"],
            1
        )


    def test_start(self):

        response = self.client.post(
            "/api/start"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertTrue(
            data["running"]
        )


    def test_stop(self):

        # Start first
        self.client.post(
            "/api/start"
        )

        # Then stop
        response = self.client.post(
            "/api/stop"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertFalse(
            data["running"]
        )


    def test_reset(self):

        # Change the simulation first
        self.client.post(
            "/api/step"
        )

        self.client.post(
            "/api/start"
        )

        # Reset
        response = self.client.post(
            "/api/reset"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["step"],
            0
        )

        self.assertFalse(
            data["running"]
        )

        self.assertFalse(
            data["finished"]
        )


if __name__ == "__main__":

    unittest.main()