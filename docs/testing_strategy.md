# Project Pirouette Testing Strategy

## Purpose

This document defines the testing strategy for Project Pirouette.

The goal is to verify that Pirouette behaves correctly, protects schedule integrity, remains usable, and provides clear feedback when a user attempts an invalid action.

Testing should focus on business behavior, not only whether the application launches.

---

# Testing Objectives

Pirouette testing should confirm that the application:

- Stores valid data
- Rejects invalid data
- Prevents scheduling conflicts
- Preserves database integrity
- Displays accurate schedule information
- Responds correctly to user interaction
- Handles resizing and window changes
- Produces understandable error messages
- Preserves data between sessions
- Remains stable during common user mistakes

---

# Testing Approach

Pirouette currently uses a combination of:

- Manual functional testing
- Exploratory testing
- Business-rule validation
- Regression testing
- UI behavior testing
- Persistence testing

Future versions should add automated tests for business and data-access logic.

---

# Testing Levels

## 1. Unit Testing

Unit tests should verify small, isolated pieces of logic.

Examples include:

- Time conversion
- End-time calculation
- Overlap detection
- Weekday mapping
- Validation helper functions
- Export formatting helpers

Planned test location:

```text
tests/
```

Possible files:

```text
tests/test_time_utils.py
tests/test_validators.py
tests/test_exporter.py
```

---

## 2. Database Testing

Database tests should verify that data is stored, retrieved, and protected correctly.

Important areas include:

- Table creation
- Foreign-key enforcement
- Duplicate prevention
- Delete restrictions
- Cascading availability deletion
- Schedule conflict queries
- Filtered schedule queries
- Database persistence

Possible file:

```text
tests/test_database.py
```

---

## 3. Integration Testing

Integration testing should verify that multiple parts of Pirouette work together.

Examples include:

- Creating a teacher and assigning availability
- Creating a class and selecting a preferred teacher
- Scheduling a class into a studio
- Displaying the saved entry in List View
- Displaying the same entry in Weekly Calendar
- Deleting a schedule entry and refreshing both views

---

## 4. User Interface Testing

UI testing should verify visible application behavior.

Important areas include:

- Buttons display correctly
- Labels remain readable
- Forms reject missing required values
- Dropdowns update when records are added or removed
- Window resizing does not hide controls
- Pop-out calendar resizes correctly
- Hover behavior does not corrupt text
- Calendar selection remains visible
- Double-click opens class details
- Right-click context menu works
- Delete buttons operate from both views

---

## 5. Exploratory Testing

Exploratory testing is an important part of Pirouette development.

The tester should actively try actions that a normal user may perform, including:

- Leaving fields blank
- Entering duplicate names
- Scheduling outside availability
- Reusing an occupied studio
- Double-booking a teacher
- Deleting records in the wrong order
- Resizing windows
- Switching between views
- Reopening the application
- Repeating clicks quickly
- Selecting records and changing filters

Unexpected behavior should be documented and converted into regression coverage where practical.

---

# Core Business Rules to Test

## Required Field Validation

Verify that Pirouette blocks missing required data.

Examples:

- Blank teacher name
- Blank studio name
- Blank class name
- Missing teacher selection
- Missing studio selection
- Missing class selection

Expected result:

Pirouette displays a clear message and does not save incomplete data.

---

## Duplicate Teacher Prevention

Steps:

1. Add a teacher.
2. Attempt to add the same teacher again.
3. Repeat using different capitalization.

Expected result:

Pirouette blocks the duplicate and explains that the teacher already exists.

---

## Duplicate Studio Prevention

Steps:

1. Add a studio.
2. Attempt to add the same studio again.
3. Repeat using different capitalization.

Expected result:

Pirouette blocks the duplicate.

---

## Duplicate Class Prevention

Steps:

1. Add a class.
2. Attempt to add the same active class again.

Expected result:

Pirouette blocks the duplicate.

---

## Availability Time Validation

Steps:

1. Select a teacher.
2. Choose an end time earlier than the start time.
3. Attempt to save.

Expected result:

