"""Task 3: Round Robin with quantum 3 and 6."""

from collections import deque

from jobs import JOBS


def round_robin(quantum, jobs=JOBS):

    remaining = {
        job["job_id"]: job["burst_time"]
        for job in jobs
    }

    completion = {}

    ready_queue = deque()

    current_time = 0

    slices = []

    last_job = None

    context_switches = 0

    arrived = set()

    def enqueue_arrivals(up_to):

        for job in jobs:

            if (
                job["job_id"] not in arrived
                and job["arrival_time"] <= up_to
            ):

                ready_queue.append(
                    job["job_id"]
                )

                arrived.add(
                    job["job_id"]
                )

    while len(completion) < len(jobs):

        enqueue_arrivals(current_time)

        if not ready_queue:

            current_time = min(
                job["arrival_time"]
                for job in jobs
                if job["job_id"] not in arrived
            )

            enqueue_arrivals(current_time)

        job_id = ready_queue.popleft()

        if (
            last_job is not None
            and job_id != last_job
        ):
            context_switches += 1

        last_job = job_id

        start = current_time

        run_time = min(
            quantum,
            remaining[job_id]
        )

        remaining[job_id] -= run_time

        current_time += run_time

        slices.append(
            (
                job_id,
                start,
                current_time
            )
        )

        # Important boundary rule:
        # New arrivals at exactly current_time
        # are added BEFORE the expired job.
        enqueue_arrivals(current_time)

        if remaining[job_id] == 0:

            completion[job_id] = current_time

        else:

            ready_queue.append(job_id)

    rows = []

    for job in jobs:

        turnaround = (
            completion[job["job_id"]]
            - job["arrival_time"]
        )

        waiting = (
            turnaround
            - job["burst_time"]
        )

        rows.append({
            **job,
            "completion": completion[job["job_id"]],
            "waiting": waiting,
            "turnaround": turnaround
        })

    return rows, slices, context_switches


def show(quantum):

    rows, slices, switches = round_robin(
        quantum
    )

    print(
        f"\nRound Robin "
        f"(quantum={quantum})"
    )

    print("Dispatch slices:")

    print(
        " -> ".join(
            f"{job_id}[{start},{end})"
            for job_id, start, end in slices
        )
    )

    print(
        "Job       Waiting Turnaround"
    )

    for row in rows:

        print(
            f"{row['job_id']:<9} "
            f"{row['waiting']:>7} "
            f"{row['turnaround']:>10}"
        )

    average_waiting = (
        sum(row["waiting"] for row in rows)
        / len(rows)
    )

    average_turnaround = (
        sum(row["turnaround"] for row in rows)
        / len(rows)
    )

    print(
        f"Average waiting time: "
        f"{average_waiting:.3f}"
    )

    print(
        f"Average turnaround time: "
        f"{average_turnaround:.3f}"
    )

    print(
        f"Context switches (job changes): "
        f"{switches}"
    )


if __name__ == "__main__":

    show(3)

    show(6)

    print(
        "\nTheory statement: quantum 3 causes "
        "more real OS switching overhead than "
        "quantum 6 because it produces 16 job "
        "changes versus 10 in this zero-cost "
        "simulation. In a real OS, those additional "
        "switches would consume CPU time."
    )
