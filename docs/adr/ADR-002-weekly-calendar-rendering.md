# ADR-002: Use a Shared Calendar Rendering Engine for Both Embedded and Pop-Out Weekly Calendars

## Status

Accepted

## Date

2026-08-03

## Context

Project Pirouette provides two different calendar views:

- Embedded Weekly Calendar
- Pop-Out Weekly Schedule

Both views present the same scheduling information but serve different purposes.

The embedded calendar is intended for day-to-day interaction within the main application window.

The pop-out calendar provides a larger planning and presentation view that can be resized or maximized independently.

Early implementation considered maintaining two independent rendering functions.

Although this approach would allow each calendar to evolve independently, it would also duplicate rendering logic and increase maintenance effort.

## Decision

Pirouette will use a single shared calendar rendering engine to draw both the embedded and pop-out weekly calendars.

Both views will render the same scheduling data using the same layout calculations while allowing presentation-specific configuration through rendering parameters.

Examples include:

- compact mode
- responsive row sizing
- fit-to-width behavior
- full-height rendering
- popup-specific formatting

## Rationale

Both calendar views represent the same business information.

Maintaining separate rendering engines would require duplicate implementation for:

- time grid generation
- class placement
- overlap calculations
- event selection
- hover behavior
- color mapping
- teacher and studio filtering
- resizing logic

Duplicated logic increases the likelihood that one calendar behaves differently than the other.

A shared renderer ensures consistent behavior across the application.

## Benefits

Using one renderer provides:

- Single implementation of rendering logic
- Consistent class placement
- Consistent schedule appearance
- Reduced maintenance effort
- Easier bug fixes
- Easier feature additions
- Less duplicated code

Improvements automatically benefit both calendar views.

---

## Rendering Responsibilities

The shared renderer is responsible for:

- Building the time grid
- Calculating day columns
- Calculating row positions
- Determining class placement
- Rendering class cards
- Drawing schedule text
- Applying dance-style colors
- Managing selection
- Managing hover effects
- Supporting responsive resizing

The renderer is **not** responsible for:

- Reading database records
- Performing validation
- Scheduling classes
- Managing application workflow

Those responsibilities remain elsewhere in the application.

---

# Presentation Differences

The renderer supports configuration options that allow each calendar to present information differently without changing the underlying rendering logic.

Examples include:

## Embedded Calendar

- Compact layout
- Integrated into the main window
- Designed for quick editing
- Fixed working area

## Pop-Out Calendar

- Larger presentation mode
- Responsive row sizing
- Expanded text
- Larger schedule blocks
- Full-window viewing

These differences are controlled through rendering parameters rather than duplicate rendering code.

---

# Alternatives Considered

## Separate Rendering Functions

One option was to create:

```text
draw_embedded_calendar()

draw_popup_calendar()
```

Advantages:

- Complete independence
- Easier experimentation

Disadvantages:

- Large amount of duplicated logic
- Higher maintenance cost
- Greater risk of inconsistent behavior
- Duplicate bug fixes
- Duplicate feature implementation

This option was rejected.

---

## Separate Renderer Classes

A second option was to implement two renderer classes.

Advantages:

- Strong separation
- Independent customization

Disadvantages:

- Significant code duplication
- Additional complexity
- Little benefit for the current application

This option was also rejected.

---

# Consequences

## Positive

- Reduced code duplication
- Easier maintenance
- Consistent rendering
- Shared bug fixes
- Shared improvements
- Simpler architecture
- Easier testing

## Negative

- Renderer becomes more configurable
- Additional rendering options require careful design
- Rendering changes affect both calendar views

These tradeoffs were considered acceptable.

---

# Known Improvements

Future versions may introduce:

- Drag-and-drop scheduling
- Zoom levels
- Different calendar themes
- Read-only presentation mode
- Print layout rendering
- Weekly export rendering
- Resource utilization overlays

The shared renderer should continue supporting these features through configuration rather than duplication.

---

# Lessons Learned

During development several rendering issues reinforced this decision.

Examples included:

- Hover effects unintentionally modifying text layout
- Fixed row heights limiting the pop-out calendar
- Window resizing behavior
- Responsive layout improvements

Because both calendars shared the same rendering engine, each correction immediately benefited both views.

This reduced development effort and improved consistency.

---

# Decision Outcome

Project Pirouette will maintain a single reusable calendar rendering engine that supports multiple presentation modes through configuration.

This decision improves maintainability, reduces duplicated logic, and ensures consistent schedule visualization throughout the application.