Pirouette blocks the entry and explains that the end time must be later.

---

## Availability Overlap Validation

Steps:

1. Add Monday availability from 4:00 PM to 8:00 PM.
2. Attempt to add Monday availability from 6:00 PM to 9:00 PM.

Expected result:

Pirouette blocks the overlapping availability.

---

## Teacher Availability Validation

Steps:

1. Give a teacher availability from 4:00 PM to 6:00 PM.
2. Attempt to schedule a class from 5:30 PM to 6:30 PM.

Expected result:

Pirouette blocks the schedule because the teacher is not available for the full class duration.

---

## Teacher Double-Booking Validation

Steps:

1. Schedule a teacher from 4:00 PM to 5:00 PM.
2. Attempt to schedule the same teacher from 4:30 PM to 5:30 PM.

Expected result:

Pirouette blocks the second class and identifies the existing conflict.

---

## Studio Double-Booking Validation

Steps:

1. Schedule a class in Studio A from 4:00 PM to 5:00 PM.
2. Attempt to schedule another class in Studio A from 4:30 PM to 5:30 PM.

Expected result:

Pirouette blocks the second class and recommends choosing another studio or time.

---

## Adjacent Time Validation

Steps:

1. Schedule a class from 4:00 PM to 5:00 PM.
2. Schedule another class using the same teacher or studio from 5:00 PM to 6:00 PM.

Expected result:

Pirouette allows the second class because the time ranges touch but do not overlap.

---

## Multi-Conflict Reporting

Steps:

1. Choose a teacher who is unavailable.
2. Choose a studio that is already occupied.
3. Attempt to schedule the class.

Expected result:

Pirouette reports all detected conflicts together rather than stopping after the first issue.

---

# Calendar Testing

## List View Accuracy

Verify that each row displays:

- Day
- Start time
- End time
- Class
- Teacher
- Studio

Expected result:

The displayed information matches the database.

---

## Weekly Calendar Placement

Steps:

1. Schedule classes on multiple days and times.
2. Open Weekly Calendar.

Verify:

- Each class appears under the correct day.
- Each class begins at the correct time.
- Class height reflects duration.
- Teacher and studio names are correct.
- Dance-style color is correct.

---

## Calendar Filter Testing

Test:

- All teachers
- One teacher
- All studios
- One studio
- Combined teacher and studio filters

Expected result:

Only matching schedule entries remain visible.

---

## Calendar Selection Testing

Steps:

1. Click a class card.
2. Observe the selected border.
3. Click empty calendar space.

Expected result:

The selected class is highlighted, and selection clears when appropriate.

---

## Hover Testing

Steps:

1. Move the pointer over a class card.
2. Move it away.

Expected result:

Only the card border changes.

The class text must not wrap into a narrow vertical column or otherwise become distorted.

---

## Double-Click Testing

Steps:

1. Double-click a class card.

Expected result:

Pirouette displays class details including:

- Class name
- Style
- Teacher
- Studio
- Day
- Time

---

## Calendar Delete Testing

Test deletion from:

- List View
- Embedded Weekly Calendar
- Pop-Out Weekly Schedule
- Right-click context menu

Expected result:

The entry is removed from the database and all visible views refresh.

---

# Pop-Out Calendar Testing

Verify that the pop-out calendar:

- Opens only one active window
- Displays Monday through Saturday
- Fits the available width
- Expands rows to use available height
- Resizes when maximized or restored
- Preserves readable class-card text
- Allows class selection
- Opens class details
- Deletes selected classes
- Closes cleanly

---

# Responsive Layout Testing

Test the application at:

- Minimum supported window size
- Normal windowed size
- Maximized size
- Pop-out maximized size

Verify:

- Buttons remain readable
- No control appears blank because of compression
- Calendar columns remain usable
- Horizontal white space is minimized
- Scrollbars appear only when needed
- Text does not overlap or become clipped

---

# Persistence Testing

Steps:

1. Add teachers.
2. Add studios.
3. Add classes.
4. Add availability.
5. Add schedule entries.
6. Close Pirouette.
7. Reopen Pirouette.

