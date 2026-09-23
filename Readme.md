# Habit Tracker

[![Habit Image](./media/habit_tracker_image.png)](./media/habit_tracker_image.png)

## Project Purpose
This **Habit Tracker** is a command-line interface (CLI) application designed to help users:

* Track habits with start times, durations, and descriptions.
* Set repeat patterns for habits on a weekly and monthly basis.
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



### [Testing](#table-of-content)

Run the complete automated test suite with:

```bash
python -m unittest discover -s src -p "test*.py" -v
```

The tests cover the habit model and validation, datetime calculations, scheduling/clash detection, SQLite CRUD operations, collection queries, and functional analytics.


For normal development and testing, keep fixture loading separate from the automated test database.

### [Run](#table-of-content)

From the project root:

```bash
python run.py
```

### [Loading the predefined fixtures](#table-of-content)
The application stores sessions in `habit.db`. A separate SQLite file can be supplied when using the persistence classes directly, which is useful for tests.

The project includes five predefined habits and four weeks of example tracking data in `fixtures/habits_fixture.json`. To load them into the default database:

```bash
python seed_fixtures.py
```
[⬆ Back to top](#top)