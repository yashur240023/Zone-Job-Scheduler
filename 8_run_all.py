"""Run all Part 1 tasks."""

import scheduling
import round_robin
import priority
import synchronization
import bankers
import memory_translation


print("=" * 72)
print("TASK 2")
print("=" * 72)


algorithms = [
    ("FCFS", scheduling.fcfs),
    ("Non-preemptive SJF", scheduling.sjf),
    ("SRTF", scheduling.srtf)
]

for name, function in algorithms:

    rows = function()

    scheduling.print_table(
        name,
        rows
    )


print("=" * 72)
print("TASK 3")
print("=" * 72)

round_robin.show(3)

round_robin.show(6)

print(
    "\nTheory statement: quantum 3 causes "
    "more real OS switching overhead than "
    "quantum 6 because it produces 16 job "
    "changes versus 10 in this zero-cost "
    "simulation, so more switches would "
    "incur more real context-switch cost."
)


print("=" * 72)
print("TASK 4")
print("=" * 72)

priority.show(False)

priority.show(True)


print("=" * 72)
print("TASK 5")
print("=" * 72)

bad_results = [
    synchronization.unsynchronized_once()
    for _ in range(5)
]

good_results = [
    synchronization.peterson_once()
    for _ in range(5)
]

print(
    "Unsynchronized:",
    bad_results
)

print(
    "Peterson:",
    good_results
)

assert any(
    value != 85
    for value in bad_results
)

assert good_results == [
    85,
    85,
    85,
    85,
    85
]


print("=" * 72)
print("TASK 6")
print("=" * 72)

need = bankers.need_matrix()

print(
    "Need:",
    need
)

print(
    "Initial safe:",
    bankers.safety(
        bankers.AVAILABLE,
        bankers.ALLOCATION,
        need
    )
)

requests = [
    ("P1", [1, 0, 2]),
    ("P0", [2, 0, 2])
]

for process, request_vector in requests:

    print(
        process,
        request_vector,
        bankers.request(
            process,
            request_vector
        )
    )


print("=" * 72)
print("TASK 7")
print("=" * 72)

for address in [
    260,
    1500,
    3000,
    5000
]:

    print(
        address,
        memory_translation.translate_page(
            address
        )
    )


for pair in [
    (0, 150),
    (1, 350),
    (2, 100)
]:

    print(
        pair,
        memory_translation.translate_segment(
            *pair
        )
    )
