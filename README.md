# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Here's what the CLI output looks like when you run the scheduler in `main.py`:

```
Today's Schedule
====================
1. 08:00 | Bella | Morning walk | Priority: high
2. 18:00 | Bella | Dinner feed | Priority: medium
3. 19:30 | Luna | Clean litter box | Priority: high

Summary
--------------------
Planned tasks:
- Morning walk for Bella (priority: high, due: 2026-07-06)
- Dinner feed for Bella (priority: medium, due: 2026-07-06)
- Clean litter box for Luna (priority: high, due: 2026-07-06)
```

Tasks are sorted by priority and displayed with time, pet name, description, and priority level for easy reference.

## 🧪 Testing PawPal+

Run the test suite to verify scheduling logic and data model behaviors:

```bash
# Run the full test suite:
pytest tests/

# Run with verbose output:
pytest tests/ -v

# Run with coverage report:
pytest tests/ --cov=pawpal_system --cov-report=term-missing
```

**Sample test output:**

```
tests/test_pawpal.py::test_mark_complete_changes_task_status PASSED
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED

============================== 2 passed in 0.01s ==============================
```

Key tests cover task completion, pet task management, and scheduling logic.

## 📐 Smarter Scheduling

PawPal+ uses clear, beginner-friendly rules to order tasks and flag problems. The goal is to be easy to read and explain, while covering the common scheduling needs of a single pet owner.

- Task ranking: tasks are scored by `Task.estimate_score()` which considers priority (high/medium/low), due date urgency (overdue or same-day), and whether the task has a set time. `Scheduler.score_task()` applies this score when building a plan.
- Filtering: completed tasks are excluded from daily plans using `Pet.get_tasks(include_completed=False)` so the schedule shows only pending work.
- Sorting by time: when you want a human-readable order for a list of tasks, use `Scheduler.sort_tasks_by_time()` — it sorts tasks with times first (by hour/minute) and places untimed tasks last.
- Recurring tasks: when you complete a recurring task (daily or weekly), `Scheduler.complete_task()` marks it done and automatically creates the next occurrence by adding a `timedelta` (1 day or 7 days). This is simple and easy to follow for beginners.
- Conflict detection: `Scheduler.detect_conflicts()` groups scheduled items by exact date+time and produces readable warnings (for example, two tasks at `2026-07-06 18:00`). Warnings are non-fatal so the app never crashes; you can decide how to resolve conflicts manually or extend this to auto-reschedule later.

How to see these features in the demo:

1. Run the CLI demo: `python main.py`. The demo shows sorted tasks, filtering by pet, completing a recurring task (which creates the next one), and prints conflict warnings.
2. In the Streamlit app (`streamlit run app.py`), add two tasks with the same date and time to see a conflict warning when you generate the schedule.

These design choices intentionally favor clarity and ease-of-use over full optimization. That makes the scheduler a good learning base for future improvements (for example, adding travel-time-aware grouping or a constraint solver).

## 📸 Demo Walkthrough

Follow these steps to generate your first PawPal+ daily schedule using the Streamlit app:

1. **Set your name**: Launch the app with `streamlit run app.py`. Enter your name in the "Owner Info" field (e.g., "Alex"). Your profile persists across app reruns via `st.session_state`.

2. **Add a pet**: In the "Add Pet" section, enter a pet name (e.g., "Biscuit"), select a species ("dog," "cat," or "other"), set an age, and click "Add pet." Your pet now appears in the "Pets" list showing name, species, age, and task count.

3. **Add tasks**: In the "Add Task" section, select your pet from the dropdown, enter a task description (e.g., "Morning walk"), choose a due date and time, set duration in minutes, pick a priority level (low/medium/high), and select frequency (none/daily/weekly). Click "Add task." The task immediately appears in the "Current Tasks by Pet" section.

4. **View your pet's tasks**: Expand the collapsible card for your pet under "Current Tasks by Pet" to see all pending tasks. Each task shows a priority indicator (🔴 high, 🟡 medium, 🟢 low) and its due date for quick reference.

5. **Generate a schedule**: Choose a date in the "Generate Schedule" section, click "Generate schedule," and PawPal+ produces a prioritized plan. Each task displays its time slot, priority emoji, description, and pet name. Click "Scheduling Rationale" to see the system's explanation for the ordering.
