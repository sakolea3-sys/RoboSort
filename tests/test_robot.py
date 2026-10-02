import unittest

import environment
import robot


class TestRobot(unittest.TestCase):

    def setUp(self):

        # Reset dynamic obstacles
        environment.dynamic_obstacles.clear()

        # Reset robot position and direction
        environment.robot_x = 2
        environment.robot_y = 2
        environment.direction = "E"

        # Reset objects
        environment.objects.clear()

        environment.objects.update({
            (4, 2): "A",
            (9, 8): "B"
        })

        # Reset robot state
        robot.carrying_object = None
        robot.current_path = None

    def test_detect_object(self):

        environment.robot_x = 4
        environment.robot_y = 2

        object_type = robot.detect_object()

        self.assertEqual(
            object_type,
            "A"
        )

    def test_pick_up_object(self):

        environment.robot_x = 4
        environment.robot_y = 2

        success = robot.pick_up_object()

        self.assertTrue(success)

        self.assertEqual(
            robot.get_carrying_object(),
            "A"
        )

        self.assertIsNone(
            environment.get_object_at((4, 2))
        )

    def test_cannot_pick_up_without_object(self):

        success = robot.pick_up_object()

        self.assertFalse(success)

        self.assertIsNone(
            robot.get_carrying_object()
        )

    def test_correct_sorting_zone(self):

        zone = environment.get_sorting_zone("A")

        self.assertEqual(
            zone,
            environment.A_ZONE
        )

        zone = environment.get_sorting_zone("B")

        self.assertEqual(
            zone,
            environment.B_ZONE
        )

    def test_drop_object_at_correct_zone(self):

        environment.robot_x, environment.robot_y = (
            environment.A_ZONE
        )

        robot.carrying_object = "A"

        success = robot.drop_object()

        self.assertTrue(success)

        self.assertIsNone(
            robot.get_carrying_object()
        )


if __name__ == "__main__":
    unittest.main()