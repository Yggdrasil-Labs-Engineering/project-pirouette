# Pirouette Engineering Principles

## Purpose

This document defines the engineering principles used to guide the design, development, testing, and evolution of Project Pirouette.

Pirouette is intended to be more than a functional scheduling tool. It should be understandable, maintainable, testable, and easy to extend.

The goal is to build software that helps users complete scheduling work with confidence and minimal friction.

---

# 1. Solve a Real Problem

Pirouette exists to simplify recurring schedule creation for dance academies.

Every feature should support one or more of the following goals:

- Reduce manual scheduling effort
- Prevent scheduling conflicts
- Improve schedule visibility
- Make schedule changes easier to understand
- Provide clear and actionable feedback
- Reduce dependence on spreadsheets

Features should not be added simply because they are technically interesting.

They should improve the user experience or strengthen the scheduling workflow.

---

# 2. Make the User Successful

Pirouette should help the user succeed rather than merely reject invalid actions.

Error messages should explain:

- What went wrong
- Why it happened
- What the user can do next

For example, instead of displaying:

```text
Invalid schedule
```

Pirouette should display:

```text
Unable to schedule Tiny Tots.

Lynn is unavailable from 4:00 PM to 5:00 PM.

Studio A is already being used during that time.

Choose another teacher, studio, or start time.
```

Validation should be clear, specific, and actionable.

---

# 3. Prevent Problems Before Saving

Pirouette should validate scheduling decisions before they are written to the database.

The application should check:

- Required fields
- Duplicate records
- Teacher availability
- Teacher double-booking
- Studio double-booking
- Invalid time ranges
- References to deleted or unavailable records

The database should contain valid schedule data whenever possible.

---

# 4. One Module, One Responsibility

Each module should have a clear and focused responsibility.

## app.py

Responsible for:

- Desktop user interface
- User interaction
- Form handling
- Calendar rendering
- Application workflow

## database.py

Responsible for:

- SQLite initialization
- Database queries
- Data persistence
- Conflict lookup logic
- CRUD operations

## models.py

Responsible for:

- Domain data structures
- Shared application entities

Future modules should follow the same principle.

Examples:

### exporter.py

- Excel export
- Workbook formatting
- Schedule report generation

### validators.py

- Reusable business-rule validation

### services.py

- Scheduling workflows
- Application-level operations

Large files should be divided when responsibilities become difficult to understand or maintain.

---

# 5. Keep Business Rules Separate from Presentation

Scheduling rules should not depend on how the interface displays them.

For example:

- Teacher availability checks belong in business logic.
- Studio conflict checks belong in business logic.
- The calendar should display validated schedule data.
- The interface should present conflict messages returned by the validation layer.

This separation makes the application easier to test and safer to change.

---

# 6. Prefer Clear Code Over Clever Code

Pirouette should favor:

- Descriptive names
- Small functions
- Explicit logic
- Readable conditions
- Simple data flow
- Helpful comments where needed

Avoid:

- Unnecessary abstraction
- Deeply nested logic
- Hidden side effects
- Unexplained constants
- Clever one-line expressions

The code should be understandable by someone returning to the project months later.

---

# 7. Preserve Data Integrity

Pirouette stores operational schedule data and should protect it carefully.

The application should:

- Use foreign keys
- Prevent deletion of records that are still in use
- Confirm destructive actions
- Avoid partial writes
- Validate references before saving
- Keep the live database out of public source control

Database changes should be introduced carefully and documented.

---

# 8. Design for Extension

Pirouette begins as a dance academy scheduler, but the scheduling engine should remain adaptable.

Future extensions may include:

- Other small businesses
- Room scheduling
- Instructor scheduling
- Employee scheduling
- Recurring appointment planning
- Resource allocation

The current design should not unnecessarily hard-code assumptions that prevent future reuse.

Dance-specific behavior should remain visible and intentional.

---

# 9. Build for Desktop Simplicity

Pirouette is currently a desktop application.

The interface should be:

- Easy to understand
- Usable without technical training
- Consistent across screens
- Responsive to window resizing
- Readable on common laptop displays
- Conservative in the number of steps required

The user should not need to understand databases, programming, or system architecture.

---

# 10. Visualize Complex Information

Schedules are easier to understand visually than as raw rows of data.

Pirouette should provide:

- List views for precise details
- Weekly calendar views for quick understanding
- Filters for teachers and studios
- Color distinctions for class styles
- Full-screen or pop-out schedule views

Visualization should reduce cognitive effort, not add decoration.

---

# 11. Use Defensive Programming

Pirouette should assume that users may:

- Leave fields blank
- Select outdated values
- Attempt conflicting schedules
- Delete records in unexpected order
- Resize windows
- Click repeatedly
- Provide duplicate information

The application should handle these cases gracefully.

A user mistake should not crash the application.

---

# 12. Test Behavior, Not Just Execution

Testing should verify that Pirouette behaves correctly, not merely that it launches.

Important test areas include:

- Duplicate prevention
- Missing-field validation
- Teacher availability
- Teacher conflicts
- Studio conflicts
- Multiple simultaneous conflict messages
- Deletion rules
- Schedule persistence
- Calendar rendering
- Filter behavior
- Export accuracy

Every significant bug should become a future regression test where practical.

---

# 13. Document Important Decisions

Meaningful architectural and design decisions should be recorded using Architecture Decision Records (ADRs).

Examples include:

- Choosing Python, Tkinter, and SQLite
- Using a shared calendar renderer
- Validating all scheduling conflicts before saving
- Separating export logic into its own module

Documentation should explain both the decision and the reason behind it.

---

# 14. Release Small, Working Improvements

Pirouette should evolve through small, testable increments.

Preferred workflow:

1. Define the problem
2. Implement the smallest useful change
3. Test the behavior
4. Review the user experience
5. Document the change
6. Commit the work
7. Release when stable

Avoid large changes that are difficult to review or reverse.

---

# 15. Keep the Repository Portfolio Ready

The repository should clearly communicate the quality of the project.

It should include:

- A polished README
- Architecture documentation
- Engineering principles
- Domain model documentation
- Database schema documentation
- Testing strategy
- ADRs
- Screenshots
- Roadmap
- Release notes
- Clear commit history

A visitor should be able to understand what Pirouette does without opening the source code first.

---

# 16. Prefer Maintainability Over Speed

Rapid development matters, but maintainability matters more.

A quick solution should not create unnecessary long-term confusion.

When choosing between two approaches, prefer the one that is:

- Easier to understand
- Easier to test
- Easier to extend
- Less tightly coupled
- Safer to modify

---

# 17. Build Software That Makes Work Easier

Pirouette follows the broader Yggdrasil Labs Engineering philosophy:

> Build software that, when someone uses it, they say:
>
> **"This made my job easier."**

Every major feature should support that goal.

---

# Summary

Pirouette should remain:

- Useful
- Understandable
- Safe
- Maintainable
- Testable
- Extensible
- User-centered
- Professionally documented

These principles should guide both current development and future expansion.