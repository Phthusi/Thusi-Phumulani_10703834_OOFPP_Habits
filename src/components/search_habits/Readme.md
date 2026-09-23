> [Go back home](../../../Readme.md)
 
## Quick Links
[Go to update habit](/src/components/update_habit/Readme.md)

[Go to delete habit](/src/components/delete_habit/Readme.md)

[Go to repeat habit](/src/components/habit_repeats/Readme.md)

# Search Habit


## Search Component Purpose


The **Search Habit Component** component provides functionality to **search for habits** based on various criteria.

Gifs can be used to illustrate steps for the user in action.

---

## Table of Contents
- [Search Habit](#search-habit)
  - [Search Component Purpose](#search-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to search for a habit or habits](#steps-to-search-for-a-habit-or-habits)
  - [Command Loop](#command-loop)
  - [Testing](#testing)

  
## [High-Level Flow](#table-of-contents)

### [Steps to search for a habit or habits](#table-of-contents)
  1.  ### Search for the habit(s) you want based on the criteria of your choice.
  2.  ### Select the habit so that it can be acted on.

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
python -m unittest discover -s src/components/search_habit/test
```
[⬆ Back to top](#top)