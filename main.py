from simulation import simulation

from visualization import display_map


simulation.reset()

for _ in range(100):

    if simulation.finished:
        break

    simulation.step_simulation()

    state = simulation.get_state()

    print(
        f"Final position: {state['position']} | "
        f"Direction: {state['direction']}"
    )

    print(
        f"Robot state: {state['state']}"
    )

    if state["carrying"]:

        print(
            f"Carrying: Type {state['carrying']}"
        )

    else:

        print(
            "Carrying: Nothing"
        )

    display_map()

    print()


# ====================================
# FINAL ROBOT REPORT
# ====================================

print()
print("################################")
print("#      FINAL ROBOT REPORT       #")
print("################################")

statistics = simulation.get_state()["statistics"]

print(
    f"Objects sorted: "
    f"{statistics['objects_sorted']}"
)

print(
    f"Objects failed: "
    f"{statistics['objects_failed']}"
)

print(
    f"Sorting success rate: "
    f"{statistics['success_rate']:.1f}%"
)

print(
    f"Robot moves: "
    f"{statistics['total_moves']}"
)

print(
    f"Failed moves: "
    f"{statistics['failed_moves']}"
)

print(
    f"Planned path steps: "
    f"{statistics['planned_path_steps']}"
)

print("================================")