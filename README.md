# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ CLI Output

Running `python3 main.py` demonstrates priority-based budgeting, overlap detection, and the next available-slot algorithm:

```text
=================================================================
 🐾 PawPal+ Smart Pet Care Management System — CLI Demo
=================================================================

👤 Owner Created: Tyler (tyler@example.com)
🐾 Pets Added: Rocky (Dog), Kitkat (Cat)
📋 Care Tasks Created: 4 total tasks across all pets.

-----------------------------------------------------------------
🔍 Algorithmic Feature 1: Conflict Detection
-----------------------------------------------------------------
⚠️ CONFLICT for Rocky: 'Morning Medication' (08:00 AM) overlaps with 'Morning Walk' (08:00 AM)

-----------------------------------------------------------------
🕒 Advanced Scheduling: Next Available Slot
-----------------------------------------------------------------
   • Next conflict-free 20-minute slot for Rocky: 8:30 AM

-----------------------------------------------------------------
📅 Algorithmic Feature 2: Daily Plan Generation (Budget: 45 mins)
-----------------------------------------------------------------

✅ Scheduled Tasks (40 mins used / 5 mins remaining):
   • [08:00 AM] Morning Medication for Rocky (10 mins) [Priority: CRITICAL]
   • [08:00 AM] Morning Walk for Rocky (30 mins) [Priority: HIGH]

⏭️ Skipped Tasks (2):
   • Breakfast Feeding (15 mins) — Reason: Insufficient time budget remaining.
   • Grooming Session (45 mins) — Reason: Insufficient time budget remaining.

=================================================================
 Demo complete! All core classes & algorithms executed successfully.
=================================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest test_pawpal_system.py

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0
rootdir: /Users/temp/Desktop/gits/ai110-module2show-pawpal-starter
collected 11 items

test_pawpal_system.py ...........                                        [100%]

============================== 11 passed in 0.02s ==============================

```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

```markdown
## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
| :--- | :--- | :--- |
| **Task Sorting** | `Scheduler.sort_tasks_by_priority()` | Primary sorting by numerical `Priority` (`CRITICAL` > `LOW`) and secondary chronological sorting. |
| **Time Budgeting** | `Scheduler.generate_daily_plan()` | Greedy allocation fitting tasks into available daily minute limit with explicit skip reasons. |
| **Conflict Detection** | `Scheduler.detect_conflicts()` | Checks interval overlaps ($max(start_1, start_2) < min(end_1, end_2)$) between tasks assigned to the same pet. |
| **Gap Finder** | `Scheduler.find_next_available_slot()` | Scans existing pet schedules and locates the earliest non-overlapping open time slot. |
```

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Owner Profile & Pet Setup: Launch the app (streamlit run app.py) and navigate to the Profile & Pets tab. View the default owner profile ("Jordan") and register a second pet (e.g., "Kitkat", Cat, age 2) using the Add a New Pet form.Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
