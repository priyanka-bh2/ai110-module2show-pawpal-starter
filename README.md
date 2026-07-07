# PawPal+ (Module 2 Project)

PawPal+ is a beginner-friendly pet care scheduler built with Python and Streamlit. It helps a pet owner track tasks, keep routines consistent, and generate a daily plan with clear explanations.

## Overview

A busy pet owner needs help staying on top of feeding, walking, medication, grooming, and other care tasks. PawPal+ stores owner and pet data, organizes tasks, and builds a schedule using simple rules.

This implementation includes:

- sorting tasks by time for readable order
- filtering tasks by pet and by completion status
- recurring daily and weekly tasks with rollover
- conflict warnings for duplicate scheduled times
- schedule generation with task ranking and sorting
- a small pytest suite with 6 passing tests

## Sample CLI Output

When the scheduler runs in `main.py`, the output looks like:

```
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

The plan is sorted by time and shows the pet name, task description, and priority.

## 🧪 Testing PawPal+

Run the test suite to verify core scheduling behaviors:

```bash
# Run all tests:
pytest tests/

# Run the single file:
pytest tests/test_pawpal.py

# Run with verbose output:
pytest tests/ -v
```

This project includes 6 focused tests covering:

- sorting tasks chronologically
- filtering incomplete tasks
- filtering tasks for a single pet
- completing daily tasks and adding the next occurrence
- detecting exact time conflicts
- generating an ordered schedule

## 📐 Smarter Scheduling

PawPal+ uses clear rules that are easy to understand and extend.

- sorting by time: `Scheduler.sort_tasks_by_time()` orders timed tasks first by hour and minute.
- filtering by pet and completion: `Scheduler.filter_tasks()` can return only one pet's tasks or only pending tasks.
- recurring daily/weekly tasks: `Scheduler.complete_task()` marks tasks complete and creates the next task for the following day or week.
- conflict warnings: `Scheduler.detect_conflicts()` checks the generated schedule for tasks with the same date and time and produces readable warnings.
- schedule generation: `Scheduler.generate_plan()` collects pending tasks, ranks them, removes duplicates, and returns a final ordered plan.

These behaviors make PawPal+ a helpful starter scheduler without requiring advanced optimization techniques.

## 📸 Demo Walkthrough

Use the Streamlit UI in `app.py` to experience PawPal+ step by step.

1. **Set owner info**
- Run `streamlit run app.py`.
- Enter your name in the Owner section.

2. **Add a pet**
- Provide a pet name, species, and age.
- Click Add pet.
- The pet appears in the pet list.

3. **Add tasks**
- Choose a pet from the task form.
- Enter a description, date, and time.
- Set duration, priority, and frequency (`none`, `daily`, or `weekly`).
- Click Add task.
- The task appears under the pet's current tasks.

4. **View tasks by pet**
- Open the pet card in the task list.
- See pending tasks and their due dates.

5. **Generate a schedule**
- Pick a date and generate the schedule.
- PawPal+ shows ordered tasks with time, pet, description, and priority.
- Review conflict warnings if any tasks share the same scheduled datetime.

This README reflects the final implementation and the core PawPal+ scheduling behaviors.
