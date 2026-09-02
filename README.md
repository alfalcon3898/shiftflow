# ShiftFlow

A command-line employee scheduling tool built in Python. ShiftFlow helps managers track employees, their roles, and their availability — replacing the paper, spreadsheets, and disconnected apps many small businesses still rely on.

## The Problem

As a manager, I've seen firsthand how much time gets lost building schedules by hand — time that could go toward actually training and supporting a team. I've also seen crew members miss shifts or struggle to request a shift swap simply because there was no easy system for it. ShiftFlow is being built to fix that, starting with the fundamentals: reliable employee and availability tracking, with real scheduling and conflict-detection logic planned as the project grows.

## Status

**Current version: V1 (in progress toward V2)**

V1 is a functional, procedural Python CLI application. It manages employees and their stated availability, but does not yet include actual shift scheduling, conflict detection, or a database backend — those are planned enhancements (see below).

## Features (V1)

- Add a new employee (name, role)
- Search for an employee by name
- View all employees, sorted alphabetically, with their availability
- View a single employee's details
- Update an employee's availability
- Remove a specific availability entry
- Clear all of an employee's availability
- Delete an employee
- Update an employee's role
- Count total employees
- Data persists to a local `employees.json` file between runs

## Tech Stack

- **Language:** Python 3
- **Storage:** JSON (flat file) — planned migration to SQLite
- **Interface:** Command-line menu

## How to Run

1. Make sure Python 3 is installed.
2. Clone or download this repository.
3. Run the script from a terminal:
   ```
   python shiftflow.py
   ```
4. Use the on-screen numbered menu to add employees, manage availability, and more. Data is automatically saved to `employees.json` after any change.

## Known Limitations (V1)

This version is intentionally simple, and enhancing it is the focus of ongoing work:

- No object-oriented structure — employees are represented as plain dictionaries, not classes
- Minimal input validation — invalid or malformed input can currently be saved without being caught
- No automated tests
- No actual shift/schedule concept yet — only employee availability is tracked, not assigned shifts
- No conflict detection, since there is no scheduling logic yet to have conflicts in
- Data stored in a flat JSON file, with no schema or relational integrity

## Planned Enhancements

ShiftFlow is being actively developed in three stages:

1. **Software Design & Engineering** — refactor into an object-oriented design (`Employee`, `Shift`, `Schedule` classes), add encapsulation, proper error handling, and automated tests with `pytest`.
2. **Algorithms & Data Structures** — build real shift/schedule logic, including conflict detection, coverage checking, overtime tracking, a shift-swap request feature, and a seniority-and-preference-based fair hour distribution algorithm that reflects real labor-budget constraints.
3. **Databases** — migrate from JSON to a normalized SQLite schema (employees, shifts, roles, availability tables), with all data access routed through a proper database layer.

## Long-Term Vision (Beyond the Capstone)

Once the core rebuild above is complete, ShiftFlow is intended to grow into a full mobile-friendly scheduling platform:

- **Attendance tracking** — record call-offs and no-shows per employee, so managers can see patterns over time (e.g., how many times a given worker has called off) rather than relying on memory.
- **Shift-swap requests, mobile-first** — an employee requests a shift change from their phone; once another employee accepts, a notification goes out for approval to the GM (always notified), plus the specific shift leader/mod who is actually scheduled to be in charge that day — not every mod, just the one on duty, so people aren't bothered about shifts they have nothing to do with. Once approved, the schedule updates automatically.
- **AI-assisted scheduling** — the schedule itself adjusts automatically as shift-swap requests are approved, rather than requiring a manager to manually rebuild it.
- **Gamified customization** — a lighter, more engaging layer on top of the core tool:
  - Each business can apply its own branding/logo with a fun, customized style (e.g., a company's logo reimagined in a friendly, stylized way).
  - Each employee gets a customizable character/avatar.
  - Employees unlock new customization options for their character by showing up on time and maintaining good attendance — turning a basic scheduling need into something more engaging to actually use.

This long-term vision is separate from the CS 499 capstone scope (which focuses on the three enhancement categories above) but represents the direction the project is headed as a personal/SaaS product afterward.

## Author

Built by Allen Falcon, Computer Science student at Southern New Hampshire University, as an independent project and CS 499 capstone artifact.
