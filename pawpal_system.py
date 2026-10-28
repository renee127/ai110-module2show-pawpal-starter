"""Core PawPal+ domain and scheduling logic."""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    task_id: str
    pet_id: str
    title: str
    duration: int = 0
    priority: Priority = Priority.MEDIUM
    scheduled_time: str = ""
    is_completed: bool = False
    recurrence: str = "none"

    def mark_complete(self) -> None:
        self.is_completed = True

    def update_task_details(self, duration: int, priority: Priority) -> None:
        self.duration = duration
        self.priority = priority


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: float
    special_instructions: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if not any(t.task_id == task.task_id for t in self.tasks):
            self.tasks.append(task)

    def update_profile(
        self, name: str, species: str, age: float, special_instructions: str
    ) -> None:
        self.name = name
        self.species = species
        self.age = age
        self.special_instructions = special_instructions

    def get_details(self) -> dict[str, Any]:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_instructions": self.special_instructions,
        }


class Owner:
    def __init__(self, owner_id: str, name: str, email: str, pets: list[Pet] | None = None) -> None:
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.pets = pets or []

    def add_pet(self, pet: Pet) -> None:
        if not any(p.pet_id == pet.pet_id for p in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pets(self) -> list[Pet]:
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Plan:
    def __init__(self) -> None:
        self.scheduled: list[Task] = []
        self.skipped: list[Task] = []
        self.remaining_minutes: int = 0
        self.skip_reasons: dict[str, str] = {}

def _time_to_minutes(time_value: str) -> int:
    value = time_value.strip().upper()
    if not value:
        return 24 * 60

    try:
        if " " in value:
            clock, meridiem = value.rsplit(" ", 1)
            hour, minute = (int(part) for part in clock.split(":"))
            if meridiem == "PM" and hour != 12:
                hour += 12
            elif meridiem == "AM" and hour == 12:
                hour = 0
            return hour * 60 + minute

        hour, minute = (int(part) for part in value.split(":"))
        return hour * 60 + minute
    except (TypeError, ValueError):
        return 24 * 60


class Scheduler:
    def generate_daily_plan(
        self, owner: Owner, time_limit_minutes: int
    ) -> Plan:
        plan = Plan()
        plan.remaining_minutes = time_limit_minutes

        all_tasks = owner.get_all_tasks()
        eligible_tasks = [task for task in all_tasks if not task.is_completed]

        sorted_tasks = self.sort_tasks_by_priority(eligible_tasks)

        for task in sorted_tasks:
            if task.duration <= plan.remaining_minutes:
                plan.scheduled.append(task)
                plan.remaining_minutes -= task.duration
            else:
                plan.skipped.append(task)
                plan.skip_reasons[task.task_id] = "Insufficient time budget remaining."

        return plan

    def sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        return sorted(
            tasks,
            key=lambda task: (-task.priority, _time_to_minutes(task.scheduled_time)),
        )

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        conflicts = []
        for index, first in enumerate(tasks):
            if not first.scheduled_time.strip():
                continue
            first_start = _time_to_minutes(first.scheduled_time)
            if first_start >= 24 * 60:
                continue
            first_end = first_start + first.duration

            for second in tasks[index + 1:]:
                # Only check for conflicts if tasks belong to the same pet
                if first.pet_id != second.pet_id:
                    continue
                if not second.scheduled_time.strip():
                    continue
                second_start = _time_to_minutes(second.scheduled_time)
                if second_start >= 24 * 60:
                    continue
                second_end = second_start + second.duration
                if first_start < second_end and second_start < first_end:
                    conflicts.append((first, second))

        return conflicts
