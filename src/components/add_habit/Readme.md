>[Go back home](../../../Readme.md)

# Add Habit

<!-- start-purpose -->
## Add Component Purpose
The Add Habit component is responsible for guiding the user through creating a new habit in the command-line interface.

It collects all required habit fields, validates user input, and then saves the habit.

This component follows a command-driven interaction loop, where each user action is mapped to an appropriate method.
<!-- end-purpose -->

GIFs can be used to illustrate each step of the process.

---
<!-- start-table-of-content -->
## Table of Contents
- [Add Habit](#add-habit)
  - [Add Component Purpose](#add-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to Create a Habit](#steps-to-create-a-habit)
    - [Screen Views](#screen-views)
    - [Here are the features we have:](#here-are-the-features-we-have)
      - [Note: For information about how the form changes as you fill it in, please look at the GIFs below. Also, you cannot be locked to any level after filling in everything in level 1.](#note-for-information-about-how-the-form-changes-as-you-fill-it-in-please-look-at-the-gifs-below-also-you-cannot-be-locked-to-any-level-after-filling-in-everything-in-level-1)
  - [Command Loop](#command-loop)
  - [Testing](#testing)
<!-- end-table-of-content -->

<!-- start-high-level-view -->
## [High-Level Flow](#table-of-contents)
### [Steps to Create a Habit](#table-of-contents)
1. ### User enters the Add Habit screen
2. ### Enters field values
   - Enter name
   - Enter start datetime
   - Enter session duration
3. ### Saves the habit
   - Save the habit
<!-- end-high-level-view -->

GIF example of the high-level flow:

[![Add Habit Flow](../add_habit/media/add_habit.gif)](../add_habit/media/add_habit.gif)
- Go back to the home screen (press `Esc`)
- Clear the screen (press `clear`)
- Get help (press `help`)

---
### [Screen Views](#table-of-contents)
[![Add Habit Image](../add_habit/media/add_habit.png)](../add_habit/media/add_habit.png)

### Here are the features we have:
- #### Completion bar

  This is used to show the progress of filling in the required fields.

  [![Progress Bar](../add_habit/media/progress_bar.png)](../add_habit/media/progress_bar.png)

- #### Fields and Levels

  There are different levels and fields. There is a level one on the left and a level two. The padlock at level two means that the save action is locked. If you fill in all the required fields in level one, then the save action can be unlocked.

  [![Progress Bar](../add_habit/media/key_fields.png)](../add_habit/media/key_fields.png)

#### Note: For information about how the form changes as you fill it in, please look at the GIFs below. Also, you cannot be locked to any level after filling in everything in level 1.

## [Command Loop](#table-of-contents)

Available commands:

| Command | Description | Format or Rule(s) | GIF |
| ------- | ----------- | ------------------ | --- |
| `name` | Sets the habit name | Name is required and must be more than 3 characters | [![Set Name](../add_habit/media/enter_name.gif)](../add_habit/media/enter_name.gif) |
| `start_datetime` | Sets the start date and time | `YYYY-MM-DD HH:MM:SS`, for example `2026-11-28 13:30:00` | [![Start Date](../add_habit/media/enter_datetime.gif)](../add_habit/media/enter_datetime.gif) |
| `duration` | Sets the session duration | `HH:MM:SS`, for example `13:30:00` | [![Session Duration](../add_habit/media/enter_duration.gif)](../add_habit/media/enter_duration.gif) |

Each command maps directly to a handler method.

---
## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/add_habit/test
```

[⬆ Back to top](#top)
