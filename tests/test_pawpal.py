from datetime import datetime, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_sorting_tasks_by_time_returns_chronological_order():
    task_morning = Task(description="Morning walk", time=time(9, 0))
    task_noon = Task(description="Lunch check", time=time(12, 0))
    task_evening = Task(description="Evening play", time=time(18, 30))
    scheduler = Scheduler(owner=Owner(name="Taylor"))

    sorted_tasks = scheduler.sort_tasks_by_time([task_evening, task_morning, task_noon])

    assert sorted_tasks == [task_morning, task_noon, task_evening]


def test_filtering_incomplete_tasks_returns_only_pending_items():
    pet = Pet(name="Fido")
    task_done = Task(description="Groom", completed=True)
    task_pending = Task(description="Feed", completed=False)
    pet.add_task(task_done)
    pet.add_task(task_pending)
    scheduler = Scheduler(owner=Owner(name="Casey"), pets=[pet])

    incomplete_tasks = scheduler.filter_tasks(completed=False)

    assert task_pending in incomplete_tasks
    assert task_done not in incomplete_tasks
    assert all(task.completed is False for task in incomplete_tasks)


def test_filtering_tasks_for_one_pet_only():
    pet_one = Pet(name="Buddy")
    pet_two = Pet(name="Milo")
    task_one = Task(description="Water plants")
    task_two = Task(description="Check ears")
    pet_one.add_task(task_one)
    pet_two.add_task(task_two)

    owner = Owner(name="Jordan")
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)
    scheduler = Scheduler(owner=owner)

    buddy_tasks = scheduler.filter_tasks(pet=pet_one)

    assert task_one in buddy_tasks
    assert task_two not in buddy_tasks


def test_completing_daily_task_creates_next_day_task():
    due_today = datetime(2026, 7, 6, 8, 0)
    pet = Pet(name="Milo")
    daily_task = Task(
        description="Brush fur",
        time=time(8, 0),
        due_date=due_today,
        frequency="daily",
    )
    pet.add_task(daily_task)
    scheduler = Scheduler(owner=Owner(name="Avery"), pets=[pet])

    next_task = scheduler.complete_task(daily_task)

    assert daily_task.completed is True
    assert next_task is not None
    assert next_task is not daily_task
    assert next_task.due_date == due_today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task in pet.get_tasks()


def test_conflict_detection_flags_duplicate_exact_times():
    owner = Owner(name="Dana")
    pet = Pet(name="Buddy")
    shared_due = datetime(2026, 7, 6, 9, 0)
    first_task = Task(
        task_id=1,
        description="Feed breakfast",
        time=time(9, 0),
        due_date=shared_due,
    )
    second_task = Task(
        task_id=2,
        description="Give medicine",
        time=time(9, 0),
        due_date=shared_due,
    )
    pet.add_task(first_task)
    pet.add_task(second_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    scheduler.generate_plan(datetime(2026, 7, 6))

    assert any("Conflict at" in warning for warning in scheduler.scheduled_warnings)
    assert "Feed breakfast" in scheduler.scheduled_warnings[0]
    assert "Give medicine" in scheduler.scheduled_warnings[0]


def test_generate_plan_returns_ordered_tasks():
    owner = Owner(name="Lee")
    pet = Pet(name="Zoe")
    early_task = Task(
        task_id=10,
        description="Feed",
        time=time(9, 0),
        due_date=datetime(2026, 7, 6, 9, 0),
        priority="medium",
    )
    late_task = Task(
        task_id=11,
        description="Walk",
        time=time(15, 0),
        due_date=datetime(2026, 7, 6, 15, 0),
        priority="medium",
    )
    pet.add_task(early_task)
    pet.add_task(late_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    plan = scheduler.generate_plan(datetime(2026, 7, 6))

    assert len(plan) >= 2
    assert plan[0]["description"] == "Feed"
    assert plan[1]["description"] == "Walk"
