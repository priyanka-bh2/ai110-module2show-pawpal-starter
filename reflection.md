# PawPal+ Project Reflection


## 1. System Design


**a. Initial design**


My initial UML design modeled the core entities of a pet care scheduling system. I created four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

- `Owner` stores owner information, availability, and preferences, and manages a list of `Pet` objects.
- `Pet` stores pet information and a list of `Task` objects, and provides methods to manage tasks.
- `Task` stores task details such as description, time, priority, and recurrence information, and handles completion and next occurrence logic.
- `Scheduler` reads from `Owner` and `Pet`, evaluates tasks, and generates a daily plan by sorting, filtering, and detecting conflicts.


The relationships were:
- Owner has many Pets
- Pet has many Tasks
- Scheduler depends on Owner, Pet, and Task


**b. Design changes**


Yes, the design changed during implementation. One major change was adding conflict detection logic to the `Scheduler` class. In the initial design, I only had a simple `resolve_conflicts()` method that silently removed duplicate time slots. During implementation, I realized it would be more helpful for the pet owner to see explicit warning messages instead.

I added a `detect_conflicts()` method that scans the generated schedule for tasks with the same dated time and produces readable warning strings, which are stored in `scheduled_warnings`. This made the system more transparent and user-friendly, and it also improved the UI by letting Streamlit show warnings with `st.warning()`.


---


## 2. Scheduling Logic and Tradeoffs


**a. Constraints and priorities**


My scheduler considers several constraints and priorities:


- **Time:** Tasks with a specific time are sorted chronologically, and tasks without a time are placed at the end.
- **Priority:** Tasks are scored using priority (high/medium/low) and due date urgency, which affects their ranking in the generated plan.
- **Completion status:** Only pending tasks are included in the daily plan; completed tasks are filtered out.
- **Recurring tasks:** Daily and weekly tasks automatically create the next occurrence when marked complete.
- **Preferences:** The owner’s preferences (such as preferred task types) slightly boost the score of matching tasks.


I decided which constraints mattered most by focusing on the needs of a busy pet owner: keeping the schedule readable and predictable. Chronological ordering and priority-based ranking are the most important behaviors because they make the plan easy to follow. Recurrence and filtering are simpler convenience features that reduce manual work.


**b. Tradeoffs**


The scheduler favors simple, predictable heuristics (priority + due date + small urgency boost) instead of solving a full scheduling optimization problem. This keeps the code easy to understand and maintain for beginners, and it is fast enough for a single-owner, small-pet use case.

The tradeoff is that the planner may not find a globally optimal schedule when many constraints interact (for example, minimizing total walking time across multiple pets), but it does provide sensible, explainable results and non-fatal conflict warnings. For recurring tasks, we use straightforward `timedelta` steps (daily/weekly) rather than a complex calendar library — this keeps recurrence logic transparent while covering common needs.


---


## 3. AI Collaboration


**a. How you used AI**


I used AI for several parts of the project: brainstorming the initial class design, refining method responsibilities, debugging Streamlit session state issues, and reviewing scheduling algorithms like sorting, filtering, recurrence, and conflict detection. The most helpful prompts were specific implementation questions such as:

- “How should I structure recurring task rollover with `timedelta`?”
- “How can I detect exact same-time conflicts without making the scheduler too complex?”


Separate chat sessions for different phases (design, implementation, testing, and documentation) helped me stay organized and avoid mixing up different concerns.


**b. Judgment and verification**


One moment I did not accept an AI suggestion as-is was when a more compact version of the scheduling logic was proposed. It was more Pythonic, but harder to read and explain during the review process. I compared the suggestion against my project requirements, tested the simpler version in `main.py`, and decided to keep the more readable version that matched the course’s beginner-friendly goals.


---


## 4. Testing and Verification


**a. What you tested**


I tested the following behaviors in `tests/test_pawpal.py`:


- Sorting tasks in chronological order
- Filtering incomplete tasks
- Filtering tasks for a single pet
- Completing a daily task and creating the next day’s task
- Detecting exact-time conflicts and generating warnings
- Generating a basic schedule in the expected order


These tests were important because they verified the core algorithmic behaviors that make PawPal+ a useful scheduler: ordering, filtering, recurrence, and conflict detection. Without them, bugs in the scheduler logic could have gone unnoticed and made the app unreliable.


**b. Confidence**


I am moderately confident in the scheduler because all 6 tests pass, and the core features were explicitly tested: task completion, adding tasks, sorting, recurrence, and conflict detection. The tests give me confidence that the basic behaviors are correct.

If I had more time, I would add more tests for edge cases such as:


- Tasks without times or dates
- Multiple pets with many tasks on the same day
- Overlapping durations that do not start at the exact same time
- Owners with no pets or no tasks


---


## 5. Reflection


**a. What went well**


I am most satisfied with the scheduling logic and the fact that the UI now clearly shows the smart behaviors I built. The combination of sorting, filtering, recurrence, and conflict warnings makes PawPal+ more than just a simple task list, and the conflict warnings give the user useful feedback when tasks collide.


**b. What you would improve**


If I had another iteration, I would:


- Add advanced priority-based scheduling (sorting by priority first, then by time)
- Persist data between runs by saving to a JSON file
- Improve the UI with more detailed task information and better visual formatting


I would also consider adding more comprehensive tests and experimenting with a more sophisticated optimization algorithm if performance became an issue.


**c. Key takeaway**


The most important thing I learned about designing systems with AI is that AI is a powerful partner, but the human must stay the lead architect. AI can generate code, suggest improvements, and help with debugging, but I had to decide which suggestions to accept, simplify, or reject, and verify everything with tests and careful reasoning. Working with AI taught me to think more clearly about tradeoffs, readability, and maintainability, and to treat AI suggestions as proposals rather than final answers.