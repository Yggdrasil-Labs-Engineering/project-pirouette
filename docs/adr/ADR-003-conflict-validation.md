# ADR-003: Validate All Scheduling Conflicts Before Saving

## Status

Accepted

## Date

2026-08-03

## Context

Project Pirouette allows users to create recurring weekly schedules for dance classes.

Each schedule entry combines:

- Teacher
- Dance Class
- Studio
- Day
- Start Time
- End Time

Before a schedule entry is committed to the database, the application must ensure that it does not violate any scheduling rules.

A common implementation strategy is to stop validation when the first error is encountered.

For example:

```text
Teacher unavailable.
```

The user corrects the issue, attempts to save again, and then receives:

```text
Studio conflict.
```

After correcting that issue, another attempt may reveal:

```text
Missing required field.
```

This repeated trial-and-error workflow is frustrating and inefficient.

---

# Decision

Pirouette will perform complete validation before saving a schedule entry.

Rather than stopping after the first validation failure, the application will evaluate all applicable business rules and present every detected conflict to the user in a single operation.

The schedule will only be committed if every validation check succeeds.

---

# Validation Scope

The current validation process evaluates:

- Required fields
- Teacher existence
- Studio existence
- Class existence
- Valid time ranges
- Teacher availability
- Teacher scheduling conflicts
- Studio scheduling conflicts
- Duplicate schedule entries

Additional validation rules may be added in future releases.

---

# Example

Instead of displaying:

```text
Teacher unavailable.
```

Pirouette should display something similar to:

```text
Unable to schedule Tiny Tots.

Validation Results

• Lynn is unavailable between 4:00 PM and 5:00 PM.

• Studio A is already scheduled during this time.

• End time must occur after the start time.

Please correct the issues above and try again.
```

The objective is to help the user resolve every known problem in a single pass.

---

# Rationale

Users think in terms of scheduling.

They should not be required to repeatedly submit the same schedule simply to discover the next validation error.

Complete validation:

- reduces frustration
- reduces repeated work
- improves usability
- increases confidence
- supports faster schedule creation

The application should guide the user toward a valid schedule rather than forcing repeated trial-and-error.

---

# Alternatives Considered

## Fail Fast

The simplest approach is:

```text
Check Rule

If Failed

Stop
```

Advantages:

- Simple implementation
- Minimal processing

Disadvantages:

- Poor user experience
- Multiple correction cycles
- Increased frustration
- Additional save attempts

This option was rejected.

---

## Partial Validation

Another option was to perform only basic validation before saving.

Examples:

- Required fields
- Time validation

and defer scheduling conflicts until later.

Advantages:

- Simpler implementation

Disadvantages:

- Invalid schedules could still enter the database.
- Additional correction steps would be required later.
- Schedule integrity would be reduced.

This option was rejected.

---

# Validation Workflow

Pirouette performs validation in the following order:

```text
Required Fields
        │
        ▼
Entity Validation
        │
        ▼
Time Validation
        │
        ▼
Teacher Availability
        │
        ▼
Teacher Conflict
        │
        ▼
Studio Conflict
        │
        ▼
Duplicate Detection
        │
        ▼
Any Errors?
      │
 ┌────┴────┐
 │         │
Yes        No
 │         │
 ▼         ▼
Display    Save
Results    Schedule
```

Only schedules that successfully pass every validation stage are written to the database.

---

# User Experience Principles

Validation messages should:

- be specific
- identify the conflicting resource
- explain why the conflict exists
- suggest corrective action
- avoid technical terminology

Messages should help users solve the problem rather than simply reporting it.

---

# Benefits

Complete validation provides:

- Better usability
- Fewer repeated save attempts
- Higher schedule quality
- Better data integrity
- Greater user confidence
- Reduced scheduling errors

---

# Consequences

## Positive

- Improved user experience
- Better business-rule enforcement
- Cleaner database
- Fewer invalid schedules
- Easier troubleshooting

## Negative

- Validation logic becomes more comprehensive.
- Additional validation checks increase implementation complexity.
- Error reporting requires structured message generation.

These tradeoffs are considered acceptable because schedule correctness is more important than minimizing validation code.

---

# Future Enhancements

Future validation may include:

- Student enrollment conflicts
- Studio capacity validation
- Instructor certification requirements
- Holiday scheduling
- Performance conflicts
- Age-group compatibility
- Schedule exception handling
- Seasonal scheduling constraints

The validation framework should remain extensible.

---

# Decision Outcome

Project Pirouette will validate all applicable scheduling rules before saving any schedule entry.

The application will present all detected conflicts together, allowing users to resolve multiple issues in a single editing cycle.

This approach prioritizes usability, schedule accuracy, and data integrity while reinforcing Pirouette's philosophy of helping users build correct schedules with confidence.