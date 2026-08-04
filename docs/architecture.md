# Project Pirouette Architecture

## Purpose

This document describes the overall software architecture of Project Pirouette.

The goal of this architecture is to provide a clean separation of responsibilities between the user interface, business logic, data access layer, and persistent storage.

Pirouette is designed as a desktop application that emphasizes readability, maintainability, and future extensibility.

---

# Architectural Philosophy

Pirouette follows several core architectural principles.

- One Module, One Responsibility
- Business Rules Before Persistence
- User-Centered Design
- Separation of Presentation and Logic
- Small, Maintainable Components
- Extensible Architecture

Every component should have a clearly defined responsibility.

---

# High-Level Architecture

```text
                        User
                          │
                          ▼
               Tkinter Desktop Interface
                          │
                          ▼
                Application Workflow
                          │
                          ▼
           Scheduling & Validation Logic
                          │
                          ▼
                 Database Access Layer
                          │
                          ▼
                      SQLite Database
```

Each layer has a specific purpose and should avoid taking on responsibilities that belong to another layer.

---

# Current Architecture

## User Interface Layer

Responsible for:

- Forms
- User interaction
- Window management
- Calendar rendering
- User notifications
- Navigation
- Event handling

Current implementation:

```text
app.py
```

The UI should remain responsible only for presentation and user interaction.

Business rules should remain outside the presentation layer whenever practical.

---

# Application Workflow Layer

Coordinates application behavior.

Responsibilities include:

- Loading records
- Saving records
- Refreshing views
- Scheduling classes
- Updating calendars
- Responding to user actions

Current implementation:

```text
app.py
```

As Pirouette grows, portions of this layer may move into dedicated service modules.

---

# Business Rules Layer

Responsible for validating scheduling operations before changes are committed.

Current business rules include:

- Required field validation
- Teacher availability
- Teacher double booking
- Studio conflicts
- Duplicate prevention
- Invalid time validation

The business rules determine whether a schedule entry is valid.

The interface should simply display the results.

---

# Data Access Layer

Responsible for communication with SQLite.

Current implementation:

```text
database.py
```

Responsibilities include:

- Database initialization
- Table creation
- CRUD operations
- Query execution
- Conflict lookup
- Persistence

The data access layer should never perform user interface work.

---

# Domain Model

Domain entities represent the primary business objects within Pirouette.

Current implementation:

```text
models.py
```

Current entities include:

- Teacher
- Studio
- Availability
- Dance Class
- Schedule Entry

The domain model provides a shared language across the application.

---

# Persistent Storage

Pirouette currently stores information using SQLite.

Benefits include:

- Lightweight
- No external server
- Easy deployment
- Reliable persistence
- Simple backup strategy

Current database contains information for:

- Teachers
- Studios
- Weekly Availability
- Dance Classes
- Weekly Schedule

---

# Scheduling Workflow

Typical scheduling sequence:

```text
User Selects Class
        │
        ▼
User Chooses Day
        │
        ▼
User Chooses Studio
        │
        ▼
User Chooses Start Time
        │
        ▼
Validation Begins
        │
        ├── Required Fields
        ├── Teacher Availability
        ├── Teacher Conflict
        ├── Studio Conflict
        │
        ▼
Validation Successful?
        │
   ┌────┴────┐
   │         │
  Yes        No
   │         │
   ▼         ▼
Save      Display
Schedule  Conflict Report
```

Only validated schedules should be committed to the database.

---

# Calendar Rendering

Pirouette provides two schedule visualizations.

## Embedded Weekly Calendar

Purpose:

- Daily scheduling
- Quick review
- Interactive editing

Features:

- Monday–Saturday
- Teacher filter
- Studio filter
- Color-coded dance styles

---

## Pop-Out Weekly Calendar

Purpose:

- Full schedule review
- Presentation
- Planning

Features:

- Larger display
- Responsive layout
- Delete scheduled entries
- Detail viewing

Both calendars share the same rendering logic to reduce duplicated code.

---

# Current Modules

## app.py

Responsibilities:

- Desktop UI
- Event handling
- Calendar rendering
- Form validation
- Workflow coordination

---

## database.py

Responsibilities:

- SQLite communication
- CRUD operations
- Persistence
- Conflict queries

---

## models.py

Responsibilities:

- Domain entities
- Shared application objects

---

# Planned Modules

As Pirouette grows, responsibilities will be divided into dedicated modules.

## exporter.py

Purpose:

- Excel export
- Workbook formatting
- Printable schedules

---

## validators.py

Purpose:

- Shared business-rule validation

---

## services.py

Purpose:

- Scheduling operations
- Application workflows

---

## reports.py

Purpose:

- Teacher reports
- Studio reports
- Statistics
- Analytics

---

# Future Architecture

The long-term architecture is expected to evolve into:

```text
                 User Interface
                        │
                        ▼
               Application Services
                        │
                        ▼
             Business Rule Validation
                        │
                        ▼
                 Domain Model
                        │
                        ▼
                Repository Layer
                        │
                        ▼
                     SQLite
```

This structure reduces coupling and improves maintainability.

---

# Architectural Strengths

Current strengths include:

- Simple deployment
- Small dependency footprint
- Clear workflow
- Business-rule validation
- Interactive scheduling
- Persistent storage
- Modular documentation
- Desktop-first usability

---

# Current Limitations

Current architectural limitations include:

- `app.py` contains multiple responsibilities.
- Business rules are partially coupled to the interface.
- Reporting and export functionality are not yet separated.
- Automated testing is still under development.

These limitations are acceptable for the current development stage and are planned for future refactoring.

---

# Architectural Goals

Future development should continue improving:

- Separation of concerns
- Module independence
- Testability
- Reusability
- Documentation
- User experience
- Performance
- Maintainability

---

# Summary

Project Pirouette follows a layered desktop architecture designed around simplicity, maintainability, and extensibility.

By separating presentation, workflow, business rules, and persistence, the application remains easier to understand, test, and expand as new scheduling capabilities are introduced.

The architecture is intentionally designed to support future enhancements while remaining approachable for contributors and maintainers.