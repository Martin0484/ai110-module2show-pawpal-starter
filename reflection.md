# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I choose a pet class, which stores age and name of the pet, an owner class, which stores
the name of the owner, a task class, which stores the duration of a task, and a medication
class, which stores the frequency of medications.

**b. Design changes**

- Did your design change during implementation?

No
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler considers time conflicts between different tasks.
- How did you decide which constraints mattered most?
I decided that based on what would affect the user experience the most.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler may not have the fastest performance.
- Why is that tradeoff reasonable for this scenario?
It allows the scheduler to have more code that is easily readable.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used Copilot to brainstorm solutions to problems in the code.
- What kinds of prompts or questions were most helpful?
Asking how a specific action could be implemented.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I did not accept an AI suggestion when I saw it be unnecessarily complex.
- How did you evaluate or verify what the AI suggested?
I ran the program after making changes that the AI suggested.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the time filters and the method for time conflicts.
- Why were these tests important?
Because they ensure that important features of the program are working as intended.

**b. Confidence**

- How confident are you that your scheduler works correctly?
3
- What edge cases would you test next if you had more time?
I would test an edge case where there is no data and one where a
dog name is very long.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the layout of the UI

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the code by adding more methods

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that AI can be very useful for creating solutions.