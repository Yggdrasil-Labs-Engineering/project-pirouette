# Project Pirouette Database Schema

## Purpose

This document describes the SQLite database schema used by Project Pirouette.

The database stores the operational data required to manage teachers, studios, dance classes, weekly availability, and scheduled classes.

The schema is designed to support:

- Reliable persistence
- Data integrity
- Scheduling validation
- Conflict detection
- Clear entity relationships
- Future expansion

---

# Database Technology

Pirouette currently uses:

```text
SQLite
```

SQLite was selected because it provides:

- Lightweight deployment
- No separate database server
- Strong support in Python
- Reliable local persistence
- Easy backup and portability
- Suitability for a desktop application

The active database file is:

```text
pirouette.db
```

The live database should not be committed to public source control.

---

# Schema Overview

Pirouette currently uses five primary tables:

```text
teachers
studios
dance_classes
teacher_availability
schedule_entries
```

These tables map directly to the core entities in the Pirouette domain model.

---

# Entity Relationship Overview

```text
teachers
    │
    ├──────────────┐
    │              │
    ▼              ▼
teacher_availability
                   dance_classes
                        │
                        ▼
                 schedule_entries
                        ▲
                        │
                     studios
```

More specifically:

```text
Teacher
  ├── has many Availability records
  ├── may be the preferred teacher for many Dance Classes
  └── may be assigned to many Schedule Entries

Studio
  └── may host many Schedule Entries

Dance Class
  └── may appear in many Schedule Entries
```

---

# Table: teachers

## Purpose

Stores teacher records.

## Columns

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto Increment | Unique teacher identifier |
| `name` | TEXT | Not Null, Unique, Case Insensitive | Teacher name |
| `active` | INTEGER | Not Null, Default `1` | Indicates whether the teacher is active |

## Definition

```sql
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
    active INTEGER NOT NULL DEFAULT 1
);
```

## Business Rules

- Teacher names cannot be blank.
- Teacher names must be unique.
- Duplicate names are checked case-insensitively.
- A teacher assigned to an existing schedule entry cannot be deleted until the schedule entry is removed.

---

# Table: studios

## Purpose

Stores physical dance studio or room records.

## Columns

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto Increment | Unique studio identifier |
| `name` | TEXT | Not Null, Unique, Case Insensitive | Studio name |
| `active` | INTEGER | Not Null, Default `1` | Indicates whether the studio is active |

## Definition

```sql
CREATE TABLE IF NOT EXISTS studios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
    active INTEGER NOT NULL DEFAULT 1
);
```

## Business Rules

- Studio names cannot be blank.
- Studio names must be unique.
- Duplicate names are checked case-insensitively.
- A studio assigned to an existing schedule entry cannot be deleted until the schedule entry is removed.

---

# Table: dance_classes

## Purpose

Stores the dance classes offered by the academy.

A dance class is defined independently from its scheduled time and location.

## Columns

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto Increment | Unique class identifier |
| `name` | TEXT | Not Null, Case Insensitive | Class name |
| `style` | TEXT | Not Null | Dance style |
| `age_group` | TEXT | Optional | Intended age group |
| `duration_minutes` | INTEGER | Not Null, Default `60` | Class duration in minutes |
| `preferred_teacher_id` | INTEGER | Foreign Key, Optional | Preferred teacher |
| `active` | INTEGER | Not Null, Default `1` | Indicates whether the class is active |

## Definition

```sql
CREATE TABLE IF NOT EXISTS dance_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE,
    style TEXT NOT NULL,
    age_group TEXT,
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    preferred_teacher_id INTEGER,
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (preferred_teacher_id)
        REFERENCES teachers(id)
        ON DELETE SET NULL
);
```

## Business Rules

- Class names cannot be blank.
- Active class names should not be duplicated.
- Duration must be greater than zero.
- A preferred teacher is optional.
- If the preferred teacher is deleted, the preferred teacher field is set to `NULL`.
- A class already used by the schedule cannot be deleted until its schedule entries are removed.

---

# Table: teacher_availability

## Purpose

Stores recurring weekly availability for teachers.

Each record defines one period during which a teacher is available to teach.

## Columns

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto Increment | Unique availability identifier |
| `teacher_id` | INTEGER | Not Null, Foreign Key | Teacher |
| `weekday` | INTEGER | Not Null, Check `0–6` | Day of week |
| `start_time` | TEXT | Not Null | Start time in 24-hour format |
| `end_time` | TEXT | Not Null | End time in 24-hour format |

## Definition

```sql
CREATE TABLE IF NOT EXISTS teacher_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    UNIQUE (
        teacher_id,
        weekday,
        start_time,
        end_time
    ),
    FOREIGN KEY (teacher_id)
        REFERENCES teachers(id)
        ON DELETE CASCADE
);
```

## Weekday Values

| Value | Day |
|---:|---|
| `0` | Monday |
| `1` | Tuesday |
| `2` | Wednesday |
| `3` | Thursday |
| `4` | Friday |
| `5` | Saturday |
| `6` | Sunday |

## Time Format

Times are stored using 24-hour text values.

Examples:

```text
16:00
17:30
20:00
```

## Business Rules

- Availability must belong to a valid teacher.
- Start time must be earlier than end time.
- Exact duplicate availability records are not allowed.
- Overlapping availability periods for the same teacher and day are blocked.
- Deleting a teacher automatically deletes that teacher’s availability records.

