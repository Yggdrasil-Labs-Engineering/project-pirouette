# 🩰 Project Pirouette

> **Plan with Confidence. Schedule with Ease.**

Project Pirouette is a desktop scheduling application designed to help dance academies organize teachers, studios, class availability, and weekly schedules while preventing scheduling conflicts.

Although originally designed for dance studios, the scheduling engine is being developed in a way that can eventually support other businesses that require recurring weekly scheduling.

---

# Current Version

**Version:** 0.4.0

Status:

✅ Active Development

---

# Features

## Teachers

- Add teachers
- Delete teachers
- Persistent SQLite storage
- Duplicate teacher validation

---

## Weekly Availability

Assign weekly availability for each instructor.

Example:

Monday

4:00 PM – 8:00 PM

Features:

- Multiple teachers
- Day selection
- Start/End times
- Availability validation
- Delete availability
- SQLite persistence

---

## Studios

Manage available studios.

Features:

- Add studios
- Delete studios
- Duplicate prevention

Examples:

- Studio A
- Studio B
- Studio C

---

## Classes

Manage classes offered by the academy.

Each class stores:

- Class Name
- Dance Style
- Preferred Teacher
- Duration

Supported dance styles include:

- Ballet
- Tap
- Jazz
- Hip Hop
- Contemporary
- Acro
- Lyrical
- Musical Theatre
- Pointe
- Conditioning

---

## Scheduling Engine

Schedule classes onto a weekly calendar.

Each scheduled class includes:

- Teacher
- Studio
- Day
- Start Time
- End Time

---

## Conflict Detection

Pirouette validates schedules before saving.

Checks include:

### Teacher Availability

Example:

Teacher Lynn is unavailable Monday from 4:00 PM–5:00 PM.

---

### Teacher Double Booking

Teachers cannot be assigned to two classes simultaneously.

---

### Studio Double Booking

Studios cannot host more than one class at the same time.

---

### Multi-Issue Reporting

Pirouette reports all detected scheduling problems rather than stopping after the first error.

Example:

Unable to schedule Tiny Tots.

Problems found:

• Teacher unavailable

• Studio conflict

---

# Weekly Calendar

Interactive weekly calendar.

Features:

- Monday–Saturday view
- Color-coded dance styles
- Weekly schedule visualization
- Teacher filtering
- Studio filtering
- Hover highlighting
- Double-click class details
- Delete scheduled classes
- Responsive calendar layout

---

# Pop-Out Weekly Schedule

Large presentation view.

Features:

- Dedicated weekly schedule window
- Monday–Saturday layout
- Full-screen support
- Click to select classes
- Double-click for details
- Delete scheduled classes

---

# Branding

Pirouette includes a consistent desktop application identity.

Features:

- Custom logo
- Product branding
- About dialog
- Version information
- Unified color palette

---

# Data Storage

Database:

SQLite

Tables include:

- Teachers
- Studios
- Availability
- Classes
- Schedule

---

# Technology

Language

- Python

GUI

- Tkinter
- ttk

Database

- SQLite

Architecture

- Modular desktop application
- Business-rule validation
- Responsive calendar rendering

---

# Screenshots

## Weekly Calendar

*(Insert screenshot here)*

---

## Full Weekly Schedule

*(Insert screenshot here)*

---

## Teacher Management

*(Insert screenshot here)*

---

# Planned Features

## Excel Export

Generate:

- Weekly schedule
- Teacher schedules
- Studio schedules
- Printable reports

---

## Drag and Drop Scheduling

Move classes by dragging them on the calendar.

Automatic validation:

- Teacher availability
- Studio availability
- Scheduling conflicts

---

## Printing

Print-friendly schedules.

---

## Statistics

Examples:

- Teacher hours
- Studio utilization
- Classes per day
- Weekly totals

---

## Packaging

- Windows installer
- Standalone executable

---

# Project Philosophy

Project Pirouette is being developed as a practical software engineering portfolio project.

The focus is not simply writing code, but building software that solves real problems through:

- Clean user interface
- Strong validation
- Clear business rules
- Ease of use
- Professional desktop experience

---

# Roadmap

Current Version

✅ Teacher Management

✅ Studio Management

✅ Class Management

✅ Weekly Availability

✅ Scheduling Engine

✅ Conflict Detection

✅ Weekly Calendar

✅ Pop-Out Schedule

✅ Branding

🔄 Excel Export

🔄 Drag-and-Drop Scheduling

🔄 Printing

🔄 Installer

---

# Author

Lawrence Luna

Project Pirouette is part of a growing portfolio of desktop software projects focused on practical business automation and user-centered design.
