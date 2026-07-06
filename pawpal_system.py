from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, time


@dataclass
class Owner:
    owner_id: Optional[int] = None
    name: str = ""
    availability: Dict[str, List[time]] = field(default_factory=dict)
    preferences: Dict[str, object] = field(default_factory=dict)
    timezone: str = "UTC"
    contact_info: Optional[str] = None

    def update_availability(self, start: time, end: time, days: List[str]) -> None:
        pass

    def set_preferences(self, prefs: Dict[str, object]) -> None:
        pass

    def is_available(self, time_window: Dict[str, time]) -> bool:
        pass

    def to_dict(self) -> Dict:
        pass


@dataclass
class Pet:
    pet_id: Optional[int] = None
    name: str = ""
    species: str = ""
    age: Optional[int] = None
    daily_needs: List[str] = field(default_factory=list)
    notes: Optional[str] = None

    def add_need(self, task_type: str, frequency: str) -> None:
        pass

    def get_daily_requirements(self) -> List[str]:
        pass

    def age_in_years(self) -> Optional[int]:
        pass

    def to_dict(self) -> Dict:
        pass


@dataclass
class Task:
    task_id: Optional[int] = None
    title: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    recurrence: Optional[str] = None
    preferred_time_windows: List[Dict[str, time]] = field(default_factory=list)
    last_done: Optional[datetime] = None

    def is_recurring(self) -> bool:
        pass

    def next_occurrence(self, from_date: datetime) -> Optional[datetime]:
        pass

    def conflicts_with(self, other: "Task") -> bool:
        pass

    def estimate_score(self, owner: Owner, pet: Pet) -> float:
        pass

    def to_dict(self) -> Dict:
        pass


@dataclass
class Scheduler:
    owner: Owner
    pet: Pet
    tasks: List[Task] = field(default_factory=list)
    day_window: Dict[str, time] = field(default_factory=dict)
    rules: Dict[str, object] = field(default_factory=dict)
    scheduled_plan: List[Dict] = field(default_factory=list)

    def generate_plan(self, date: datetime) -> List[Dict]:
        pass

    def score_task(self, task: Task, time_slot: Dict[str, time]) -> float:
        pass

    def resolve_conflicts(self, candidate_plan: List[Dict]) -> List[Dict]:
        pass

    def explain_plan(self, plan: List[Dict]) -> str:
        pass

    def add_constraint(self, rule: Dict[str, object]) -> None:
        pass
