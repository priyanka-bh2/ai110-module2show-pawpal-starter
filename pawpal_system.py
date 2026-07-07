from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, time, timedelta


@dataclass
class Owner:
    owner_id: Optional[int] = None
    name: str = ""
    availability: Dict[str, List[Dict[str, time]]] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    timezone: str = "UTC"
    contact_info: Optional[str] = None
    pets: List["Pet"] = field(default_factory=list)

    def update_availability(self, start: time, end: time, days: List[str]) -> None:
        """Add an availability time slot for the given days."""
        for day in days:
            slots = self.availability.setdefault(day.lower(), [])
            slots.append({"start": start, "end": end})

    def set_preferences(self, prefs: Dict[str, Any]) -> None:
        """Update owner scheduling preferences with the provided dict."""
        self.preferences.update(prefs)

    def is_available(self, time_window: Dict[str, time]) -> bool:
        """Return True if the owner is available for the given time window."""
        start = time_window.get("start")
        end = time_window.get("end")
        if start is None or end is None:
            return False

        for slots in self.availability.values():
            for slot in slots:
                slot_start = slot.get("start")
                slot_end = slot.get("end")
                if slot_start is None or slot_end is None:
                    continue
                if slot_start <= start and end <= slot_end:
                    return True
        return False

    def add_pet(self, pet: "Pet") -> None:
        """Add a Pet to this owner if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def get_pets(self) -> List["Pet"]:
        """Return a list of this owner's pets."""
        return list(self.pets)

    def get_all_tasks(self, include_completed: bool = False) -> List["Task"]:
        """Collect and return tasks from all pets (optionally include completed)."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Owner to a dictionary for display or storage."""
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "availability": self.availability,
            "preferences": self.preferences,
            "timezone": self.timezone,
            "contact_info": self.contact_info,
            "pets": [pet.to_dict() for pet in self.pets],
        }


