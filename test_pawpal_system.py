from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def create_owner_with_task(task: Task) -> Owner:
    pet = Pet("pet-1", "Mochi", "dog", 3.0)
    pet.add_task(task)
    return Owner("owner-1", "Jordan", "jordan@example.com", [pet])


def test_owner_manages_pets():
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3.0)

    owner.add_pet(pet)

    assert owner.get_pets() == [pet]
    owner.remove_pet("pet-1")
    assert owner.get_pets() == []


def test_pet_profile_and_task_helpers():
    pet = Pet("pet-1", "Mochi", "dog", 3.0)
    task = Task("task-1", "pet-1", "Morning walk")

    pet.add_task(task)
    pet.update_profile("Mochi", "Golden Retriever", 4.0, "Take water")

    assert pet.tasks == [task]
    assert pet.get_details()["age"] == 4.0
    assert pet.special_instructions == "Take water"


def test_task_methods_update_completion_and_details():
    task = Task("task-1", "pet-1", "Medication", 15)

    task.mark_complete()
    task.update_task_details(20, Priority.CRITICAL)

    assert task.is_completed is True
    assert task.duration == 20
    assert task.priority == Priority.CRITICAL


def test_scheduler_sorts_tasks_by_priority_then_time():
    later_high = Task("task-1", "pet-1", "Walk", 20, Priority.HIGH, "09:00 AM")
    earlier_high = Task("task-2", "pet-1", "Feed", 10, Priority.HIGH, "08:00 AM")
    medium = Task("task-3", "pet-1", "Brush", 10, Priority.MEDIUM, "07:00 AM")

    sorted_tasks = Scheduler().sort_tasks_by_priority([later_high, medium, earlier_high])

    assert [task.task_id for task in sorted_tasks] == ["task-2", "task-1", "task-3"]


def test_daily_plan_schedules_tasks_and_records_skipped_tasks():
    first = Task("task-1", "pet-1", "Medication", 10, Priority.CRITICAL, "08:00 AM")
    second = Task("task-2", "pet-1", "Walk", 20, Priority.HIGH, "09:00 AM")
    owner = create_owner_with_task(first)
    owner.get_pets()[0].add_task(second)

    plan = Scheduler().generate_daily_plan(owner, 25)

    assert plan.scheduled == [first]
    assert plan.skipped == [second]
    assert plan.remaining_minutes == 15


def test_daily_plan_skips_task_when_time_runs_out():
    task = Task("task-1", "pet-1", "Walk", 30, Priority.HIGH, "08:00 AM")
    owner = create_owner_with_task(task)

    plan = Scheduler().generate_daily_plan(owner, 20)

    assert plan.scheduled == []
    assert plan.skipped == [task]
    assert plan.skip_reasons[task.task_id] == "Insufficient time budget remaining."


def test_scheduler_detects_overlapping_tasks_for_same_pet():
    first = Task("task-1", "pet-1", "Walk", 30, Priority.HIGH, "08:00 AM")
    second = Task("task-2", "pet-1", "Medication", 15, Priority.CRITICAL, "08:15 AM")
    separate_pet = Task("task-3", "pet-2", "Feed", 15, Priority.HIGH, "08:15 AM")

    conflicts = Scheduler().detect_conflicts([first, second, separate_pet])

    assert conflicts == [(first, second)]
