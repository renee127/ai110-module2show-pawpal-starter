"""Core PawPal+ domain and scheduling logic."""

from dataclasses import dataclass
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Owner:
    def __init__(self, owner_id: str, name: str, email: str, pets: list["Pet"] | None = None) -> None:
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.pets = pets or []

    def add_pet(self, pet: "Pet") -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pets(self) -> list["Pet"]:
        return self.pets


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: float
    special_instructions: str = ""

    def update_profile(
        self, name: str, species: str, age: float, special_instructions: str
    ) -> None:
        self.name = name
        self.species = species
        self.age = age
        self.special_instructions = special_instructions

    def get_details(self) -> dict:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_instructions": self.special_instructions,
        }


@dataclass
class Task:
    task_id: str
    pet_id: str
    title: str
    duration: int = 0
    priority: Priority = Priority.MEDIUM
    scheduled_time: str = ""
    is_completed: bool = False
    is_recurring: bool = False

    def mark_complete(self) -> None:
        self.is_completed = True

    def update_task_details(self, duration: int, priority: Priority) -> None:
        self.duration = duration
        self.priority = priority


class Scheduler:
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self.tasks = tasks or []

    def add_task(self, task: Task) -> None:
        if task not in self.tasks:
            self.tasks.append(task)

    def generate_daily_plan(
        self, owner: Owner, time_limit_minutes: int
    ) -> dict:
        owned_pet_ids = {pet.pet_id for pet in owner.get_pets()}
        eligible_tasks = [
            task for task in self.tasks
            if task.pet_id in owned_pet_ids and not task.is_completed
        ]
        sorted_tasks = sorted(
            eligible_tasks,
            key=lambda task: (-task.priority, _time_to_minutes(task.scheduled_time)),
        )

        scheduled = []
        skipped = []
        remaining_minutes = time_limit_minutes
        for task in sorted_tasks:
            if task.duration <= remaining_minutes:
                scheduled.append(task)
                remaining_minutes -= task.duration
            else:
                skipped.append(task)

        return {
            "scheduled_tasks": scheduled,
            "skipped_tasks": skipped,
            "remaining_minutes": remaining_minutes,
            "scheduled": scheduled,
            "skipped": skipped,
        }

    def sort_tasks_by_priority(self) -> list[Task]:
        return sorted(
            self.tasks,
            key=lambda task: (-task.priority, _time_to_minutes(task.scheduled_time)),
        )

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        conflicts = []
        for index, first in enumerate(self.tasks):
            if not first.scheduled_time:
                continue
            first_start = _time_to_minutes(first.scheduled_time)
            first_end = first_start + first.duration
            for second in self.tasks[index + 1:]:
                if not second.scheduled_time:
                    continue
                second_start = _time_to_minutes(second.scheduled_time)
                second_end = second_start + second.duration
                if first_start < 24 * 60 and second_start < 24 * 60:
                    if first_start < second_end and second_start < first_end:
                        conflicts.append((first, second))
        return conflicts


def _time_to_minutes(time_value: str) -> int:
    """Convert common 12-hour or 24-hour time strings to minutes after midnight."""
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