Expected result:

All saved data remains available.

---

# Delete Integrity Testing

## Teacher Deletion

Verify:

- A teacher with no schedule entries may be deleted.
- The teacher’s availability is deleted automatically.
- A teacher assigned to a schedule entry cannot be deleted until the schedule entry is removed.

---

## Studio Deletion

Verify:

- An unused studio may be deleted.
- A studio assigned to a schedule entry cannot be deleted until the schedule entry is removed.

---

## Class Deletion

Verify:

- An unused class may be deleted.
- A class on the schedule cannot be deleted until its schedule entries are removed.

---

# Error Handling Testing

Pirouette should not crash when:

- A required field is blank
- A selected record no longer exists
- The database rejects an operation
- A user clicks Delete without selecting a record
- A user opens the pop-out more than once
- A user closes the pop-out during refresh
- The window is resized repeatedly

Expected result:

The application displays a clear message or safely ignores the invalid action.

---

# Regression Testing

Every resolved defect should be considered for regression coverage.

Known regression areas include:

## Legend Background Error

Issue:

A `ttk.Frame` background was read using `cget("background")`, which caused a Tkinter error.

Regression expectation:

The legend should render without attempting unsupported `ttk` background access.

---

## Hover Text Collapse

Issue:

Hover styling applied `width` to all canvas items, causing text to wrap into a narrow vertical column.

Regression expectation:

Hover changes only the border item.

---

## Blank Availability Button

Issue:

A delete button appeared blank at smaller window sizes because the layout compressed it.

Regression expectation:

The button text remains visible at the minimum supported application size.

---

## Pop-Out Calendar Compression

Issue:

The full weekly schedule used a fixed row height and occupied only a small portion of the window.

Regression expectation:

The pop-out dynamically calculates row height and fills the available vertical space.

---

# Excel Export Testing

When Excel export is implemented, tests should verify:

- Workbook is created successfully
- File opens in Microsoft Excel
- Weekly schedule data is accurate
- Teacher sheets contain correct classes
- Studio sheets contain correct classes
- Times are formatted correctly
- Column widths are readable
- Headers are styled
- Frozen panes work
- Print settings are appropriate
- Empty schedules export gracefully
- Existing files are not overwritten without confirmation

---

# Automated Testing Roadmap

Planned automated coverage should prioritize:

1. Time calculations
2. Availability overlap logic
3. Teacher conflict logic
4. Studio conflict logic
5. Database CRUD operations
6. Foreign-key delete behavior
7. Schedule filtering
8. Excel export accuracy

UI automation may be added later where practical.

---

# Test Data

A reusable manual test dataset should include:

## Teachers

- Brooke
- Lynn
- Tammy

## Studios

- Studio A
- Studio B
- Studio C

## Classes

- Tiny Tots Ballet
- Beginner Jazz
- Competitive Teen Acro

## Availability

- Brooke: Monday, 4:00 PM–8:00 PM
- Lynn: Tuesday, 4:00 PM–8:00 PM
- Tammy: Wednesday, 4:00 PM–8:00 PM

This dataset supports normal scheduling, conflicts, filters, and calendar visualization.

---

# Test Evidence

Testing evidence may include:

- Screenshots
- Test checklists
- Defect notes
- Git commit references
- Release notes
- Automated test output

Future releases should document major validation performed before publication.

---

# Release Readiness Criteria

A Pirouette release should not be published until:

- The application launches without errors.
- Core records can be created and deleted.
- Conflict rules behave correctly.
- Schedule data persists.
- List View and Weekly Calendar agree.
- Pop-out calendar behaves correctly.
- Known critical defects are resolved.
- Documentation reflects the current version.
- The Git repository does not include the live database.
- The release has a clear version number.

---

# Summary

Pirouette testing focuses on:

- Business-rule correctness
- Data integrity
- User experience
- Schedule accuracy
- Responsive behavior
- Regression prevention
- Reliable persistence

The objective is not merely to prove that the application runs.

The objective is to prove that Pirouette helps users create valid schedules safely, clearly, and consistently.