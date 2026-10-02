class RobotState:

    IDLE = "IDLE"
    SEARCHING = "SEARCHING"
    NAVIGATING_TO_OBJECT = "NAVIGATING_TO_OBJECT"
    PICKING_UP = "PICKING_UP"
    CARRYING = "CARRYING"
    NAVIGATING_TO_ZONE = "NAVIGATING_TO_ZONE"
    SORTING = "SORTING"
    ERROR = "ERROR"


class StateMachine:

    def __init__(self):

        self.state = RobotState.IDLE

    def set_state(self, new_state):

        self.state = new_state

        print(
            f"State changed → {self.state}"
        )

    def get_state(self):

        return self.state

    def is_state(self, state):

        return self.state == state