@dataclass
class Pet:
    pet_id: Optional[int] = None
    name: str = ""
    species: str = ""
    age: Optional[int] = None
    daily_needs: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    tasks: List["Task"] = field(default_factory=list)

    def add_need(self, task_type: str, frequency: str) -> None:
        """Register a recurring need type for this pet (e.g., feeding)."""
        if task_type not in self.daily_needs:
            self.daily_needs.append(task_type)

    def get_daily_requirements(self) -> List[str]:
        """Return the pet's daily requirement types."""
        return list(self.daily_needs)

    def age_in_years(self) -> Optional[int]:
        """Return the pet's age in years (if known)."""
        return self.age

    def add_task(self, task: "Task") -> None:
        """Add a Task to this pet if it's not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_tasks(self, include_completed: bool = True) -> List["Task"]:
        """Return this pet's tasks; optionally filter out completed tasks."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def get_pending_tasks(self) -> List["Task"]:
        """Return only tasks that are not completed."""
        return self.get_tasks(include_completed=False)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Pet to a dictionary for display or storage."""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "daily_needs": self.daily_needs,
            "notes": self.notes,
            "tasks": [task.to_dict() for task in self.tasks],
        }


@dataclass
class Task:
    task_id: Optional[int] = None
    description: str = ""
    time: Optional[time] = None
    frequency: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    priority: str = "medium"
    duration_minutes: int = 0
    recurrence: Optional[str] = None
    preferred_time_windows: List[Dict[str, time]] = field(default_factory=list)
    last_done: Optional[datetime] = None

    def mark_complete(self) -> None:
        """Mark the task completed and record the completion time."""
        self.completed = True
        self.last_done = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def toggle_complete(self) -> None:
        """Toggle the task's completed state."""
        if self.completed:
            self.mark_incomplete()
        else:
            self.mark_complete()

    def is_recurring(self) -> bool:
        """Return True when `frequency` indicates a recurring task.

        Treats values like 'daily' or 'weekly' as recurring. Values 'none',
        'once', or an empty frequency are treated as non-recurring.
        """
        if not self.frequency:
            return False
        return self.frequency.lower().strip() not in {"none", "once", "single"}

    def next_occurrence(self, from_date: datetime) -> Optional[datetime]:
        """Return the next occurrence after `from_date` for recurring tasks.

        Uses simple `timedelta` steps for common frequencies: daily (+1 day),
        weekly (+7 days), monthly (+30 days). For non-recurring tasks this
        returns the `due_date` if it is on or after `from_date`, otherwise None.
        """
        if self.due_date is None:
            return None

        if not self.is_recurring():
            return self.due_date if self.due_date >= from_date else None

        candidate = self.due_date
        frequency = self.frequency.lower().strip()

        while candidate < from_date:
            if frequency == "daily":
                candidate += timedelta(days=1)
            elif frequency == "weekly":
                candidate += timedelta(weeks=1)
            elif frequency == "monthly":
                candidate += timedelta(days=30)
            else:
                break

        return candidate if candidate >= from_date else None

    def conflicts_with(self, other: "Task") -> bool:
        """Return True when this task and `other` are scheduled at the same datetime.

        Compares `due_date` and, if provided, the `time` field. If either task
        lacks a `due_date` this returns False.
        """
        if self.due_date is None or other.due_date is None:
            return False

        self_dt = self.due_date
        other_dt = other.due_date

        if self.time is not None:
            self_dt = self.due_date.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second, microsecond=0)
        if other.time is not None:
            other_dt = other.due_date.replace(hour=other.time.hour, minute=other.time.minute, second=other.time.second, microsecond=0)

        return self_dt == other_dt

    def estimate_score(self, owner: Owner, pet: Pet) -> float:
        """Compute a simple heuristic score used to rank tasks in the plan.

        Factors include explicit priority (high/medium/low), whether the task
        is completed (large negative penalty), due date urgency (overdue or
        due within 1 day), and whether the task has a fixed time. Owner
        preferences can add a small boost for preferred task types.
        """
        priority_weights = {"high": 3.0, "medium": 2.0, "low": 1.0}
        score = priority_weights.get(self.priority.lower(), 2.0) * 10

        if self.completed:
            score -= 100

        if self.due_date is not None:
            now = datetime.now()
            if self.due_date < now:
                score -= 20
            elif self.due_date <= now + timedelta(days=1):
                score += 10

        if self.time is not None:
            score += 1

        if owner.preferences.get("preferred_task_types") and self.description.lower() in {
            item.lower() for item in owner.preferences.get("preferred_task_types", [])
        }:
            score += 5

        return score

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Task to a dictionary for display or storage."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "time": self.time.strftime("%H:%M") if self.time else None,
            "frequency": self.frequency,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "priority": self.priority,
            "duration_minutes": self.duration_minutes,
            "recurrence": self.recurrence,
            "last_done": self.last_done.isoformat() if self.last_done else None,
        }


