>[Go back home](../../../Readme.md)

# Delete Habit

<!-- start-purpose -->
## Delete Component Purpose

The **DeleteHabitController** component allows users to safely delete a habit from the database via the command-line interface.

It ensures:

* Habit exists before deletion
* Reflections and descriptions are preserved until deletion
* User confirmation before removing

This component follows a **command-driven interaction loop**, where each user action is mapped to appropriate methods.
<!-- end-purpose -->

Gifs can be used to illustrate steps for the user in action.

---
<!-- start-table-of-content -->
## Table of Contents
- [Delete Habit](#delete-habit)
  - [Delete Component Purpose](#delete-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to delete a habit](#steps-to-delete-a-habit)
    - [Screen views](#screen-views)
      - [Elements of the delete screen:](#elements-of-the-delete-screen)
      - [Delete habit screen without grabbing any habit](#delete-habit-screen-without-grabbing-any-habit)
      - [Delete habit screen view with grabbed any habit but didn't copy it from the shelf](#delete-habit-screen-view-with-grabbed-any-habit-but-didnt-copy-it-from-the-shelf)
      - [Delete habit screen view with grabbed any habit copied from the shelf](#delete-habit-screen-view-with-grabbed-any-habit-copied-from-the-shelf)
  - [Testing](#testing)
<!-- end-table-of-content -->

---
<!-- start-high-level-view -->
## [High-Level Flow](#table-of-contents)
### [Steps to delete a habit](#table-of-contents)
  1.  ### [Search for a habit you want to delete](/src/components/search_habits/Readme.md)
  2.  ### Copy habit to the shelf
  3.  ### Delete habit
<!-- end-high-level-view -->

  Gif example of the high level flow:

  [![Add Habit Flow](../delete_habit/media/delete_habit.gif)](../delete_habit/media/delete_habit.gif)
- Go back to the home screen (select esc)
- Clear the screen(select clear)
- get help(select help)

---
### [Screen views](#table-of-contents)
  The Delete screen is made up of what I call the elements of the delete screen. They are explained and shown below. `Please refer to gifs to see how the elements of the delete screen  change in different circumstances.`

  #### Elements of the delete screen:

  - #### The Shelf: 
    This is where we put the habit session so that it be can be accessed to update,delete, complete etc. The picture shown below shows if the shelf has a habit session or not. Please note the shelf can only have 1 habit session.
    
    [![Delete Habit Shelf Image](../delete_habit/media/deletes_shelf.png)](../delete_habit/media/deletes_shelf.png)

  - #### The Status: 
    This is where we see if the habit has been copied from the shelf or not.

    [![Delete Habit Status Image](../delete_habit/media/deletes_status.png)](../delete_habit/media/deletes_status.png)

  - #### The Habit Id:
    This is where you see the habit ID of the habit session that has been copied from the shelf.
    
    [![Delete Habit Id Image](../delete_habit/media/deletes_habit_id.png)](../delete_habit/media/deletes_habit_id.png)

  #### Delete habit screen without grabbing any habit
  [![Delete Habit Image](../delete_habit/media/delete_habit.png)](../delete_habit/media/delete_habit.png)

  #### Delete habit screen view with grabbed any habit but didn't copy it from the shelf
  [![Delete Habit Image](../delete_habit/media/habit_on_shelf_not_copied.png)](../delete_habit/media/habit_on_shelf_not_copied.png)

  #### Delete habit screen view with grabbed any habit copied from the shelf
  [![Delete Habit Image](../delete_habit/media/copied_habit_on_shelf_.png)](../delete_habit/media/copied_habit_on_shelf_.png)

---

## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/delete_habit/test
```
[⬆ Back to top](#top)