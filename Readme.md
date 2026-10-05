# Habit Tracker

[![Habit Image](./media/habit_tracker_image.png)](./media/habit_tracker_image.png)

## Project Purpose
This **Habit Tracker** is a command-line interface (CLI) application designed to help users:

* Track habits with start times, durations, and periodicities.
* Set repeat patterns for habits on a daily and weekly basis.
* Automatically update habit statuses based on time and activity.
* Search, update, and delete habits efficiently.

It’s a lightweight but fully featured system for building **consistency, accountability, and growth tracking**.
## Table of content
- [Habit Tracker](#habit-tracker)
  - [Project Purpose](#project-purpose)
  - [Table of content](#table-of-content)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Testing](#testing)
    - [Run](#run)
    - [Loading the predefined fixtures](#loading-the-predefined-fixtures)
    - [Core Concepts & Time Units](#core-concepts--time-units)
    - [Add habit](/src/components/add_habit/Readme.md)
    - [Delete habit](/src/components/delete_habit/Readme.md)
    - [Update habit](/src/components/update_habit/Readme.md)
    - [Search habit](/src/components/search_habits/Readme.md)
    - [Habit repeats](/src/components/habit_repeats/Readme.md)
    
  
A Python habit-tracking backend/CLI using object-oriented modelling, SQLite persistence, functional analytics, and a command-line interface.

### [Requirements](#table-of-content)

- Python 3.7+ (Python 3.10+ is recommended because the project uses structural pattern matching in the CLI.)
- Dependencies in `requirements.txt`

### [Installation](#table-of-content)

```bash
python -m pip install -r requirements.txt
```
[![Requirements](./media/requirements.gif)](./media/requirements.gif)
---


### [Testing](#table-of-content)

Run the complete automated test suite with:

```bash
python -m unittest discover -s src -p "test*.py" -v
```
[![Press Space](./media/run_tests.gif)](./media/press_space.gif)

The tests cover the habit model and validation, datetime calculations, scheduling/clash detection, SQLite CRUD operations, collection queries, and functional analytics.


For normal development and testing, keep fixture loading separate from the automated test database.
---
### [Run](#table-of-content)

From the project root:

```bash
python run.py
```
[![Run program](./media/run_program.gif)](./media/run_program.gif)
---
### [Loading the predefined fixtures](#table-of-content)
The application stores sessions in `habit.db`. A separate SQLite file can be supplied when using the persistence classes directly, which is useful for tests.

The project includes five predefined habits and four weeks of example tracking data in `fixtures/habits_fixture.json`. To load them into the default database:

```bash
python seed_fixtures.py
```
----
### [Core Concepts & Time Units](#table-of-content)
- #### Time Scale Definitions:

  - 1 Week: Defined as 7 days.

  - 1 Month: Defined as 4 weeks (28 days).

- #### Session Creation: 
  All workflows originate by adding an initial habit session. Parameters pass through HabitValidator and clash check routines before being persisted to habit.db.

- ##### The Active "Shelf": 
  Upon creation or selection, the active session is loaded into the Shelf state (Shelf.preserve_habit()).

- #### Downstream Operations:

  - Repeat Habits: Uses the session held on the Shelf to calculate future recurrences using HabitDateTimeManager (stepping by 7 days for weekly repeats, or 28 days for monthly repeats).

  - Update & Delete: Modifies or purges the staged shelf session across both SQLite database storage and local cache.

---
### 💡 Pro Tips:

Instant Command Menu: Press Space at any screen or menu stage to pull up all available commands and keyboard shortcuts.

example
[![Press Space](./media/press_space.gif)](./media/press_space.gif)

[⬆ Back to top](#top)