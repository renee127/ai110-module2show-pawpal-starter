"""PawPal+ CLI Demo Script."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def main() -> None:
    print("=" * 65)
    print(" 🐾 PawPal+ Smart Pet Care Management System — CLI Demo")
    print("=" * 65)

    # 1. Instantiate Owner
    owner = Owner(owner_id="o1", name="Tyler", email="tyler@example.com")
    print(f"\n👤 Owner Created: {owner.name} ({owner.email})")

    # 2. Instantiate 2 Pets
    pet1 = Pet(
        pet_id="p1",
        name="Rocky",
        species="Dog",
        age=3.0,
        special_instructions="Daily meds required",
    )
    pet2 = Pet(
        pet_id="p2",
        name="Kitkat",
        species="Cat",
        age=2.0,
        special_instructions="Needs slow feeder",
    )

    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"🐾 Pets Added: {pet1.name} ({pet1.species}), {pet2.name} ({pet2.species})")

    # 3. Create 4 Tasks across both pets
    task1 = Task(
        "t1",
        pet1.pet_id,
        "Morning Medication",
        duration=10,
        priority=Priority.CRITICAL,
        scheduled_time="08:00 AM",
    )
    task2 = Task(
        "t2",
        pet1.pet_id,
        "Morning Walk",
        duration=30,
        priority=Priority.HIGH,
        scheduled_time="08:00 AM",
    )
    task3 = Task(
        "t3",
        pet2.pet_id,
        "Breakfast Feeding",
        duration=15,
        priority=Priority.HIGH,
        scheduled_time="08:30 AM",
    )
    task4 = Task(
        "t4",
        pet1.pet_id,
        "Grooming Session",
        duration=45,
        priority=Priority.LOW,
        scheduled_time="02:00 PM",
    )

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task4)
    pet2.add_task(task3)

    print(f"📋 Care Tasks Created: {len(owner.get_all_tasks())} total tasks across all pets.")

    # 4. Demonstrate Algorithmic Feature 1: Conflict Detection
    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()
    conflicts = scheduler.detect_conflicts(all_tasks)

    print("\n" + "-" * 65)
    print("🔍 Algorithmic Feature 1: Conflict Detection")
    print("-" * 65)
    if conflicts:
        for t1, t2 in conflicts:
            pet_name = next(p.name for p in owner.get_pets() if p.pet_id == t1.pet_id)
            print(
                f"⚠️ CONFLICT for {pet_name}: '{t1.title}' ({t1.scheduled_time}) overlaps with '{t2.title}' ({t2.scheduled_time})"
            )
    else:
        print("No time conflicts detected.")

    # 5. Demonstrate Algorithmic Feature 3: Next Available Slot
    next_slot = scheduler.find_next_available_slot(
        all_tasks,
        pet_id=pet1.pet_id,
        desired_start="08:00 AM",
        duration=20,
    )
    print("\n" + "-" * 65)
    print("🕒 Advanced Scheduling: Next Available Slot")
    print("-" * 65)
    print(f"   • Next conflict-free 20-minute slot for {pet1.name}: {next_slot}")

    # 6. Demonstrate Algorithmic Feature 2: Daily Plan Generation with Time Budgeting
    time_budget = 45
    print("\n" + "-" * 65)
    print(f"📅 Algorithmic Feature 2: Daily Plan Generation (Budget: {time_budget} mins)")
    print("-" * 65)

    plan = scheduler.generate_daily_plan(owner, time_limit_minutes=time_budget)

    print(
        f"\n✅ Scheduled Tasks ({time_budget - plan.remaining_minutes} mins used / {plan.remaining_minutes} mins remaining):"
    )
    for task in plan.scheduled:
        pet_name = next(p.name for p in owner.get_pets() if p.pet_id == task.pet_id)

        print(
            f"   • [{task.scheduled_time}] {task.title} for {pet_name} ({task.duration} mins) [Priority: {task.priority.name}]"
        )

    print(f"\n⏭️ Skipped Tasks ({len(plan.skipped)}):")
    for task in plan.skipped:
        reason = plan.skip_reasons.get(task.task_id, "Skipped")
        print(f"   • {task.title} ({task.duration} mins) — Reason: {reason}")

    print("\n" + "=" * 65)
    print(" Demo complete! All core classes & algorithms executed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()
