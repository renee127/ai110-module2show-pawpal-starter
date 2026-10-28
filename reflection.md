# PawPal+ Project Reflection

## 1. System Design

Here are three core actions a user should be able to perform in PawPal+:

---

### System Design

#### Core User Actions

1. **Add and Manage Pet Profiles**
Users can register their pets by creating individual profiles with key details such as name, species, age, and specific health or care instructions.


2. **Schedule and Prioritize Care Tasks**
Users can schedule daily pet care activities (e.g., feedings, walks, medications, or grooming sessions) and assign constraints such as duration, priority level, and recurring frequency.


3. **View Daily Agenda and Generated Plan**
Users can view an organized daily plan or dashboard of scheduled care tasks, allowing them to track completed activities and see the prioritized breakdown for each pet.

**a. Initial design**

For the initial architecture of PawPal+, I designed four core classes to separate user domain models, pet metadata, care activities, and scheduling logic:

* **`Owner`**: Represents the user profile. Its primary responsibility is managing top-level account metadata (`owner_id`, `name`, `email`) and maintaining the collection of registered pets through methods like `add_pet()`, `remove_pet()`, and `get_pets()`.
* **`Pet`**: Encapsulates individual pet profile data, storing information such as `pet_id`, `name`, `species`, `age`, and `special_instructions`. It uses `@dataclass` for clean attribute initialization and provides behavioral methods like `update_profile()` and `get_details()` to manage and export profile metadata.
* **`Task`**: Implemented as a `@dataclass`, this class represents discrete care activities (e.g., feedings, walks, medications). It holds task attributes including `task_id`, `pet_id`, `title`, `duration`, `scheduled_time`, completion status, recurrence flags, and a strongly-typed `Priority` (`IntEnum`). Its methods (`mark_complete()` and `update_task_details()`) manage task state updates.
* **`Scheduler`**: Serves as the central backend engine decoupled from domain models. It stores the aggregate pool of tasks (`tasks`) and executes core operational logic, including `add_task()`, `sort_tasks_by_priority()`, `detect_conflicts()`, and `generate_daily_plan()` to calculate daily agendas based on user time constraints.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
