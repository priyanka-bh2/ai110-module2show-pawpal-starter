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

Here's what the CLI output looks like when you run the scheduler:

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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.score_task()`, `generate_plan()` | Ranks tasks by priority (high/medium/low) and urgency |
| Filtering | `Pet.get_tasks(include_completed=False)` | Excludes completed tasks from scheduling |
| Conflict handling | `Scheduler.resolve_conflicts()` | Removes duplicate task entries and prefers higher-scored items |
| Recurring tasks | `Task.is_recurring()`, `Task.next_occurrence()` | Supports daily, weekly, and one-time task frequencies |
| Due date awareness | `Task.estimate_score()` | Boosts priority for overdue or same-day tasks |
| Owner preferences | `Owner.set_preferences()` | Allows customization of scheduling rules |

## 📸 Demo Walkthrough

Follow these steps to generate your first PawPal+ daily schedule:

1. **Set your name**: Enter your name in the "Owner Info" field (e.g., "Alex"). This personalizes your profile and persists across all visits to the app.

2. **Add a pet**: Scroll to "Add Pet," enter a pet name (e.g., "Biscuit"), select a species ("dog," "cat," or "other"), and click "Add pet." Your pet now appears in the "Pets" table showing its name, species, age, and task count.

3. **Add tasks**: In the "Add Task" section, select your pet from the dropdown, enter a task description (e.g., "Morning walk"), choose a due date and time, set a duration (in minutes), pick a priority level (low/medium/high), and select frequency (none/daily/weekly). Click "Add task." The task immediately appears in the "Current Tasks by Pet" section.

4. **View your pet's tasks**: Expand the collapsible card for your pet under "Current Tasks by Pet" to see all pending tasks. Each task shows a priority indicator (🔴 high, 🟡 medium, 🟢 low) and its due date for quick reference.

5. **Generate a schedule**: Choose a date in the "Generate Schedule" section, click "Generate schedule," and PawPal+ produces a prioritized daily plan. Each task shows its time slot, priority level, description, and the pet it belongs to. Click "Scheduling Rationale" to see why tasks were ordered that way.