---

# Table: schedule_entries

## Purpose

Stores scheduled class occurrences.

This table connects a dance class, teacher, studio, day, and time range.

## Columns

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Auto Increment | Unique schedule-entry identifier |
| `class_id` | INTEGER | Not Null, Foreign Key | Scheduled dance class |
| `teacher_id` | INTEGER | Not Null, Foreign Key | Assigned teacher |
| `studio_id` | INTEGER | Not Null, Foreign Key | Assigned studio |
| `weekday` | INTEGER | Not Null, Check `0–6` | Scheduled day |
| `start_time` | TEXT | Not Null | Start time in 24-hour format |
| `end_time` | TEXT | Not Null | End time in 24-hour format |

## Definition

```sql
CREATE TABLE IF NOT EXISTS schedule_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    studio_id INTEGER NOT NULL,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    FOREIGN KEY (class_id)
        REFERENCES dance_classes(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (teacher_id)
        REFERENCES teachers(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (studio_id)
        REFERENCES studios(id)
        ON DELETE RESTRICT
);
```

## Business Rules

Before insertion, Pirouette verifies:

- The class exists.
- The teacher exists.
- The studio exists.
- Start time is earlier than end time.
- The teacher is available for the complete time range.
- The teacher is not already scheduled during an overlapping period.
- The studio is not already occupied during an overlapping period.

Only schedule entries that pass all validation checks should be stored.

---

# Indexes

Pirouette uses indexes to improve scheduling and conflict-query performance.

## Teacher Availability Index

```sql
CREATE INDEX IF NOT EXISTS idx_availability_teacher_day
    ON teacher_availability (
        teacher_id,
        weekday
    );
```

Supports:

- Teacher availability lookup
- Day-specific availability validation

---

## Teacher Schedule Index

```sql
CREATE INDEX IF NOT EXISTS idx_schedule_teacher_day
    ON schedule_entries (
        teacher_id,
        weekday
    );
```

Supports:

- Teacher conflict detection
- Teacher schedule filtering

---

## Studio Schedule Index

```sql
CREATE INDEX IF NOT EXISTS idx_schedule_studio_day
    ON schedule_entries (
        studio_id,
        weekday
    );
```

Supports:

- Studio conflict detection
- Studio schedule filtering

---

# Foreign Key Behavior

Pirouette enables SQLite foreign-key enforcement with:

```sql
PRAGMA foreign_keys = ON;
```

Foreign-key actions include:

| Relationship | Delete Behavior |
|---|---|
| Teacher → Availability | Cascade |
| Teacher → Preferred Class Assignment | Set Null |
| Teacher → Schedule Entry | Restrict |
| Studio → Schedule Entry | Restrict |
| Dance Class → Schedule Entry | Restrict |

These rules protect schedule integrity.

---

# Conflict Detection Logic

Pirouette uses overlapping-time comparisons.

Two time ranges conflict when:

```text
existing_start < proposed_end
AND
existing_end > proposed_start
```

This allows adjacent classes such as:

```text
4:00 PM–5:00 PM
5:00 PM–6:00 PM
```

because the ranges touch but do not overlap.

It blocks ranges such as:

```text
4:00 PM–5:00 PM
4:30 PM–5:30 PM
```

because the time periods overlap.

---

# Data Access Responsibilities

Database operations are currently implemented in:

```text
database.py
```

Responsibilities include:

- Database initialization
- Table creation
- Record insertion
- Record retrieval
- Record deletion
- Duplicate detection
- Availability validation
- Schedule conflict lookup
- Schedule filtering

The user interface should not execute raw SQL directly.

---

# Data Integrity Principles

Pirouette should preserve the following guarantees:

- Every availability record belongs to a valid teacher.
- Every schedule entry references valid entities.
- Teachers cannot be double-booked.
- Studios cannot be double-booked.
- Scheduled classes remain within teacher availability.
- Destructive actions are restricted when records are still in use.
- The live database is excluded from the public Git repository.

---

# Backup and Portability

Because Pirouette uses SQLite, the database can be backed up by copying:

```text
pirouette.db
```

The application should be closed before copying, moving, or replacing the database file to avoid file-locking issues.

Future versions may include:

- Built-in backup
- Restore support
- Exported data snapshots
- Database migration tooling

---

# Future Schema Expansion

Possible future tables include:

## students

Stores student information.

## enrollments

Links students to classes.

## seasons

Defines scheduling years or terms.

## attendance

Stores class attendance.

## performances

Stores recital and performance events.

## tuition

Stores billing information.

## waitlists

Stores students awaiting class placement.

## schedule_exceptions

Stores holidays, cancellations, substitute teachers, and temporary schedule changes.

---

# Current Limitations

The current schema does not yet support:

- Multiple seasons
- Date-specific schedules
- Holiday exceptions
- Recurring-pattern variation
- Student enrollment
- Attendance
- Tuition
- Audit history
- Soft deletion across all entities
- Database migration versions

These features may be introduced as the application evolves.

---

# Summary

The Pirouette database schema supports the core scheduling workflow through five tables:

- `teachers`
- `studios`
- `dance_classes`
- `teacher_availability`
- `schedule_entries`

The schema emphasizes:

- Referential integrity
- Conflict prevention
- Lightweight desktop persistence
- Clear entity relationships
- Future extensibility

This structure provides a stable foundation for scheduling, visualization, filtering, reporting, and Excel export.