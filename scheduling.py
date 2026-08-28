"""Task 2: FCFS, non-preemptive SJF, and SRTF."""

from jobs import JOBS


def averages(rows):
    """Return average waiting and turnaround time."""
    average_waiting = sum(
        row["waiting"] for row in rows
    ) / len(rows)

    average_turnaround = sum(
        row["turnaround"] for row in rows
    ) / len(rows)

    return average_waiting, average_turnaround


def fcfs(jobs=JOBS):
    """First Come First Serve scheduling."""

    current_time = 0
    rows = []

    for job in jobs:

        current_time = max(
            current_time,
            job["arrival_time"]
        )

        start = current_time

        current_time += job["burst_time"]

        completion = current_time

        waiting = (
            start - job["arrival_time"]
        )

        turnaround = (
            completion - job["arrival_time"]
        )

        rows.append({
            **job,
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return rows


def sjf(jobs=JOBS):
    """
    Non-preemptive Shortest Job First.

    Tie-breaking:
    1. Shorter burst time
    2. Earlier arrival time
    3. Lower job_id
    """

    pending = list(jobs)
    current_time = 0
    rows = []

    while pending:

        ready = [
            job for job in pending
            if job["arrival_time"] <= current_time
        ]

        if not ready:
            current_time = min(
                job["arrival_time"]
                for job in pending
            )
            continue

        job = min(
            ready,
            key=lambda x: (
                x["burst_time"],
                x["arrival_time"],
                x["job_id"]
            )
        )

        pending.remove(job)

        start = current_time

        current_time += job["burst_time"]

        completion = current_time

        waiting = (
            start - job["arrival_time"]
        )

        turnaround = (
            completion - job["arrival_time"]
        )

        rows.append({
            **job,
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return rows


def srtf(jobs=JOBS):
    """
    Shortest Remaining Time First.

    Tie-breaking:
    1. Remaining time
    2. Earlier arrival time
    3. Lower job_id
    """

    remaining = {
        job["job_id"]: job["burst_time"]
        for job in jobs
    }

    completion = {}

    current_time = 0

    while len(completion) < len(jobs):

        ready = [
            job
            for job in jobs
            if (
                job["arrival_time"] <= current_time
                and job["job_id"] not in completion
            )
        ]

        if not ready:

            current_time = min(
                job["arrival_time"]
                for job in jobs
                if job["job_id"] not in completion
            )

            continue

        job = min(
            ready,
            key=lambda x: (
                remaining[x["job_id"]],
                x["arrival_time"],
                x["job_id"]
            )
        )

        job_id = job["job_id"]

        remaining[job_id] -= 1

        current_time += 1

        if remaining[job_id] == 0:
            completion[job_id] = current_time

    rows = []

    for job in jobs:

        turnaround = (
            completion[job["job_id"]]
            - job["arrival_time"]
        )

        waiting = (
            turnaround - job["burst_time"]
        )

        rows.append({
            **job,
            "completion": completion[job["job_id"]],
            "waiting": waiting,
            "turnaround": turnaround
        })

    return rows


def print_table(name, rows):

    print(f"\n{name}")

    print(
        "Job       Arrival Burst Start "
        "Completion Waiting Turnaround"
    )

    for row in rows:

        print(
            f"{row['job_id']:<9} "
            f"{row['arrival_time']:>7} "
            f"{row['burst_time']:>5} "
            f"{row.get('start', '-'):>5} "
            f"{row['completion']:>10} "
            f"{row['waiting']:>7} "
            f"{row['turnaround']:>10}"
        )

    average_waiting, average_turnaround = averages(rows)

    print(
        f"Average waiting time: "
        f"{average_waiting:.3f}"
    )

    print(
        f"Average turnaround time: "
        f"{average_turnaround:.3f}"
    )


if __name__ == "__main__":

    algorithms = [
        ("FCFS", fcfs),
        ("Non-preemptive SJF", sjf),
        ("SRTF", srtf)
    ]

    for name, function in algorithms:

        rows = function()

        print_table(
            name,
            rows
        )