@dataclass
class Scheduler:
    owner: Owner
    pet: Optional[Pet] = None
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    day_window: Dict[str, time] = field(default_factory=dict)
    rules: Dict[str, Any] = field(default_factory=dict)
    scheduled_plan: List[Dict[str, Any]] = field(default_factory=list)
    scheduled_warnings: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize the Scheduler pets list from provided pet or owner."""
        if self.pet is not None and self.pet not in self.pets:
            self.pets.append(self.pet)
        if not self.pets and self.owner.pets:
            self.pets = list(self.owner.pets)

    def _collect_tasks(self) -> List[Task]:
        """Gather pending tasks from scheduler pets and its own task list."""
        collected: List[Task] = []
        for pet in self.pets:
            collected.extend(pet.get_pending_tasks())
        collected.extend(task for task in self.tasks if not task.completed)
        return collected

    def filter_tasks(self, pet: Optional[Pet] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks optionally filtered by `pet` and `completed` state.

        - `pet`: when provided, only tasks belonging to that pet are returned.
        - `completed`: when True/False, include only completed or only pending tasks.
        When `completed` is None no completion filtering is applied.
        """
        results: List[Task] = []
        # search pets' tasks
        for p in self.pets:
            if pet is not None and p is not pet:
                continue
            for t in p.tasks:
                if completed is None or t.completed == completed:
                    results.append(t)

        # include scheduler-level tasks
        for t in self.tasks:
            if completed is None or t.completed == completed:
                results.append(t)

        return results

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return `tasks` sorted by clock time; untimed tasks appear last.

        This is a convenience for displaying tasks in a human-friendly order.
        """
        tasks_with_time = [t for t in tasks if t.time is not None]
        tasks_without_time = [t for t in tasks if t.time is None]
        tasks_with_time.sort(key=lambda t: (t.time.hour, t.time.minute))
        return tasks_with_time + tasks_without_time

    def find_task_by_id(self, task_id: Optional[int]) -> Optional[Task]:
        """Search for a task by `task_id` across pets and scheduler tasks."""
        if task_id is None:
            return None
        for p in self.pets:
            for t in p.tasks:
                if t.task_id == task_id:
                    return t
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        return None

    def complete_task(self, task_identifier: Any) -> Optional[Task]:
        """Mark a task complete and (for daily/weekly tasks) create the next occurrence.

        `task_identifier` may be either a `Task` instance or a `task_id` integer.
        If the task is recurring and has a `due_date`, a new `Task` instance
        for the next date is created by adding a `timedelta` (1 day or 7 days)
        and returned. If no next occurrence is created, returns `None`.
        """
        # find task object
        task_obj: Optional[Task]
        if isinstance(task_identifier, Task):
            task_obj = task_identifier
        else:
            task_obj = self.find_task_by_id(task_identifier)

        if task_obj is None:
            return None

        # mark complete
        task_obj.mark_complete()

        # auto-create next occurrence for daily/weekly recurring tasks
        if task_obj.is_recurring() and task_obj.due_date is not None and task_obj.frequency:
            freq = task_obj.frequency.lower().strip()
            if freq == "daily":
                delta = timedelta(days=1)
            elif freq == "weekly":
                delta = timedelta(weeks=1)
            else:
                delta = None

            if delta is not None:
                new_due = task_obj.due_date + delta
                new_task = Task(
                    task_id=None,
                    description=task_obj.description,
                    time=task_obj.time,
                    frequency=task_obj.frequency,
                    due_date=new_due,
                    priority=task_obj.priority,
                    duration_minutes=task_obj.duration_minutes,
                    recurrence=task_obj.recurrence,
                    preferred_time_windows=list(task_obj.preferred_time_windows),
                )

                # add to the same pet if found there, otherwise to scheduler tasks
                for p in self.pets:
                    if task_obj in p.tasks:
                        p.add_task(new_task)
                        return new_task

                # fallback to scheduler-level tasks list
                self.tasks.append(new_task)
                return new_task

        return None

    def generate_plan(self, date: datetime) -> List[Dict[str, Any]]:
        """Generate a scheduled plan for the given `date`.

        Collects pending tasks, ranks them using `score_task`, removes exact
        duplicates with `resolve_conflicts`, sorts the final plan for display,
        and refreshes `self.scheduled_warnings` (conflict messages).
        Returns a list of plan entries (dicts) containing task metadata.
        """

        pending_tasks = self._collect_tasks()
        unique_tasks: List[Task] = []
        seen: set[tuple[Any, ...]] = set()

        for task in pending_tasks:
            identity = (task.task_id, task.description, task.due_date, task.time)
            if identity in seen:
                continue
            seen.add(identity)
            unique_tasks.append(task)

        ranked_tasks = sorted(
            unique_tasks,
            key=lambda task: (
                -self.score_task(task, {}),
                task.due_date or datetime.max,
                task.priority.lower(),
                task.description.lower(),
            ),
        )

        """Generate a scheduled plan for the given date and return it as a list."""
        plan: List[Dict[str, Any]] = []
        for task in ranked_tasks:
            pet_name = next((pet.name for pet in self.pets if task in pet.tasks), self.owner.name)
            plan.append(
                {
                    "task_id": task.task_id,
                    "description": task.description,
                    "pet": pet_name,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "time": task.time,
                    "completed": task.completed,
                    "score": self.score_task(task, {}),
                    "scheduled_for": task.time or date.time(),
                }
            )

        plan = self.resolve_conflicts(plan)
        plan = sorted(
            plan,
            key=lambda item: (
                item.get("time") is None,
                item.get("time") or time(23, 59),
                item.get("due_date") or datetime.max,
                item.get("description", ""),
            ),
        )

        self.scheduled_plan = plan
        # refresh conflict warnings for the current plan
        self.scheduled_warnings = self.detect_conflicts(self.scheduled_plan)
        return self.scheduled_plan

    def score_task(self, task: Task, time_slot: Dict[str, time]) -> float:
        """Return a numeric score used for ranking tasks in `generate_plan()`.

        This delegates to `Task.estimate_score()` so the scoring rules are
        centralized on the `Task` class. `time_slot` is reserved for future use.
        """
        return task.estimate_score(self.owner, self.pets[0] if self.pets else Pet())

    def resolve_conflicts(self, candidate_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve simple conflicts by preferring higher-scored items and removing duplicates."""
        resolved: List[Dict[str, Any]] = []
        seen: set[tuple[Optional[int], Optional[time], Optional[datetime]]] = set()

        for item in sorted(candidate_plan, key=lambda entry: entry.get("score", 0), reverse=True):
            key = (item.get("task_id"), item.get("time"), item.get("due_date"))
            if key in seen:
                continue
            resolved.append(item)
            seen.add(key)

        return resolved

    def detect_conflicts(self, plan: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Detect exact datetime conflicts in the plan and return readable warnings.

        If `plan` is None, analyze `self.scheduled_plan`.
        A conflict is when two or more items have the same date+time.
        """
        if plan is None:
            plan = list(self.scheduled_plan)

        slots: Dict[Any, List[Dict[str, Any]]] = {}

        for item in plan:
            due = item.get("due_date")
            t = item.get("time")

            # skip items without a concrete datetime or time
            if due is None and t is None:
                continue

            if due is not None and isinstance(due, datetime):
                # if time provided, set hour/minute from it; otherwise use due as-is
                if t is not None:
                    try:
                        sched = due.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
                    except Exception:
                        sched = due
                else:
                    sched = due
                key = sched
            else:
                # no due date: group by time-only key
                key = ("time-only", t.hour if t else None, t.minute if t else None)

            slots.setdefault(key, []).append(item)

        warnings: List[str] = []
        for key, items in slots.items():
            if len(items) > 1:
                if isinstance(key, datetime):
                    timestr = key.strftime("%Y-%m-%d %H:%M")
                else:
                    timestr = str(key)
                names = ", ".join([f"{i.get('description')} ({i.get('pet')})" for i in items])
                warnings.append(f"Conflict at {timestr}: {names}")

        return warnings

    def explain_plan(self, plan: List[Dict[str, Any]]) -> str:
        """Return a short human-readable explanation of the scheduled plan."""
        if not plan:
            return "No tasks scheduled."

        lines = ["Planned tasks:"]
        for item in plan:
            due_date = item.get("due_date")
            due_text = due_date.strftime("%Y-%m-%d") if due_date else "No due date"
            lines.append(
                f"- {item['description']} for {item['pet']} (priority: {item['priority']}, due: {due_text})"
            )
        return "\n".join(lines)

    def add_constraint(self, rule: Dict[str, Any]) -> None:
        """Add or update a scheduling constraint rule."""
        self.rules.update(rule)
