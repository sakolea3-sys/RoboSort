import random

from environment import get_direction, get_distance


def get_front_direction():
    return get_direction()


def get_left_direction():
    directions = ["N", "E", "S", "W"]
    current = get_direction()

    index = directions.index(current)

    return directions[(index - 1) % 4]


def get_right_direction():
    directions = ["N", "E", "S", "W"]
    current = get_direction()

    index = directions.index(current)

    return directions[(index + 1) % 4]


def get_front_distance():
    distance = get_distance(get_front_direction())

    # Small simulated sensor noise
    noise = random.uniform(-1.5, 1.5)

    return max(0, distance + noise)


def get_left_distance():
    distance = get_distance(get_left_direction())

    noise = random.uniform(-1.5, 1.5)

    return max(0, distance + noise)


def get_right_distance():
    distance = get_distance(get_right_direction())

    noise = random.uniform(-1.5, 1.5)

    return max(0, distance + noise)


def get_all_distances():
    return {
        "front": get_front_distance(),
        "left": get_left_distance(),
        "right": get_right_distance()
    }


def filter_readings(readings):
    return sum(readings) / len(readings)


def get_filtered_front_distance():
    readings = []

    for _ in range(5):
        readings.append(get_front_distance())

    return filter_readings(readings)