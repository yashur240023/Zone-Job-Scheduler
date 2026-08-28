"""Task 4: Priority scheduling with and without aging."""

from jobs import JOBS


def priority_schedule(
    aging=False,
    jobs=JOBS
):

    pending = list(jobs)

    current_time = 0

    rows = []

    while pending:

        ready = [
            job
            for job in pending
            if job["arrival_time"] <= current_time
        ]

        if not ready:

            current_time = min(
                job["arrival_time"]
                for job in pending
            )

            continue

        def priority_key(job):

            if aging:

                effective_priority = max(
                    1,
                    job["priority"]
                    - (
                        (
                            current_time
                            - job["arrival_time"]
                        ) // 3
                    )
                )

            else:

                effective_priority = job["priority"]

            return (
                effective_priority,
                job["arrival_time"],
                job["job_id"]
            )

        job = min(
            ready,
            key=priority_key
        )

        pending.remove(job)

        start = current_time

        current_time += job["burst_time"]

        completion = current_time

        waiting = (
            start
            - job["arrival_time"]
        )

        turnaround = (
            completion
            - job["arrival_time"]
        )

        rows.append({
            **job,
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return rows


def show(aging):

    rows = priority_schedule(
        aging=aging
    )

    label = (
        "with aging"
        if aging
        else "without aging"
    )

    print(
        f"\nPriority scheduling {label}"
    )

    print(
        "Job       Priority Waiting Turnaround"
    )

    for row in rows:

        print(
            f"{row['job_id']:<9} "
            f"{row['priority']:>8} "
            f"{row['waiting']:>7} "
            f"{row['turnaround']:>10}"
        )

    longest = max(
        rows,
        key=lambda row: row["waiting"]
    )

    average_waiting = (
        sum(row["waiting"] for row in rows)
        / len(rows)
    )

    print(
        f"Longest wait: "
        f"{longest['job_id']} "
        f"({longest['waiting']} ticks)"
    )

    print(
        f"Average waiting time: "
        f"{average_waiting:.3f}"
    )


if __name__ == "__main__":

    show(False)

    show(True)
