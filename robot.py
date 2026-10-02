import environment

from sensor import get_filtered_front_distance

from statistics import Statistics


state = "IDLE"

carrying_object = None

statistics = Statistics()

current_path = None


def move_forward():

    global state

    # Check the front sensor before moving
    front_distance = get_filtered_front_distance()

    if front_distance <= 5:

        state = "AVOIDING"

        statistics.record_failed_move()

        print(
            f"Sensor detected obstacle "
            f"at {front_distance:.1f} cm!"
        )

        print(
            "Robot stops for safety."
        )

        return False

    success = environment.move_forward()

    if success:

        state = "MOVING"

        statistics.record_move()

        print("Robot moves forward.")

        return True

    else:

        state = "AVOIDING"

        statistics.record_failed_move()

        print(
            "Robot cannot move forward! "
            "Obstacle or boundary detected."
        )

        return False


def stop():

    global state

    state = "IDLE"

    print("Robot stops.")


def turn_left():

    global state

    environment.turn_left()

    state = "TURNING LEFT"

    print("Robot turns left.")


def turn_right():

    global state

    environment.turn_right()

    state = "TURNING RIGHT"

    print("Robot turns right.")


def avoid_obstacle():

    global state

    state = "AVOIDING"

    print("Robot is avoiding an obstacle.")


def sort():

    global state

    state = "SORTING"

    print("Robot is sorting an object.")


def detect_object():

    position = environment.get_position()

    object_type = environment.get_object_at(position)

    if object_type:

        print(
            f"Object detected at {position}: "
            f"Type {object_type}"
        )

        return object_type

    return None


def find_nearest_object():

    result = environment.get_nearest_object()

    if result is None:

        print("No objects remaining.")

        return None

    position, object_type = result

    print(
        f"Nearest object: Type {object_type} "
        f"at {position}"
    )

    return position, object_type


def heuristic(position, goal):

    return (
        abs(position[0] - goal[0])
        + abs(position[1] - goal[1])
    )


def find_path(start, goal):

    open_list = [start]

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: heuristic(start, goal)
    }

    while open_list:

        current = min(
            open_list,
            key=lambda position: f_score.get(
                position,
                float("inf")
            )
        )

        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        open_list.remove(current)

        for neighbor in environment.get_neighbors(current):

            tentative_g_score = (
                g_score[current] + 1
            )

            if tentative_g_score < g_score.get(
                neighbor,
                float("inf")
            ):

                came_from[neighbor] = current

                g_score[neighbor] = (
                    tentative_g_score
                )

                f_score[neighbor] = (
                    tentative_g_score
                    + heuristic(neighbor, goal)
                )

                if neighbor not in open_list:

                    open_list.append(neighbor)

    return None


def follow_path(path):

    if path is None or len(path) < 2:

        return False

    next_position = path[1]

    current_x, current_y = environment.get_position()

    next_x, next_y = next_position

    if next_x > current_x:

        while environment.get_direction() != "E":
            turn_right()

    elif next_x < current_x:

        while environment.get_direction() != "W":
            turn_right()

    elif next_y > current_y:

        while environment.get_direction() != "N":
            turn_right()

    elif next_y < current_y:

        while environment.get_direction() != "S":
            turn_right()

    return move_forward()


def navigate_to_position(target_position):

    global current_path

    current_position = environment.get_position()

    # Create a path only when necessary
    if (
        current_path is None
        or len(current_path) < 2
        or current_path[-1] != target_position
    ):

        current_path = find_path(
            current_position,
            target_position
        )

        if current_path is None:

            print(
                f"No path found to "
                f"{target_position}"
            )

            statistics.record_failed_object()

            return False

        path_steps = len(current_path) - 1

        statistics.record_path(
            path_steps
        )

        print(
            f"Path found to {target_position}: "
            f"{path_steps} steps"
        )

    # Already at target
    if current_position == target_position:

        current_path = None

        return True

    # Follow the next step
    success = follow_path(current_path)

    if not success:

        # Sensor blocked the planned movement.
        # Discard the old path so it can be
        # recalculated on the next cycle.
        current_path = None

        print(
            "Navigation interrupted. "
            "Path will be recalculated."
        )

        return False

    # Remove the position we just reached
    if len(current_path) > 1:

        current_path.pop(0)

    return True


def navigate_to_object():

    target = find_nearest_object()

    if target is None:
        return False

    target_position, object_type = target

    return navigate_to_position(
        target_position
    )


def pick_up_object():

    global carrying_object
    global state
    global current_path

    position = environment.get_position()

    object_type = environment.get_object_at(
        position
    )

    if object_type:

        carrying_object = object_type

        environment.remove_object(position)

        current_path = None

        state = "CARRYING"

        print(
            f"Picked up object Type "
            f"{object_type}."
        )

        return True

    print("No object available to pick up.")

    return False


def get_carrying_object():

    return carrying_object


def drop_object():

    global carrying_object
    global state
    global current_path

    if carrying_object is None:

        print("Robot is not carrying an object.")

        return False

    zone = environment.get_sorting_zone(
        carrying_object
    )

    current_position = environment.get_position()

    if current_position == zone:

        print(
            f"Object Type {carrying_object} "
            f"successfully sorted!"
        )

        statistics.record_sorted_object()

        carrying_object = None

        current_path = None

        state = "IDLE"

        return True

    print(
        "Robot is not at the correct "
        "sorting zone."
    )

    return False


def get_statistics():

    return statistics


def get_state():

    return state


def get_position():

    return environment.get_position()


def get_direction():

    return environment.get_direction()