import unittest

import environment
import robot


class TestNavigation(unittest.TestCase):

    def setUp(self):
        environment.dynamic_obstacles.clear()

    def test_path_exists(self):
        start = (2, 2)
        goal = (4, 2)

        path = robot.find_path(start, goal)

        self.assertIsNotNone(path)

    def test_path_starts_at_start(self):
        start = (2, 2)
        goal = (4, 2)

        path = robot.find_path(start, goal)

        self.assertEqual(path[0], start)

    def test_path_reaches_goal(self):
        start = (2, 2)
        goal = (4, 2)

        path = robot.find_path(start, goal)

        self.assertEqual(path[-1], goal)

    def test_path_avoids_obstacle(self):
        start = (2, 2)
        goal = (8, 2)

        path = robot.find_path(start, goal)

        self.assertIsNotNone(path)

        for position in path:
            self.assertNotIn(
                position,
                environment.obstacles
            )

    def test_dynamic_obstacle_is_avoided(self):
        start = (2, 2)
        goal = (4, 2)

        environment.add_dynamic_obstacle((3, 2))

        path = robot.find_path(start, goal)

        self.assertIsNotNone(path)

        self.assertNotIn(
            (3, 2),
            path
        )


if __name__ == "__main__":
    unittest.main()