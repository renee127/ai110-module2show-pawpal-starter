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

- Refining System Logic: During initial code checks with the AI coding assistant, we evaluated pawpal_system.py for potential bottlenecks and missing relationships.

- Decoupling Responsibilities: Instead of having individual Pet objects manage their own scheduling logic, we centralized task scheduling and conflict checking strictly inside the Scheduler class to keep class responsibilities clear and modular.

- Dataclass Implementation: Applied Python @dataclass decorators to structural data objects like Task and Pet to streamline template initialization and reduce boilerplate code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers the total available time budget, task priority levels, and scheduled time slots. 
- I prioritized the time budget and priority levels highest; the algorithm uses a greedy approach to ensure that CRITICAL and HIGH priority tasks are scheduled first, filling the time budget before LOW priority tasks are even considered.

**b. Tradeoffs**

- The algorithm uses a greedy sorting method rather than complex dynamic programming (like the knapsack problem). The tradeoff is that while high-priority tasks are guaranteed to be considered first, it might not perfectly optimize every single remaining minute. For example, it might schedule a 15-minute HIGH priority task and leave 5 empty minutes, skipping two 10-minute LOW priority tasks that would have technically fit a 20-minute window better. 
- This is a reasonable tradeoff for a pet care app because ensuring a critical medication is given is vastly more important than mathematically optimizing every minute of the day.

---

## 3. AI Collaboration

**a. How you used AI**

- I used the AI assistant to brainstorm the initial object attributes, generate the boilerplate Mermaid.js UML diagram, and scaffold the Python class stubs. 
- The most helpful prompts were asking the AI to critique the generated skeleton for missing relationships, which highlighted the flaws in the initial flat data structure.

**b. Judgment and verification**

- When generating the initial boilerplate, the AI suggested a flat architecture where the Scheduler held a global list of all tasks. I did not accept this as final. 
- Instead, I evaluated this against OOP principles and realized this would lead to orphaned tasks if a pet was deleted. I verified the need for a change and prompted the AI to refactor the structure so that Pets owned their Tasks directly.

---

## 4. Testing and Verification

**a. What you tested**

- I tested the time string conversion logic, the nested object relationships (Owner -> Pet -> Task), the algorithmic sorting by priority, the time budget filtering, and the conflict detection logic (ensuring it accurately caught overlapping times for the same pet while ignoring simultaneous tasks for different pets).

**b. Confidence**

- I am highly confident the core scheduler works correctly because the automated pytest suite passes all boundary conditions. 
- If I had more time, I would test edge cases regarding daylight saving time boundaries and input validation for severely malformed time strings.


---

## 5. Reflection

**a. What went well**

- I am most satisfied with the architectural refactoring phase. Recognizing that a global task list was a bottleneck and shifting to a true domain-driven hierarchy (Owner containing Pets containing Tasks) made the final UI integration seamless.

**b. What you would improve**

- If I had another iteration, I would implement a full visual calendar view in the Streamlit UI (like a Gantt chart) rather than a simple text-based list, and add drag-and-drop reordering for tasks.

**c. Key takeaway**

- A key takeaway is that UML diagrams and initial AI generations are starting blueprints, not finished logic maps. It is essential to generate a baseline, look for structural bottlenecks (like disconnected data relationships), and refactor the architecture before trying to write complex algorithms or attach a frontend.
