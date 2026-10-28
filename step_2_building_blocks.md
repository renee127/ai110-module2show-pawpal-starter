# Step 2: List the Building Blocks

## Main System Objects

### 1. Owner
Represents the pet owner using the application.

* **Attributes (Information it holds):**
  * `owner_id` *(str / int)*: Unique identifier for the owner.
  * `name` *(str)*: Name of the pet owner.
  * `email` *(str)*: Owner's contact email.
  * `pets` *(list[Pet])*: A list containing all `Pet` objects belonging to this owner.

* **Methods (Actions it can perform):**
  * `add_pet(pet: Pet) -> None`: Adds a new pet profile to the owner's account.
  * `remove_pet(pet_id: str) -> None`: Removes a pet profile from the owner's account.
  * `get_pets() -> list[Pet]`: Returns all registered pets belonging to the owner.

---

### 2. Pet
Represents an individual pet profile.

* **Attributes (Information it holds):**
  * `pet_id` *(str / int)*: Unique identifier for the pet.
  * `name` *(str)*: Pet's name (e.g., "Biscuit").
  * `species` *(str)*: Animal species or breed (e.g., "Dog", "Golden Retriever").
  * `age` *(int / float)*: Age of the pet in years.
  * `special_instructions` *(str)*: Care notes or medical instructions (e.g., dietary restrictions, low stamina).

* **Methods (Actions it can perform):**
  * `update_profile(name, species, age, special_instructions) -> None`: Updates pet profile metadata.
  * `get_details() -> dict`: Returns a summary dictionary of the pet's profile.

---

### 3. Task
Encapsulates a specific care activity or routine (implemented as a Python `@dataclass`).

* **Attributes (Information it holds):**
  * `task_id` *(str / int)*: Unique identifier for the task.
  * `pet_id` *(str / int)*: ID of the pet assigned to this task.
  * `title` *(str)*: Description of the activity (e.g., "Morning Walk", "Feeding", "Medication").
  * `duration` *(int)*: Duration of the task in minutes.
  * `priority` *(Priority IntEnum)*: Importance level defined using an Enum (`LOW = 1`, `MEDIUM = 2`, `HIGH = 3`, `CRITICAL = 4`).
  * `scheduled_time` *(str / time)*: Preferred start time (e.g., "08:00 AM").
  * `is_completed` *(bool)*: Flag indicating whether the task is finished.
  * `is_recurring` *(bool)*: Flag indicating if the task repeats daily or weekly.

* **Methods (Actions it can perform):**
  * `mark_complete() -> None`: Sets `is_completed` to `True`.
  * `update_task_details(...) -> None`: Updates task attributes like duration or priority.

---

### 4. Scheduler
Serves as the central engine responsible for planning, sorting, and managing task workflows.

* **Attributes (Information it holds):**
  * `tasks` *(list[Task])*: Collection of all registered tasks across pets.

* **Methods (Actions it can perform):**
  * `add_task(task: Task) -> None`: Adds a new task to the scheduling pool.
  * `generate_daily_plan(owner: Owner, time_limit_minutes: int) -> dict`: Generates a prioritized daily agenda and provides explanations for any skipped tasks if time constraints are exceeded.
  * `sort_tasks_by_priority() -> list[Task]`: Sorts tasks by priority level and start time.
  * `detect_conflicts() -> list[tuple]`: Identifies overlapping time slots among scheduled tasks.