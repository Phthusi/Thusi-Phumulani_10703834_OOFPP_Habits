>[Go back home](../../../Readme.md)

# Repeat Habit


## Repeat Component Purpose


The **DeleteHabitController** component allows users to safely delete a habit from the database via the command-line interface.
 
It ensures:

* Habit exists before deletion
* Reflections and descriptions are preserved until deletion
* User confirmation before removing

This component follows a **command-driven interaction loop**, where each user action is mapped to appropriate methods.

Gifs can be used to illustrate steps for the user in action.

---

## Table of Contents
- [Repeat Habit](#repeat-habit)
  - [Repeat Component Purpose](#repeat-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Screen views](#screen-views)
      - [Repeat habit screen without grabbing any habit](#repeat-habit-screen-without-grabbing-any-habit)
      - [Repeat habit screen view with grabbed any habit but didn't copy it from the shelf](#repeat-habit-screen-view-with-grabbed-any-habit-but-didnt-copy-it-from-the-shelf)
      - [Repeat habit screen view with grabbed any habit copied from the shelf](#repeat-habit-screen-view-with-grabbed-any-habit-copied-from-the-shelf)
    - [Steps to delete a habit](#steps-to-delete-a-habit)
  - [Testing](#testing)

  
## [High-Level Flow](#table-of-contents)
### [Screen views](#table-of-contents) 
  #### Repeat habit screen without grabbing any habit
  ![Add Habit Image](../delete_habit/media/delete_habit.png)

  #### Repeat habit screen view with grabbed any habit but didn't copy it from the shelf
  ![Add Habit Image](../delete_habit/media/habit_on_shelf_not_copied.png)

  #### Repeat habit screen view with grabbed any habit copied from the shelf
  ![Add Habit Image](../delete_habit/media/copied_habit_on_shelf_.png)

### [Steps to delete a habit](#table-of-contents)
  1.  ### [Search for a habit you want to delete](/src/components/search_habits/Readme.md)
  2.  ### Copy habit to the shelf
  3.  ### Repeat habit

  Gif example of the high level flow:

  ![Add Habit Flow](../delete_habit/media/delete_habit.gif)
- Go back to the home screen (select esc)
- Clear the screen(select clear)
- get help(select help)
---

## [Command Loop](#table-of-contents)


Available commands:

| Command                      | Description                  | format or rule(s)         | Gif                                           |
| ---------------------------- | -----------------------------| ---------------------------------------------  | --------------------------------------------- |
| `name`             | Sets the habit name        | name is required and must have more than 3 characters          | [![Set Name](../add_habit/media/enter_name.gif)](../add_habit/media/enter_name.gif)        |
| `start_datetime`         | Sets the start date and time| YYYY-MM-DD HH:MM:SS e.g 2026-11-28 13:30:00  | [![Start Date](../add_habit/media/enter_datetime.gif)](../add_habit/media/enter_datetime.gif)  |
| `duration` | Sets the session duration     |HH:MM:SS e.g 13:30:00   | [![Session Duration](../add_habit/media/enter_duration.gif)](../add_habit/media/enter_duration.gif)  |

Each command maps directly to a handler method.

---

## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/delete_habit/test
```
[⬆ Back to top](#top)