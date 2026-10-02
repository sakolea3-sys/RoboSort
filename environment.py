WIDTH = 20
HEIGHT = 20


# Static obstacles on the map
obstacles = {
    (6, 2),
    (6, 3),
    (6, 4),
    (10, 5),
    (11, 5),
    (12, 5),
    (14, 10),
    (14, 11),
    (14, 12),
    (5, 15),
    (6, 15),
    (7, 15)
}


# Dynamic obstacles
dynamic_obstacles = set()


# Objects on the map
objects = {
    (4, 2): "A",
    (9, 8): "B",
    (16, 6): "A",
    (12, 15): "B"
}


# Sorting zones
A_ZONE = (1, 18)
B_ZONE = (18, 18)


# Robot starting position
robot_x = 2
robot_y = 2


# Robot direction
direction = "E"


def get_position():
    return robot_x, robot_y


def get_direction():
    return direction


def get_objects():
    return objects


def get_object_at(position):
    return objects.get(position)


def remove_object(position):

    if position in objects:
        del objects[position]


def get_sorting_zone(object_type):

    if object_type == "A":
        return A_ZONE

    elif object_type == "B":
        return B_ZONE

    return None


def get_nearest_object():

    if not objects:
        return None

    nearest_position = None
    nearest_type = None
    nearest_distance = None

    for position, object_type in objects.items():

        distance = (
            abs(position[0] - robot_x)
            + abs(position[1] - robot_y)
        )

        if (
            nearest_distance is None
            or distance < nearest_distance
        ):

            nearest_distance = distance
            nearest_position = position
            nearest_type = object_type

    return nearest_position, nearest_type


def add_dynamic_obstacle(position):

    if is_valid_position(position):

        dynamic_obstacles.add(position)

        print(
            f"Dynamic obstacle appeared at "
            f"{position}"
        )

        return True

    return False


def remove_dynamic_obstacle(position):

    dynamic_obstacles.discard(position)


def get_dynamic_obstacles():

    return dynamic_obstacles


def is_valid_position(position):

    x, y = position

    if x < 0 or x >= WIDTH:
        return False

    if y < 0 or y >= HEIGHT:
        return False

    if position in obstacles:
        return False

    if position in dynamic_obstacles:
        return False

    return True


def get_neighbors(position):

    x, y = position

    possible_neighbors = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    neighbors = []

    for neighbor in possible_neighbors:

        if is_valid_position(neighbor):
            neighbors.append(neighbor)

    return neighbors


def turn_left():

    global direction

    directions = ["N", "W", "S", "E"]

    direction = directions[
        (directions.index(direction) + 1) % 4
    ]


def turn_right():

    global direction

    directions = ["N", "E", "S", "W"]

    direction = directions[
        (directions.index(direction) + 1) % 4
    ]


def move_forward():

    global robot_x, robot_y

    new_x = robot_x
    new_y = robot_y

    if direction == "N":
        new_y += 1

    elif direction == "E":
        new_x += 1

    elif direction == "S":
        new_y -= 1

    elif direction == "W":
        new_x -= 1

    if not is_valid_position((new_x, new_y)):
        return False

    robot_x = new_x
    robot_y = new_y

    return True


def get_distance(direction_to_check):

    x = robot_x
    y = robot_y

    distance = 0

    while True:

        if direction_to_check == "N":
            y += 1

        elif direction_to_check == "E":
            x += 1

        elif direction_to_check == "S":
            y -= 1

        elif direction_to_check == "W":
            x -= 1

        if (
            x < 0
            or x >= WIDTH
            or y < 0
            or y >= HEIGHT
        ):

            return distance * 10

        if (
            (x, y) in obstacles
            or (x, y) in dynamic_obstacles
        ):

            return distance * 10

        distance += 1