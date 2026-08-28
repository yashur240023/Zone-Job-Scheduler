# Zone Job-Scheduler, Deadlock-Safety Engine & Secure Cloud-IoT Deployment Blueprint

## Project Overview

This project implements a scheduling, synchronization, deadlock-safety,
and memory-management compute engine for Tata Communications' Smart City
Network Operations scenario.

The project has two parts:

- Part 1: Runnable scheduling and operating-system algorithms.
- Part 2: Written secure Cloud-IoT deployment blueprint.

Part 2 describes how the exact Part 1 engine would be deployed as a
secure cloud-hosted platform. Part 2 does not replace the Part 1 engine
with a different implementation.

---

# Repository Structure

```text
zone_scheduler_project/
│
├── jobs.py
├── scheduling.py
├── round_robin.py
├── priority.py
├── synchronization.py
├── bankers.py
├── memory_translation.py
├── run_all.py
├── README.md
├── OUTPUT.txt
│
└── docs/
    └── architecture_blueprint.md
