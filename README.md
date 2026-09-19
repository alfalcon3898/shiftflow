# ShiftFlow

A command-line employee scheduling tool built in Python. ShiftFlow helps managers track employees, their roles, and their availability — replacing the paper, spreadsheets, and disconnected apps many small businesses still rely on.

## The Problem

As a manager, I've seen firsthand how much time gets lost building schedules by hand — time that could go toward actually training and supporting a team. I've also seen crew members miss shifts or struggle to request a shift swap simply because there was no easy system for it. ShiftFlow is being built to fix that, starting with the fundamentals: reliable employee and availability tracking, with real scheduling and conflict-detection logic planned as the project grows.

## Status

**Current development: Enhancement 1 — Software Design & Engineering**

ShiftFlow V1 is a functional, procedural Python CLI application preserved on the `main` branch. It manages employee records and availability using a local JSON file.

The `enhancement-1-oop` branch introduces three object-oriented classes:

* `Employee` — encapsulates employee information, validates names and roles, and manages availability.
* `Shift` — represents an assigned shift, validates date and time formats, and calculates shift duration.
* `Schedule` — manages a private collection of shifts through methods for adding, viewing, and removing shifts.

The refactored classes currently use in-memory list storage. This design keeps Enhancement 1 focused on object-oriented programming, encapsulation, validation, and testing.

**Testing:** 35 automated tests passed in the latest confirmed run.

The OOP classes are implemented, but integration with the original CLI and persistence has not yet been confirmed. Advanced scheduling algorithms and SQLite migration are reserved for later enhancements.


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

* **Language:** Python 3
* **Original application:** Procedural command-line interface (V1)
* **Enhancement 1 architecture:** Object-oriented design using `Employee`, `Shift`, and `Schedule` classes
* **Storage:** JSON file (`employees.json`) in V1; in-memory lists in the current OOP implementation
* **Testing:** `pytest`
* **Planned database:** SQLite (Enhancement 3)

## How to Run

### Run the original V1 application

1. Install Python 3.
2. Clone or download the repository.
3. Switch to the `main` branch.
4. Run the application:

```bash
python shiftflow.py
```

5. Follow the numbered command-line menu to manage employees and availability.

V1 saves employee data to `employees.json`.

### Review the OOP enhancement

Switch to the enhancement branch:

```bash
git switch enhancement-1-oop
```

The refactored implementation is organized into three Python files:

* `employee.py` — employee information, validation, and availability management.
* `shift.py` — shift information, date/time validation, and duration calculations.
* `schedule.py` — adding, retrieving, and removing shifts.

These classes currently provide the foundation for the scheduling system. A complete command-line interface for the refactored version has not yet been confirmed.

### Run the automated tests

From the project directory, install `pytest` if necessary:

```bash
python -m pip install pytest
```

Then run:

```bash
python -m pytest -q
```

The latest confirmed test run completed with **35 passing tests**.

The test suite covers the `Employee`, `Shift`, and `Schedule` classes, including validation, shift-duration calculations, collection management, and encapsulation.

## Known Limitations and Current Progress

### Original V1 limitations

The original version of ShiftFlow has several limitations that motivated the capstone enhancements:

* Employees are represented as dictionaries rather than objects.
* Input validation is limited, allowing malformed employee information to enter the system.
* There are no automated tests.
* The application tracks employee availability but does not represent assigned shifts.
* There is no scheduling conflict detection.
* Employee data is stored in a flat JSON file rather than a relational database.

### Improvements implemented in Enhancement 1

The object-oriented refactor addresses several of these limitations:

* Introduced separate `Employee`, `Shift`, and `Schedule` classes.
* Encapsulated employee information and shift collections using private attributes.
* Added validation for employee names, roles, shift dates, and time formats.
* Added methods for managing employee availability and scheduled shifts.
* Added shift-duration calculations, including overnight shifts.
* Added automated tests using `pytest`, with 35 tests passing in the latest confirmed run.
* Protected internal collections by returning copies from `Employee.get_availability()` and `Schedule.get_shifts()`.

The refactored classes currently use in-memory lists. Integration with the original command-line interface and persistent storage has not yet been confirmed.

Advanced scheduling algorithms and database functionality remain outside the current enhancement.

## Planned Enhancements

ShiftFlow is being developed through three capstone enhancement categories.

### Enhancement 1: Software Design & Engineering

**Status: Core OOP implementation completed; documentation and final review in progress.**

Refactor the original procedural application into an object-oriented design.

Implemented improvements include:

* `Employee`, `Shift`, and `Schedule` classes.
* Encapsulation through private attributes and public methods.
* Input validation and explicit error handling.
* Automated unit and integration tests using `pytest`.
* In-memory list storage to keep the initial design simple.

The current implementation provides a foundation for future scheduling functionality.

Remaining work includes final documentation, the enhancement narrative, and verification against the assignment rubric.

