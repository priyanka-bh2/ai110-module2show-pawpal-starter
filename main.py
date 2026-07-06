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
    litter_box = Task(
        description="Clean litter box",
        time=time(19, 30),
        frequency="daily",
        due_date=datetime(2026, 7, 6, 19, 30),
        priority="high",
    )

    bella.add_task(morning_walk)
    bella.add_task(dinner_feed)
    luna.add_task(litter_box)

    scheduler = Scheduler(owner=owner, pets=owner.get_pets())
    plan = scheduler.generate_plan(datetime(2026, 7, 6, 0, 0))

    print("Today's Schedule")
    print("=" * 20)
    for index, item in enumerate(plan, start=1):
        task_time = item.get("time")
        time_text = task_time.strftime("%H:%M") if task_time else "No time"
        print(f"{index}. {time_text} | {item['pet']} | {item['description']} | Priority: {item['priority']}")

    print("\nSummary")
    print("-" * 20)
    print(scheduler.explain_plan(plan))


if __name__ == "__main__":
    main()
