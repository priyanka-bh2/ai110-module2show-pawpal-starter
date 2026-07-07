from datetime import datetime, time

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Alex")

    bella = Pet(name="Bella", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)

    owner.add_pet(bella)
    owner.add_pet(luna)

    morning_walk = Task(
        description="Morning walk",
        time=time(8, 0),
        frequency="daily",
        due_date=datetime(2026, 7, 6, 8, 0),
        priority="high",
    )
    dinner_feed = Task(
        description="Dinner feed",
        time=time(18, 0),
        frequency="daily",
        due_date=datetime(2026, 7, 6, 18, 0),
        priority="medium",
    )
    conflict_feed = Task(
        description="Give medication",
        time=time(18, 0),
        frequency="once",
        due_date=datetime(2026, 7, 6, 18, 0),
        priority="high",
    )
    litter_box = Task(
        description="Clean litter box",
        time=time(19, 30),
        frequency="daily",
        due_date=datetime(2026, 7, 6, 19, 30),
        priority="high",
    )

    bella.add_task(morning_walk)
    bella.add_task(dinner_feed)
    bella.add_task(conflict_feed)
    luna.add_task(litter_box)

    scheduler = Scheduler(owner=owner, pets=owner.get_pets())
    # initial plan
    plan = scheduler.generate_plan(datetime(2026, 7, 6, 0, 0))

    # Demonstrate sorting tasks by time (show pending)
    print("\nSorted pending tasks by time:")
    print("-" * 30)
    pending = scheduler.filter_tasks(completed=False)
    sorted_tasks = scheduler.sort_tasks_by_time(pending)
    for i, t in enumerate(sorted_tasks, start=1):
        ttime = t.time.strftime("%H:%M") if t.time else "No time"
        print(f"{i}. {ttime} | {t.description} | Pet: {next((p.name for p in owner.pets if t in p.tasks), 'N/A')}")

    # Demonstrate filtering: tasks for Bella only and incomplete
    print("\nBella's pending tasks:")
    print("-" * 30)
    bellas_pending = scheduler.filter_tasks(pet=bella, completed=False)
    for t in bellas_pending:
        print(f"- {t.description} at {t.time.strftime('%H:%M') if t.time else 'No time'}")

    # Demonstrate completing a recurring task and auto-creating the next occurrence
    print("\nCompleting the morning walk (recurring) and creating next occurrence...")
    new_task = scheduler.complete_task(morning_walk)
    if new_task:
        print("Next occurrence created:", new_task.description, "due:", new_task.due_date)
    else:
        print("No next occurrence created.")

    # regenerate plan and show conflict warnings
    plan = scheduler.generate_plan(datetime(2026, 7, 6, 0, 0))

    print("Today's Schedule")
    print("=" * 20)
    for index, item in enumerate(plan, start=1):
        task_time = item.get("time")
        time_text = task_time.strftime("%H:%M") if task_time else "No time"
        print(f"{index}. {time_text} | {item['pet']} | {item['description']} | Priority: {item['priority']}")

    # Print any conflict warnings (non-fatal)
    if scheduler.scheduled_warnings:
        print("\nWarnings:")
        for w in scheduler.scheduled_warnings:
            print("-", w)

    print("\nSummary")
    print("-" * 20)
    print(scheduler.explain_plan(plan))


if __name__ == "__main__":
    main()
