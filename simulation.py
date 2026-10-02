import environment

from sensor import (
    get_filtered_front_distance,
    get_left_distance,
    get_right_distance
)

from robot import (
    sort,
    detect_object,
    navigate_to_object,
    navigate_to_position,
    pick_up_object,
    drop_object,
    get_carrying_object,
    get_position,
    get_direction,
    get_statistics
)

from state_machine import (
    StateMachine,
    RobotState
)


class Simulation:

    def __init__(self):

        self.state_machine = StateMachine()

        self.step = 0
        self.running = False
        self.finished = False

        self.front = 0
        self.left = 0
        self.right = 0

        self.activity_log = []

        self.reset()

    def reset(self):

        # -----------------------------
        # Reset environment
        # -----------------------------

        environment.dynamic_obstacles.clear()

        environment.robot_x = 2
        environment.robot_y = 2
        environment.direction = "E"

        environment.objects.clear()

        environment.objects.update({
            (4, 2): "A",
            (9, 8): "B",
            (16, 6): "A",
            (12, 15): "B"
        })

        # -----------------------------
        # Reset robot
        # -----------------------------

        import robot

        robot.carrying_object = None
        robot.current_path = None
        robot.state = "IDLE"

        # -----------------------------
        # Reset statistics
        # -----------------------------

        robot.statistics.objects_sorted = 0
        robot.statistics.objects_failed = 0
        robot.statistics.total_moves = 0
        robot.statistics.failed_moves = 0
        robot.statistics.total_path_steps = 0

        # -----------------------------
        # Reset state machine
        # -----------------------------

        self.state_machine = StateMachine()

        # -----------------------------
        # Reset simulation
        # -----------------------------

        self.step = 0
        self.running = False
        self.finished = False

        self.front = 0
        self.left = 0
        self.right = 0

        self.activity_log = []

    def log_activity(self, message):

        self.activity_log.append({
            "step": self.step,
            "message": message
        })

        # Keep only the latest 20 events
        self.activity_log = self.activity_log[-20:]

    def step_simulation(self):

        # Do nothing if simulation has finished
        if self.finished:
            return self.get_state()

        print("================================")
        print(f"Simulation step: {self.step}")

        # -----------------------------
        # Add dynamic obstacle
        # -----------------------------

        if self.step == 25:

            x, y = environment.get_position()
            direction = environment.get_direction()

            if direction == "N":
                obstacle_position = (x, y + 1)

            elif direction == "E":
                obstacle_position = (x + 1, y)

            elif direction == "S":
                obstacle_position = (x, y - 1)

            else:
                obstacle_position = (x - 1, y)

            added = environment.add_dynamic_obstacle(
                obstacle_position
            )

            if added:
                self.log_activity(
                    f"Dynamic obstacle appeared at {obstacle_position}"
                )

        # -----------------------------
        # Sensor readings
        # -----------------------------

        self.front = get_filtered_front_distance()
        self.left = get_left_distance()
        self.right = get_right_distance()

        position = get_position()
        direction = get_direction()

        print(
            f"Position: {position} | "
            f"Direction: {direction}"
        )

        print(
            f"Front: {self.front:.1f} cm | "
            f"Left: {self.left:.1f} cm | "
            f"Right: {self.right:.1f} cm"
        )

        # -----------------------------
        # Check carrying status
        # -----------------------------

        carrying = get_carrying_object()

        if carrying:

            self.state_machine.set_state(
                RobotState.CARRYING
            )

            self.log_activity(
                f"Carrying Type {carrying}"
            )

            print(
                f"Carrying object Type {carrying}"
            )

            target_zone = environment.get_sorting_zone(
                carrying
            )

            if position == target_zone:

                self.state_machine.set_state(
                    RobotState.SORTING
                )

                self.log_activity(
                    f"Sorting Type {carrying}"
                )

                sort()

                drop_object()

                self.state_machine.set_state(
                    RobotState.IDLE
                )

            else:

                self.state_machine.set_state(
                    RobotState.NAVIGATING_TO_ZONE
                )

                self.log_activity(
                    f"Navigating to sorting zone {target_zone}"
                )

                print(
                    f"Navigating to sorting zone "
                    f"{target_zone}"
                )

                navigate_to_position(
                    target_zone
                )

        # -----------------------------
        # Search for object
        # -----------------------------

        else:

            self.state_machine.set_state(
                RobotState.SEARCHING
            )

            object_type = detect_object()

            if object_type:

                self.state_machine.set_state(
                    RobotState.PICKING_UP
                )

                self.log_activity(
                    f"Object Type {object_type} detected"
                )

                print(
                    f"Preparing to pick up "
                    f"Type {object_type}"
                )

                self.log_activity(
                    f"Picking up Type {object_type}"
                )

                pick_up_object()

            else:

                self.state_machine.set_state(
                    RobotState.NAVIGATING_TO_OBJECT
                )

                self.log_activity(
                    "Searching for nearest object"
                )

                print(
                    "Searching for nearest object..."
                )

                navigate_to_object()

        # -----------------------------
        # Check if simulation is finished
        # -----------------------------

        if (
            not environment.get_objects()
            and get_carrying_object() is None
        ):

            if not self.finished:

                self.log_activity(
                    "All objects sorted - simulation finished"
                )

            self.finished = True
            self.running = False

        self.step += 1

        return self.get_state()

    def run(self, steps=100):

        self.running = True

        self.log_activity(
            "Simulation started"
        )

        for _ in range(steps):

            if self.finished:
                break

            self.step_simulation()

        self.running = False

        if not self.finished:

            self.log_activity(
                "Simulation stopped after reaching step limit"
            )

        return self.get_state()

    def start(self):

        if not self.finished:

            self.running = True

            self.log_activity(
                "Simulation started"
            )

    def stop(self):

        self.running = False

        self.log_activity(
            "Simulation stopped"
        )

    def get_state(self):

        statistics = get_statistics()

        return {

            # -------------------------
            # Simulation information
            # -------------------------

            "step": self.step,

            "running": self.running,

            "finished": self.finished,

            # -------------------------
            # Robot information
            # -------------------------

            "position": get_position(),

            "direction": get_direction(),

            "state": self.state_machine.get_state(),

            "carrying": get_carrying_object(),

            # -------------------------
            # Sensor information
            # -------------------------

            "sensors": {

                "front":
                    round(self.front, 1),

                "left":
                    round(self.left, 1),

                "right":
                    round(self.right, 1)
            },

            # -------------------------
            # Environment information
            # -------------------------

            "environment": {

                "width":
                    environment.WIDTH,

                "height":
                    environment.HEIGHT,

                "static_obstacles": [

                    list(position)

                    for position
                    in environment.obstacles
                ],

                "dynamic_obstacles": [

                    list(position)

                    for position
                    in environment.get_dynamic_obstacles()
                ],

                "zones": {

                    "A":
                        list(environment.A_ZONE),

                    "B":
                        list(environment.B_ZONE)
                }
            },

            # -------------------------
            # Object information
            # -------------------------

            "objects": {

                "remaining":
                    len(
                        environment.get_objects()
                    ),

                "locations": [

                    {
                        "position":
                            list(position),

                        "type":
                            object_type
                    }

                    for position, object_type
                    in environment.get_objects().items()
                ]
            },

            # -------------------------
            # Statistics
            # -------------------------

            "statistics": {

                "objects_sorted":
                    statistics.objects_sorted,

                "objects_failed":
                    statistics.objects_failed,

                "success_rate":
                    round(
                        statistics.get_sorting_success_rate(),
                        1
                    ),

                "total_moves":
                    statistics.total_moves,

                "failed_moves":
                    statistics.failed_moves,

                "planned_path_steps":
                    statistics.total_path_steps
            },

            # -------------------------
            # Activity log
            # -------------------------

            "activity_log":
                self.activity_log
        }


simulation = Simulation()