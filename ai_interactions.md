# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Implement Challenge 1 by adding a third algorithmic capability that finds the next available non-overlapping time slot for a pet. Also integrate the capability into the Streamlit UI, add unit tests, and document the workflow.

**What did the agent do?**

The agent modified:

- `pawpal_system.py`: added `Scheduler.find_next_available_slot()`, 12-hour time formatting, and stricter scheduled-time validation.
- `test_pawpal_system.py`: added tests for free slots, overlapping tasks, tasks belonging to other pets, and slots that extend beyond the end of the day.
- `app.py`: added controls that select a pet, desired start time, and duration, then display the next available slot.
- `ai_interactions.md`: documented this agent workflow and verification steps.

**What did you have to verify or fix manually?**

- Reviewed the algorithm to ensure completed tasks and tasks assigned to other pets are ignored.
- Verified that an occupied interval moves the proposed start to the interval's end and that the result remains before 10:00 PM.
- Reviewed invalid-time handling and ran the focused unit tests and Python compilation checks.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
