import unittest

import environment


class TestEnvironment(unittest.TestCase):

    def test_valid_position(self):

        self.assertTrue(
            environment.is_valid_position((0, 0))
        )

    def test_invalid_boundary_position(self):

        self.assertFalse(
            environment.is_valid_position((-1, 0))
        )

        self.assertFalse(
            environment.is_valid_position(
                (environment.WIDTH, 0)
            )
        )

    def test_static_obstacle(self):

        obstacle = next(
            iter(environment.obstacles)
        )

        self.assertFalse(
            environment.is_valid_position(obstacle)
        )

    def test_dynamic_obstacle(self):

        position = (0, 1)

        # Make sure the test position is free
        environment.dynamic_obstacles.discard(
            position
        )

        environment.add_dynamic_obstacle(
            position
        )

        self.assertFalse(
            environment.is_valid_position(position)
        )

        environment.remove_dynamic_obstacle(
            position
        )

        self.assertTrue(
            environment.is_valid_position(position)
        )

    def test_neighbors_are_valid(self):

        position = (0, 0)

        neighbors = environment.get_neighbors(
            position
        )

        for neighbor in neighbors:

            self.assertTrue(
                environment.is_valid_position(
                    neighbor
                )
            )


if __name__ == "__main__":
    unittest.main()