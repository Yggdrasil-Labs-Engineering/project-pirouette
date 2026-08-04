# ADR-001: Use Python, Tkinter, and SQLite for the Pirouette Desktop Application

## Status

Accepted

## Date

2026-08-03

## Context

Project Pirouette began as a focused desktop scheduling application intended to help manage recurring dance academy schedules.

The initial product needed to support:

- Teacher management
- Studio management
- Class management
- Weekly teacher availability
- Schedule creation
- Conflict detection
- Visual weekly calendar rendering
- Local data persistence
- Simple deployment to a Windows laptop

The application needed to be developed quickly while remaining understandable, maintainable, and suitable for a portfolio demonstration.

A lightweight desktop architecture was preferred over a web-based solution because the initial target user did not require:

- Multi-user access
- Cloud hosting
- Browser-based deployment
- Centralized authentication
- Remote database infrastructure

The technology stack needed to minimize setup complexity while still supporting a professional user interface, reliable local storage, and future packaging as a standalone Windows application.

## Decision

Pirouette will use:

- Python as the primary programming language
- Tkinter and ttk for the desktop user interface
- SQLite for local persistent storage

## Rationale

### Python

Python was selected because it supports:

- Rapid development
- Readable syntax
- Strong standard-library support
- SQLite integration
- Desktop application development
- Excel export through external libraries such as `openpyxl`
- Automated testing through `pytest`
- Future refactoring into services, validators, and exporters

Python also aligns with the broader Yggdrasil Labs Engineering toolset and supports consistent development practices across projects.

### Tkinter and ttk

Tkinter was selected because it:

- Is included with standard Python installations
- Requires no separate frontend framework
- Supports forms, tabs, dialogs, tables, canvases, and multiple windows
- Works well for a focused desktop MVP
- Can be packaged into a standalone executable
- Provides enough flexibility to build an interactive weekly calendar

The `ttk` themed widget set provides improved styling and consistency over basic Tkinter widgets.

### SQLite

SQLite was selected because it:

- Requires no separate server
- Stores data in a single local file
- Is included with Python
- Supports foreign keys, constraints, indexes, and transactions
- Is suitable for single-user desktop applications
- Simplifies backup and portability
- Can support Pirouette’s current data volume and scheduling workload

## Alternatives Considered

### Web Application

A browser-based application using a frontend framework and web API was considered.

Potential benefits included:

- Remote access
- Multi-user support
- Easier centralized deployment
- Broader device compatibility

It was not selected for the initial version because it would introduce:

- More infrastructure
- More dependencies
- Hosting requirements
- Authentication concerns
- Increased development time
- Greater deployment complexity

A web version may be considered in the future if Pirouette expands beyond a single-user desktop application.

### Wails with Go and a Web Frontend

Wails was considered as a future desktop architecture.

Potential benefits include:

- Modern frontend capabilities
- Strong desktop packaging
- Go backend performance
- Separation between frontend and backend

It was not selected for the first version because the project needed to move quickly and validate the scheduling concept before introducing a larger technology stack.

### Electron

Electron was considered as another desktop option.

Potential benefits include:

- Modern web-based interface
- Large ecosystem
- Cross-platform support

It was not selected because:

- It has a larger runtime footprint
- It introduces more dependencies
- It is unnecessary for the current application size
- Tkinter is sufficient for the MVP

### PostgreSQL or MySQL

A server-based relational database was considered.

It was not selected because:

- Pirouette is currently a local single-user application
- A separate database server would add unnecessary complexity
- SQLite provides sufficient relational integrity and performance

A server database may be introduced if Pirouette evolves into a multi-user application.

## Consequences

### Positive Consequences

- Fast initial development
- Minimal installation requirements
- Simple local persistence
- Small dependency footprint
- Easier debugging
- Straightforward Windows packaging
- Strong compatibility with Python testing and export libraries
- Low operational overhead

### Negative Consequences

- Tkinter has limited modern styling compared with web frameworks
- Large UI files can become difficult to maintain
- Advanced drag-and-drop behavior may require custom implementation
- SQLite is not ideal for concurrent multi-user access
- A future migration may be required for web or cloud deployment
- Responsive desktop layouts require explicit management

## Mitigations

To reduce these limitations:

- UI responsibilities should gradually be separated from business logic
- Large modules should be refactored when responsibilities become unclear
- Calendar rendering should remain isolated and reusable
- Export logic should live in a dedicated module
- Business rules should remain independent of the UI
- Database access should remain centralized in `database.py`
- Architecture decisions should be documented before major technology changes

## Future Review Triggers

This decision should be reviewed if Pirouette requires:

- Multi-user access
- Cloud synchronization
- Browser-based usage
- Mobile support
- Real-time collaboration
- Centralized authentication
- Large-scale deployment
- Complex drag-and-drop interaction
- A significantly more modern visual framework

## Decision Outcome

Python, Tkinter, and SQLite provide the right balance of speed, simplicity, functionality, and maintainability for Pirouette’s current stage.

The stack supports the present desktop MVP while allowing the project to validate its scheduling model before adopting more complex infrastructure.