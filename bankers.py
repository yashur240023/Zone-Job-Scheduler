"""Task 6: Banker's Algorithm."""

AVAILABLE = [
    3,
    3,
    2
]

MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2]
}

ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1]
}


def need_matrix(
    max_need=MAX_NEED,
    allocation=ALLOCATION
):

    return {
        process: [
            max_need[process][i]
            - allocation[process][i]
            for i in range(3)
        ]
        for process in max_need
    }


def safety(
    available,
    allocation,
    need
):

    work = available[:]

    finish = {
        process: False
        for process in need
    }

    sequence = []

    changed = True

    while changed:

        changed = False

        for process in need:

            if (
                not finish[process]
                and all(
                    need[process][i]
                    <= work[i]
                    for i in range(3)
                )
            ):

                work = [
                    work[i]
                    + allocation[process][i]
                    for i in range(3)
                ]

                finish[process] = True

                sequence.append(process)

                changed = True

    return (
        all(finish.values()),
        sequence
    )


def request(
    process,
    request_vector
):

    # Always start from original state.
    need = need_matrix()

    # Check Need.
    if any(
        request_vector[i]
        > need[process][i]
        for i in range(3)
    ):

        return (
            False,
            "denied: request exceeds "
            "the process's Need"
        )

    # Check Available.
    if any(
        request_vector[i]
        > AVAILABLE[i]
        for i in range(3)
    ):

        return (
            False,
            "denied: request exceeds Available"
        )

    # Create hypothetical state.
    new_available = [
        AVAILABLE[i]
        - request_vector[i]
        for i in range(3)
    ]

    new_allocation = {
        process_name:
        ALLOCATION[process_name][:]
        for process_name in ALLOCATION
    }

    new_need = {
        process_name:
        need[process_name][:]
        for process_name in need
    }

    # Pretend to allocate.
    new_allocation[process] = [
        new_allocation[process][i]
        + request_vector[i]
        for i in range(3)
    ]

    new_need[process] = [
        new_need[process][i]
        - request_vector[i]
        for i in range(3)
    ]

    safe, sequence = safety(
        new_available,
        new_allocation,
        new_need
    )

    if safe:

        return (
            True,
            "granted; resulting state is safe, "
            f"sequence={sequence}"
        )

    return (
        False,
        "denied: granting this request "
        "would leave the system in an unsafe state"
    )


if __name__ == "__main__":

    need = need_matrix()

    print(
        "Need matrix:",
        need
    )

    safe, sequence = safety(
        AVAILABLE,
        ALLOCATION,
        need
    )

    print(
        "Initial state safe:",
        safe
    )

    print(
        "One safe sequence:",
        sequence
    )

    requests = [
        ("P1", [1, 0, 2]),
        ("P0", [2, 0, 2])
    ]

    for process, request_vector in requests:

        result, message = request(
            process,
            request_vector
        )

        print(
            f"{process} requests "
            f"{request_vector}: {message}"
        )
