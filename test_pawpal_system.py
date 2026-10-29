"""Automated unit test suite for PawPal+ core domain and scheduling logic."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def create_owner_with_task(task: Task) -> Owner:
    pet = Pet("pet-1", "Rocky", "dog", 3.0)
    pet.add_task(task)
    return Owner("owner-1", "Tyler", "tyler@example.com", [pet])


def test_owner_manages_pets():
    owner = Owner("owner-1", "Tyler", "tyler@example.com")
    pet = Pet("pet-1", "Rocky", "dog", 3.0)

    owner.add_pet(pet)

    assert owner.get_pets() == [pet]
    owner.remove_pet("pet-1")
    assert owner.get_pets() == []


def test_pet_profile_and_task_helpers():
    pet = Pet("pet-1", "Rocky", "dog", 3.0)
    task = Task("task-1", "pet-1", "Morning walk")

    pet.add_task(task)
    pet.update_profile("Rocky", "Golden Retriever", 4.0, "Take water")

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


# --- ADVANCED SCHEDULING & ALGORITHMIC FEATURE TESTS ---

def test_find_next_available_slot_identifies_middle_gap():
    """Verifies that find_next_available_slot locates an open window between two scheduled tasks."""
    t1 = Task("t1", "p1", "Morning Feed", duration=30, priority=Priority.HIGH, scheduled_time="08:00 AM")
    t2 = Task("t2", "p1", "Playtime", duration=30, priority=Priority.MEDIUM, scheduled_time="09:00 AM")
    scheduler = Scheduler()

    slot = scheduler.find_next_available_slot(
        [t1, t2], pet_id="p1", desired_start="08:00 AM", duration=20
    )
    assert slot == "08:30 AM"


def test_find_next_available_slot_returns_none_when_no_gap_fits():
    """Verifies boundary handling when schedule is full and no valid slot exists."""
    t1 = Task("t1", "p1", "All Day Activity", duration=720, priority=Priority.HIGH, scheduled_time="08:00 AM")
    scheduler = Scheduler()

    slot = scheduler.find_next_available_slot(
        [t1], pet_id="p1", desired_start="08:00 AM", duration=60
    )
    assert slot is None


def test_conflict_detection_isolates_by_pet():
    """Ensures overlapping task times for DIFFERENT pets do NOT trigger a false positive conflict."""
    p1_task = Task("t1", "p1", "Walk Dog", duration=30, priority=Priority.HIGH, scheduled_time="08:00 AM")
    p2_task = Task("t2", "p2", "Feed Cat", duration=30, priority=Priority.HIGH, scheduled_time="08:00 AM")
    scheduler = Scheduler()

    conflicts = scheduler.detect_conflicts([p1_task, p2_task])
    assert conflicts == []


def test_complex_scheduling_priority_and_time_tiebreak():
    """Verifies primary sorting by priority level and secondary sorting by chronological time."""
    t1 = Task("t1", "p1", "Late High Priority", duration=15, priority=Priority.HIGH, scheduled_time="10:00 AM")
    t2 = Task("t2", "p1", "Early High Priority", duration=15, priority=Priority.HIGH, scheduled_time="08:00 AM")
    t3 = Task("t3", "p1", "Critical Task", duration=15, priority=Priority.CRITICAL, scheduled_time="09:00 AM")
    scheduler = Scheduler()

    sorted_tasks = scheduler.sort_tasks_by_priority([t1, t2, t3])
    assert [t.task_id for t in sorted_tasks] == ["t3", "t2", "t1"]