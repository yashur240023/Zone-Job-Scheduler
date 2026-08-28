"""Task 5: Race condition and Peterson's Algorithm."""

import threading
import time


def unsynchronized_once():

    counter = {
        "value": 100
    }

    barrier = threading.Barrier(2)

    def update(delta):

        barrier.wait()

        old_value = counter["value"]

        # Deliberately create a race window.
        time.sleep(0.002)

        counter["value"] = (
            old_value + delta
        )

    subtract_thread = threading.Thread(
        target=update,
        args=(-40,)
    )

    add_thread = threading.Thread(
        target=update,
        args=(25,)
    )

    subtract_thread.start()
    add_thread.start()

    subtract_thread.join()
    add_thread.join()

    return counter["value"]


def peterson_once():

    counter = {
        "value": 100
    }

    # Peterson's shared variables.
    flag = [False, False]

    turn = 0

    # Used to make updates to the Python
    # shared state observable consistently.
    state_lock = threading.Lock()

    def set_flag(index, value):

        with state_lock:
            flag[index] = value

    def set_turn(value):

        nonlocal turn

        with state_lock:
            turn = value

    def snapshot():

        with state_lock:
            return flag[:], turn

    def enter(index):

        other = 1 - index

        set_flag(index, True)

        set_turn(other)

        while True:

            flags, current_turn = snapshot()

            if not (
                flags[other]
                and current_turn == other
            ):
                break

            time.sleep(0.0001)

    def leave(index):

        set_flag(
            index,
            False
        )

    def update(index, delta):

        enter(index)

        try:

            old_value = counter["value"]

            time.sleep(0.002)

            counter["value"] = (
                old_value + delta
            )

        finally:

            leave(index)

    subtract_thread = threading.Thread(
        target=update,
        args=(0, -40)
    )

    add_thread = threading.Thread(
        target=update,
        args=(1, 25)
    )

    subtract_thread.start()
    add_thread.start()

    subtract_thread.join()
    add_thread.join()

    return counter["value"]


if __name__ == "__main__":

    print("Unsynchronized runs:")

    bad_results = [
        unsynchronized_once()
        for _ in range(5)
    ]

    print(bad_results)

    print(
        "\nPeterson-protected runs:"
    )

    good_results = [
        peterson_once()
        for _ in range(5)
    ]

    print(good_results)

    assert any(
        result != 85
        for result in bad_results
    ), (
        "Race demo did not expose "
        "a wrong result."
    )

    assert good_results == [
        85,
        85,
        85,
        85,
        85
    ]
