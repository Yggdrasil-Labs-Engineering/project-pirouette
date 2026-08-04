# Project Pirouette Domain Model

## Purpose

This document defines the core business entities that make up Project Pirouette.

The domain model describes **what the application manages**, independent of user interface design, database implementation, or programming language.

These entities form the common language used throughout the project.

---

# Domain Overview

Project Pirouette models the scheduling operations of a dance academy.

The application revolves around five primary business entities:

```text
Teacher
     │
     ├────────────┐
     │            │
Availability   Dance Class
     │            │
     └──────┐     │
            ▼     ▼
         Schedule Entry
               ▲
               │
            Studio
```

Each entity has a clearly defined responsibility.

---

# Teacher

## Description

A teacher represents an instructor who teaches one or more dance classes.

Teachers are central to scheduling.

A teacher may:

- teach multiple classes
- teach different dance styles
- have recurring weekly availability
- appear multiple times within a weekly schedule

---

## Responsibilities

- Provide instruction
- Maintain weekly availability
- Be assigned to classes
- Prevent scheduling conflicts

---

## Attributes

- Teacher ID
- Name

Future attributes may include:

- Email
- Phone Number
- Certifications
- Biography
- Employment Status

---

# Studio

## Description

A studio represents a physical room where dance instruction occurs.

Studios are limited resources.

Only one class may occupy a studio during a given time period.

---

## Responsibilities

- Host scheduled classes
- Prevent room conflicts

---

## Attributes

- Studio ID
- Studio Name

Future attributes may include:

- Capacity
- Floor Type
- Mirrors
- Equipment
- Location

---

# Availability

## Description

Availability defines when a teacher is able to teach.

Availability is recurring and applies to each week.

---

## Responsibilities

- Define teaching hours
- Restrict scheduling
- Support conflict validation

---

## Attributes

- Teacher
- Day of Week
- Start Time
- End Time

---

## Business Rules

Availability should:

- have a valid start time
- have a valid end time
- not overlap itself
- belong to a teacher

---

# Dance Class

## Description

A dance class represents a recurring instructional offering.

Examples include:

- Ballet I
- Tiny Tots
- Competitive Acro
- Hip Hop
- Pointe

A dance class is independent from the schedule.

The schedule determines when and where the class occurs.

---

## Responsibilities

- Identify a class offering
- Associate with a teacher
- Define dance style
- Define duration

---

## Attributes

- Class ID
- Class Name
- Dance Style
- Preferred Teacher
- Duration

Future attributes may include:

- Age Group
- Skill Level
- Enrollment Limit
- Tuition Category

---

# Schedule Entry

## Description

A schedule entry represents one scheduled occurrence of a dance class.

This entity combines:

- Dance Class
- Teacher
- Studio
- Day
- Start Time
- End Time

It is the central entity within Pirouette.

---

## Responsibilities

- Place classes on the calendar
- Prevent conflicts
- Support visualization
- Support reporting

---

## Attributes

- Schedule ID
- Dance Class
- Teacher
- Studio
- Day
- Start Time
- End Time

---

# Relationships

## Teacher → Availability

One teacher may have many availability records.

```text
Teacher
    │
    ├──── Availability
    ├──── Availability
    └──── Availability
```

---

## Teacher → Dance Class

One teacher may teach many classes.

```text
Teacher
    │
    ├──── Ballet
    ├──── Tap
    └──── Jazz
```

---

## Dance Class → Schedule Entry

One class may appear multiple times.

```text
Dance Class
     │
     ├──── Monday
     ├──── Wednesday
     └──── Friday
```

---

## Studio → Schedule Entry

A studio hosts many scheduled classes.

Only one schedule entry may occupy a studio at a specific time.

---

# Business Rules

Pirouette currently enforces:

## Teacher Availability

Classes may only be scheduled during available hours.

---

## Teacher Conflict

Teachers cannot teach two classes simultaneously.

---

## Studio Conflict

Studios cannot host multiple classes simultaneously.

---

## Required Information

Schedule entries require:

- Teacher
- Class
- Studio
- Day
- Start Time
- End Time

---

# Future Domain Expansion

Future versions may introduce:

## Student

Represents enrolled dancers.

---

## Enrollment

Links students to classes.

---

## Season

Represents yearly scheduling periods.

---

## Performance

Represents recitals and performances.

---

## Costume

Tracks costume assignments.

---

## Tuition

Tracks billing and payments.

---

## Attendance

Tracks weekly attendance.

---

## Waiting List

Tracks students awaiting placement.

---

# Domain Principles

The domain model should remain independent from:

- Tkinter
- SQLite
- Python implementation
- Screen layouts

The domain represents the business itself.

Technology exists to support the domain—not define it.

---

# Summary

Project Pirouette models the operation of a dance academy through five primary entities:

- Teacher
- Studio
- Availability
- Dance Class
- Schedule Entry

These entities provide the foundation for scheduling, conflict detection, reporting, visualization, and future expansion.