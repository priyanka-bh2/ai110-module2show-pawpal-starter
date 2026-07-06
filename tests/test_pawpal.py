from datetime import time

from pawpal_system import Task, Pet


def test_mark_complete_changes_task_status():
    task = Task(description="Test task")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Fido")
    initial_count = len(pet.get_tasks())
    new_task = Task(description="Feed", time=time(9, 0))
    pet.add_task(new_task)
    assert len(pet.get_tasks()) == initial_count + 1
    assert new_task in pet.get_tasks()
