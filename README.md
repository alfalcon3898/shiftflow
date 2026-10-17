# ShiftFlow

ShiftFlow is a Python command-line employee scheduling application developed as a Southern New Hampshire University CS 499 capstone project. Inspired by firsthand restaurant management experience, it helps managers maintain employee records, track availability, create shifts, and apply scheduling rules while persisting data in SQLite.

## The Problem

Building schedules manually can consume time that managers could spend supporting employees. Disconnected spreadsheets and informal availability tracking can also cause scheduling errors.

ShiftFlow explores a structured approach to employee and shift management, with a longer-term goal of providing a mobile-friendly scheduling platform.

## Current Status

**Capstone enhancements: completed.**

The enhanced application integrates object-oriented models, scheduling logic, and SQLite persistence into a functional command-line interface.

**Testing results:**
- 110 automated tests passing in the most recently reported pytest run.
- Manual application tests passed, including employee management, availability, scheduling, database persistence, restarting, and deletion.
- These development checks do not constitute production-readiness certification.

## Implemented Features

- Add, search, view, update, and delete employees.
- Manage employee roles and day-specific availability, including all-day and time-block entries.
- Create and display assigned shifts, including shift duration and chronological schedule output.
- Reject overlapping shifts and shifts marked unavailable.
- Track weekly scheduled hours and check a 40-hour assignment threshold.
- Calculate staffing shortages from required and current staffing counts.
- Compare employees for hours allocation using remaining target hours and hire date, with random tie-breaking when both match.
- Save employees, availability, and shifts in SQLite, then restore saved assignments on restart.
- Preserve previously saved shifts when employee availability is subsequently changed.

Some scheduling helper methods are implemented in the `Schedule` class but are not exposed as interactive menu options. Automated shift generation, a shift-request workflow, notifications, and AI scheduling are **not** part of the current CLI.

## Tech Stack

- **Language:** Python 3
- **Interface:** Command-line application
- **Architecture:** Object-oriented `Employee`, `Shift`, and `Schedule` classes
- **Database:** SQLite via Python's `sqlite3` module
- **Testing:** `pytest`
- **Version control:** Git and GitHub

## Run the Application

1. Install Python 3 and clone or download the repository.
2. Open a terminal in the project directory containing `shiftflow.py`.
3. Start the CLI:

```bash
python shiftflow.py
```

Follow the numbered menu. The application initializes a local `shiftflow.db` file to store its records.

**Use fictional employee data when demonstrating or publishing this project.**

## Run Tests

Install pytest if necessary:

```bash
python -m pip install pytest
```

Run the automated suite from the project directory:

```bash
python -m pytest tests/ -q
```

The most recently reported suite result was **110 passing tests**, with warnings for missing availability entries. The manual CLI walkthrough also passed.

Test counts may change as regression coverage is expanded.

## CS 499 Capstone Enhancements

### Enhancement 1 — Software Design and Engineering

Refactored the original procedural employee-management program into reusable classes.

The `Employee` class manages identity, role, and availability; `Shift` models an assignment and validates its date and times; and `Schedule` encapsulates a collection of shifts.

Validation, private attributes, and controlled access methods improve maintainability and reduce malformed data.

### Enhancement 2 — Algorithms and Data Structures

Added scheduling checks for shift conflicts and employee availability, calculations for shift duration and weekly hours, a 40-hour assignment limit, staffing-shortage calculations, and employee selection logic using remaining target hours and hire date.

These algorithms provide building blocks for more advanced scheduling, rather than a complete automatic schedule generator.

### Enhancement 3 — Databases

Migrated the enhanced application to SQLite persistence for employees, availability, and scheduled shifts.

The CLI loads saved employees and reconstructs scheduled shifts at startup. Previously saved shifts are restored without reapplying the employee's current availability rules, while new assignments still receive availability and conflict checks.

## Original Artifact and Evolution

The original ShiftFlow V1 was a procedural Python CLI that tracked employees and availability using JSON.

The enhanced capstone implementation replaces that storage approach with SQLite and adds object-oriented scheduling models and algorithms.

Earlier versions may be available in the repository's Git history or branches, depending on what has been published.

## Current Limitations

- The interface is terminal-based; there is no web or mobile client.
- Shift swaps, employee self-service requests, approval notifications, and AI-generated schedules remain future work.
- Staffing requirements use a simple sales threshold helper rather than a configurable labor forecasting model.
- The CLI is intended as a capstone demonstration, not a production-ready multi-user scheduling service.

## Long-Term Vision (Beyond the Capstone)

ShiftFlow is intended to grow into a full mobile-friendly scheduling platform.

### Attendance Tracking

Record call-offs and no-shows per employee so managers can see patterns over time rather than relying on memory.

### Mobile-First Shift Swaps

An employee requests a shift change from their phone. Once another employee accepts, a notification goes out for approval to the general manager and the specific shift leader or manager scheduled to be in charge that day.

Once approved, the schedule updates automatically.

### AI-Assisted Scheduling

Introduce AI-assisted schedule creation and adjustments, reducing the time managers spend manually building and updating schedules.

### Sales-Tiered Staffing Coverage

Tie staffing requirements to projected sales using restaurant-specific rules.

For example, projected sales around $6,000–$7,000 may call for seven workers including the manager on duty, while sales around $4,000–$5,000 may call for six.

The system would also ensure a manager is present for opening and closing shifts.

These are proposed rules based on workplace experience, not features fully implemented in the current application.

### Structured Availability Input

Replace free-text availability entry with a calendar-style interface where managers can select days and times.

Potentially support importing availability from Excel exports.

The underlying employee availability methods are designed to remain independent of the future user interface.

### Sales-Based Labor Forecasting

Eventually incorporate projected sales to recommend staffing and labor adjustments.

This is a longer-term feature requiring additional sales data and forecasting logic.

### Gamified Employee Customization

Explore a more engaging experience through:

- Custom business branding and logos.
- Employee characters and avatars.
- Unlockable customization options.
- Monthly avatar outfits earned through transparent attendance points.

A proposed monthly attendance meter would reward punctuality while distinguishing advance-notice absences from short-notice absences and no-call/no-shows.

The system would use clear, explainable rules rather than random reward probabilities.

**Design consideration:** Gamification should remain respectful of employees and avoid punitive or shaming experiences.

This long-term vision is separate from the CS 499 capstone scope and represents the direction ShiftFlow may take as an independent software product.

## Author

Built by Allen Falcon, Computer Science student at Southern New Hampshire University, as an independent project and CS 499 capstone artifact.