### Enhancement 2: Algorithms & Data Structures

**Status: Planned.**

Develop scheduling functionality using the object-oriented foundation established in Enhancement 1.

Planned features include:

* Detecting overlapping employee shifts.
* Checking staffing coverage.
* Tracking scheduled hours and identifying potential overtime.
* Supporting shift-swap requests.
* Distributing hours using employee preferences, seniority, and labor-budget constraints.

These features will introduce scheduling rules beyond the basic creation and management of shift objects.

### Enhancement 3: Databases

**Status: Planned.**

Replace flat-file and temporary in-memory storage with a relational database.

Planned improvements include:

* Migrating persistent data storage to SQLite.
* Designing normalized tables for employees, shifts, roles, and availability.
* Introducing a database access layer.
* Supporting reliable storage and retrieval of employee and scheduling information.

The database enhancement will build on the object-oriented architecture developed in Enhancement 1.

## Long-Term Vision (Beyond the Capstone)

Once the core rebuild above is complete, ShiftFlow is intended to grow into a full mobile-friendly scheduling platform:

- **Attendance tracking** — record call-offs and no-shows per employee, so managers can see patterns over time (e.g., how many times a given worker has called off) rather than relying on memory.
- **Shift-swap requests, mobile-first** — an employee requests a shift change from their phone; once another employee accepts, a notification goes out for approval to the GM (always notified), plus the specific shift leader/mod who is actually scheduled to be in charge that day — not every mod, just the one on duty, so people aren't bothered about shifts they have nothing to do with. Once approved, the schedule updates automatically.
- **AI-assisted scheduling** — the schedule itself adjusts automatically as shift-swap requests are approved, rather than requiring a manager to manually rebuild it.
- **Sales-tiered staffing coverage (concrete, near-term idea — closer than the sales-forecasting idea below):** coverage checking that ties total staffing to predicted sales, based on real staffing rules observed at work — a MOD (manager on duty) must always be present to open/close; predicted sales around $6-7K call for 7 total workers including the MOD; predicted sales around $4-5K call for 6 total workers including the MOD; the GM doesn't count toward these numbers. This is more concrete and closer-term than full sales forecasting, and could realistically become part of the Algorithms & Data Structures enhancement rather than staying a "someday" feature.
- **Structured availability input:** long-term goal is a dropdown/calendar-style UI for managers to select availability, rather than free-typing it, to keep bad/inconsistent data from entering the system — with an option to also import availability data from an Excel export, matching how the workplace's current scheduling process already works. The underlying data layer (e.g. `Employee.add_availability()`) is intentionally built to be UI-agnostic, so it doesn't matter whether the input eventually comes from typing, a dropdown, or an Excel import — no rewrite needed as the interface evolves.
- **Sales-based labor forecasting (later idea, not near-term):** the schedule could incorporate projected sales data (e.g., food sales) to recommend labor adjustments — flagging when a slow projected sales period suggests cutting hours/staff, or a busy projected period suggests adding coverage. This would tie labor costs directly to expected revenue instead of scheduling purely on availability/fairness, closer to how real restaurant/retail labor budgeting actually works. This is a significant addition (would need a sales-data source and forecasting logic) and is explicitly a "someday" idea, not scoped into V3/V4.
- **Gamified customization** — a lighter, more engaging layer on top of the core tool:
  - Each business can apply its own branding/logo with a fun, customized style (e.g., a company's logo reimagined in a friendly, stylized way).
  - Each employee gets a customizable character/avatar.
  - Employees unlock new customization options for their character by showing up on time and maintaining good attendance — turning a basic scheduling need into something more engaging to actually use.
  - **Monthly outfit mechanic (attendance meter, points-based):** each month features a limited-time avatar outfit, unlocked by reaching a visible attendance-points threshold (e.g., 100 points) by month's end. On-time shifts worked add points; violations subtract them, scaled by severity — an advance-notice call-off costs little to nothing (normal, expected process), a short-notice call-off costs a moderate amount, a no-call/no-show costs the most, and lateness scales with how late. The meter resets each month, keeping the incentive ongoing rather than a one-time reward.
  - **Why points instead of odds:** an earlier design considered a probability-based unlock (attendance affecting the *chance* of earning the outfit), but that risked feeling like a hidden "black box" and eroding trust. A visible points meter is fully transparent — every point change is a direct, explainable consequence, formula-based and consistent for every employee, so nothing can look manually tweaked or unfair.
  - **Design caution:** penalties should read as "progress paused," not punitive or shame-based — a fun system can backfire fast if it starts to feel demeaning to real employees doing real jobs.

This long-term vision is separate from the CS 499 capstone scope (which focuses on the three enhancement categories above) but represents the direction the project is headed as a personal/SaaS product afterward.

## Author

Built by Allen Falcon, Computer Science student at Southern New Hampshire University, as an independent project and CS 499 capstone artifact.
