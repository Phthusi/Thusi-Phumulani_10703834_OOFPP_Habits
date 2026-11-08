>[Go back home](../../../Readme.md)

<!-- start-purpose -->
# Repeat Habit
The RepeatHabit component allows users to create recurring habit sessions from an existing habit session selected to be on the shelf and copied from the shelf.

The component supports several repetition modes:

- Daily — repeats a habit for a specified number of days.
- Weekly — repeats a selected week pattern for a specified number of weeks.
- Custom — allows the user to build a more complex recurrence schedule using week, month, and multi-month patterns.
- Monthly — currently under development.

Before a repeat operation can be performed, the user must first copy a habit session from the shelf.

The component uses a command-driven interaction loop, where each available command is mapped to a specific handler method.
<!-- end-purpose -->

---
<!-- start-table-of-content -->
## Table of Contents
- [Repeat Habit](#repeat-habit)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to Repeat a Habit](#steps-to-repeat-a-habit)
  - [Command Loop](#command-loop)
    - [Screen Views](#screen-views)
      - [Repeat Habit Screen Without a Habit on the Shelf](#repeat-habit-screen-without-a-habit-on-the-shelf)
      - [Repeat Habit Screen With a Habit on the Shelf but Not Copied](#repeat-habit-screen-with-a-habit-on-the-shelf-but-not-copied)
      - [Repeat Habit Screen With a Habit Copied from the Shelf](#repeat-habit-screen-with-a-habit-copied-from-the-shelf)
  - [Testing](#testing)
<!-- end-table-of-content -->

<!-- start-high-level-view -->
## [High-Level Flow](#table-of-contents)
### [Steps to Repeat a Habit](#table-of-contents)
1. ### [Search for a habit you want to repeat](./src/components/search_habits/Readme.md)
2. ### Copy the habit to the shelf
3. ### Choose a repeat type (daily, weekly, custom, or monthly)
4. ### Follow the on-screen instructions
<!-- end-high-level-view -->

## [Command Loop](#table-of-contents)

| Command | Description | GIF |
| ------- | ----------- | --- |
| `run daily repeat pattern` | Repeats the copied habit for a specified number of days | [![Daily Repeat](../habit_repeats/media/repeat_daily.gif)](../habit_repeats/media/repeat_daily.gif) |
| `run weekly repeat pattern` | Repeats a selected week pattern for a specified number of weeks | [![Weekly Repeat](../habit_repeats/media/repeat_weekly.gif)](../habit_repeats/media/repeat_weekly.gif) |
| `run custom repeat pattern` | Creates a custom recurrence schedule using week, month, and multi-month patterns | [![Custom Repeat](../habit_repeats/media/repeat_custom.gif)](../habit_repeats/media/repeat_custom.gif) |

The Repeat Habit command interface also supports common commands:

- `Esc` — exits the current Repeat Habit screen.
- `clear` — clears the terminal screen.
- `Space` — displays available commands.
- `↑ / ↓` — navigates through previously entered commands using command history.

---

### [Screen Views](#table-of-contents)
#### Repeat Habit Screen Without a Habit on the Shelf
[![Repeat Habit Image](../habit_repeats/media/repeat_without_copy.png)](../habit_repeats/media/repeat_without_copy.png)

#### Repeat Habit Screen With a Habit on the Shelf but Not Copied
[![Repeat Habit Image](../habit_repeats/media/repeat_select_habit_without_copy.png)](../habit_repeats/media/repeat_select_habit_without_copy.png)

#### Repeat Habit Screen With a Habit Copied from the Shelf
[![Repeat Habit Image](../habit_repeats/media/repeat_select_habit_with_copy.png)](../habit_repeats/media/repeat_select_habit_with_copy.png)

## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/repeat_habit/test
```

[⬆ Back to top](#top)
