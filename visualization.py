import environment


def display_map():

    robot_x, robot_y = environment.get_position()
    direction = environment.get_direction()
    objects = environment.get_objects()
    dynamic_obstacles = environment.get_dynamic_obstacles()

    for y in range(environment.HEIGHT - 1, -1, -1):

        row = ""

        for x in range(environment.WIDTH):

            position = (x, y)

            if position == (robot_x, robot_y):

                if direction == "N":
                    row += "^"

                elif direction == "E":
                    row += ">"

                elif direction == "S":
                    row += "v"

                elif direction == "W":
                    row += "<"

            elif position in dynamic_obstacles:

                row += "X"

            elif position in environment.obstacles:

                row += "#"

            elif position in objects:

                row += objects[position]

            elif position == environment.A_ZONE:

                row += "A"

            elif position == environment.B_ZONE:

                row += "B"

            else:

                row += "."

        print(row)

    print()