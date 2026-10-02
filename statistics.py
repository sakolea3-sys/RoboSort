class Statistics:

    def __init__(self):

        self.objects_sorted = 0
        self.objects_failed = 0
        self.total_moves = 0
        self.failed_moves = 0
        self.total_path_steps = 0

    def record_move(self):

        self.total_moves += 1

    def record_failed_move(self):

        self.failed_moves += 1

    def record_sorted_object(self):

        self.objects_sorted += 1

    def record_failed_object(self):

        self.objects_failed += 1

    def record_path(self, steps):

        self.total_path_steps += steps

    def get_sorting_success_rate(self):

        total_objects = (
            self.objects_sorted
            + self.objects_failed
        )

        if total_objects == 0:
            return 0

        return (
            self.objects_sorted
            / total_objects
        ) * 100

    def display(self):

        print()
        print("========== STATISTICS ==========")

        print(
            f"Objects sorted: "
            f"{self.objects_sorted}"
        )

        print(
            f"Objects failed: "
            f"{self.objects_failed}"
        )

        print(
            f"Sorting success rate: "
            f"{self.get_sorting_success_rate():.1f}%"
        )

        print(
            f"Robot moves: "
            f"{self.total_moves}"
        )

        print(
            f"Failed moves: "
            f"{self.failed_moves}"
        )

        print(
            f"Planned path steps: "
            f"{self.total_path_steps}"
        )

        print("================================")