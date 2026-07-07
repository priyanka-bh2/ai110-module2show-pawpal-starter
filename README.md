Here’s a polished updated `README.md` version you can use:

```md
# PawPal+ (Module 2 Project)

PawPal+ is a beginner-friendly pet care scheduler built with Python and Streamlit. It helps a pet owner track care tasks, stay consistent with routines, and generate a daily plan with clear explanations.

## Overview

A busy pet owner needs help staying on top of feeding, walking, medication, grooming, enrichment, and other pet care responsibilities. PawPal+ stores owner and pet information, organizes tasks, and builds a schedule using simple, explainable rules.

### Features

- Owner and pet management
- Task creation and tracking
- Sorting tasks by time for readable schedules
- Filtering tasks by pet and completion status
- Recurring daily and weekly task rollover
- Conflict warnings for duplicate scheduled times
- Schedule generation with explanation text
- Automated pytest coverage for key scheduling behaviors

## Sample CLI Output

When the scheduler runs in `main.py`, the output looks like this:

```bash
Today's Schedule
====================
1. 08:00 | Bella | Morning walk | Priority: high
2. 12:00 | Bella | Lunch check | Priority: medium
3. 18:30 | Luna | Evening play | Priority: low

Summary
--------------------
Planned tasks:
- Morning walk for Bella (priority: high, due: 2026-07-06)
- Lunch check for Bella (priority: medium, due: 2026-07-06)
- Evening play for Luna (priority: low, due: 2026-07-06)
```

The generated plan is displayed in schedule order and includes the time, pet name, task description, and priority level.

## 🧪 Testing PawPal+

Run the automated test suite from the project root:

```bash
python -m pytest
```

These tests verify the most important backend behaviors in PawPal+, including:

- sorting tasks in chronological order
- filtering tasks by pet and completion status
- recurring task creation for daily tasks
- conflict detection for duplicate scheduled times
- basic schedule generation behavior

**Confidence Level:** ★★★★☆ (4/5)

Example successful test run:

```bash
rootdir: /Users/priyanka/Downloads/Codepath/Week3/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 6 items

tests/test_pawpal.py ......                      [100%]

================== 6 passed in 0.02s ===================
```

## 📐 Smarter Scheduling

PawPal+ uses simple scheduling rules that are easy to understand, test, and extend.

- **Sorting by time:** `Scheduler.sort_tasks_by_time()` orders timed tasks first by hour and minute, with untimed tasks placed at the end.
- **Filtering:** `Scheduler.filter_tasks()` can return tasks for one pet only, pending tasks only, or all tasks.
- **Recurring tasks:** `Scheduler.complete_task()` marks a recurring task complete and creates the next daily or weekly occurrence automatically.
- **Conflict warnings:** `Scheduler.detect_conflicts()` scans scheduled items for duplicate date-and-time slots and returns readable warnings instead of crashing the system.
- **Schedule generation:** `Scheduler.generate_plan()` gathers pending tasks, ranks them, removes duplicates, and returns the final plan.
- **Plan explanation:** `Scheduler.explain_plan()` produces a human-readable explanation of the scheduled tasks so the user can understand why tasks appear in the plan.

These behaviors make PawPal+ a helpful starter scheduler without requiring advanced optimization techniques or a heavy rule engine.

## 📸 Demo Walkthrough

Use the Streamlit UI in `app.py` to experience PawPal+ step by step.

1. **Set owner info**  
Run `streamlit run app.py` and enter your name in the Owner section.

2. **Add a pet**  
Enter a pet name, species, and age, then click **Add pet**. The pet appears in the pet list.

3. **Add tasks**  
Choose a pet, enter a task description, select a due date and time, set duration, priority, and frequency (`none`, `daily`, or `weekly`), then click **Add task**.

4. **Review current tasks**  
Open the pet’s task section to view pending tasks and their due dates before generating a schedule.

5. **Generate a schedule**  
Pick a date and click **Generate schedule**. PawPal+ displays an ordered task table, highlights any scheduling conflicts with warnings, and shows the scheduling rationale in a separate expandable section.

## Project Structure

```bash
.
├── app.py
├── main.py
├── pawpal_system.py
├── tests/
│   └── test_pawpal.py
├── diagrams/
│   └── uml_final.mmd
├── README.md
└── reflection.md
```

## Notes

This project intentionally favors readable, beginner-friendly scheduling logic over complex optimization. The scheduler focuses on clarity, predictable behavior, and explainable results, making it a strong foundation for future improvements such as persistence, weighted priority scheduling, or overlap-aware conflict handling.
```