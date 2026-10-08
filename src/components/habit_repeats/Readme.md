>[Go back home](../../../Readme.md)

# Repeat Habit

  The RepeatHabit component allows users to create recurring habit sessions from an existing habit session selected to be on the shelf and copied from the Shelf.

  The component supports several repetition modes:

  Daily — repeats a habit for a specified number of days.
  Weekly — repeats a selected week pattern for a specified number of weeks.
  Custom — allows the user to build a more complex recurrence schedule using week, month, and multi-month patterns.
  Monthly — currently under development.

  Before a repeat operation can be performed, the user must first copy a habit session from the Shelf.

  The component uses a command-driven interaction loop, where each available command is mapped to a specific handler method.

---

## Table of Contents
- [Repeat Habit](#repeat-habit)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to Repeatt a habit](#steps-to-repeatt-a-habit)
  - [Command Loop](#command-loop)
    - [Screen views](#screen-views)
      - [Repeat habit screen without grabbing any habit or any habit on the shelf](#repeat-habit-screen-without-grabbing-any-habit-or-any-habit-on-the-shelf)
      - [Repeat habit screen view with grabbed any habit but didn't copy it from the shelf](#repeat-habit-screen-view-with-grabbed-any-habit-but-didnt-copy-it-from-the-shelf)
      - [Repeat habit screen view with grabbed any habit copied from the shelf](#repeat-habit-screen-view-with-grabbed-any-habit-copied-from-the-shelf)
  - [Testing](#testing)

  
## [High-Level Flow](#table-of-contents)
### [Steps to Repeatt a habit](#table-of-contents)
  1.  ### [Search for a habit you want to delete](/src/components/search_habits/Readme.md)
  2.  ### Copy habit to the shelf
  3.  ### Choose a repeat type(daily, monthly etc)
  4. ### Follow instructions there

## [Command Loop](#table-of-contents)


| Command                      | Description                  | Gif                                           |
| ---------------------------- | -----------------------------| --------------------------------------------- |
| `run daily repeat pattern`             | Repeats the copied habit for a specified number of days       |  [![daily repeat](../habit_repeats/media/repeat_daily.gif)](../habit_repeats/media/repeat_daily.gif)        |
| `run weekly repeat pattern`         | .Repeats a selected week pattern for a specified number of weeks.|  [![weekly repeat](../habit_repeats/media/repeat_weekly.gif)](../habit_repeats/media/repeat_weekly.gif)  |
| `run custom repeat pattern` | Creates a custom recurrence schedule using week, month, and multi-month patterns.     | [![Session Duration](../habit_repeats/media/repeat_custom.gif)](../habit_repeats/media/repeat_custom.gif)  |


`The Repeat Habit command interface also supports common commands:`

  - esc   —  exits the current Repeat Habit screen.

  - clear  —  clears the terminal screen.

  - Space  —  displays available commands.

  - ↑ / ↓ — navigates through previously entered commands using command history.

---

### [Screen views](#table-of-contents) 
  #### Repeat habit screen without grabbing any habit or any habit on the shelf
  [![Repeat Habit Image](../habit_repeats/media/repeat_without_copy.png)](../habit_repeats/media/repeat_without_copy.png)

  #### Repeat habit screen view with grabbed any habit but didn't copy it from the shelf
  [![Repeat Habit Image](../habit_repeats/media/repeat_select_habit_without_copy.png)](../habit_repeats/media/repeat_select_habit_without_copy.png)

  #### Repeat habit screen view with grabbed any habit copied from the shelf
  ![Repeat Habit Image](../habit_repeats/media/repeat_select_habit_with_copy.png)


## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/repeat_habit/test
```
[⬆ Back to top](#top)