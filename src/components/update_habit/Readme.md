>[Go back home](../../../Readme.md)

# Update Habit

<!-- start-purpose -->
## Update Component Purpose

The **Update Habit Component** component allows users to update, complete, and view habits in the command-line interface.

It provides functionality to:

* Update habit details
* Mark tasks as completed
* Update habit statuses based on start time and duration
* View individual or multiple habits

The component follows a **command-driven loop**, where each command maps to a handler method.
<!-- end-purpose -->

Gifs can be used to illustrate steps for the user in action.

---

<!-- start-table-of-content -->
## Table of Contents
- [Update Habit](#update-habit)
  - [Update Component Purpose](#update-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to update a habit](#steps-to-update-a-habit)
      - [update a habit session](#update-a-habit-session)
      - [search and complete a habit session](#search-and-complete-a-habit-session)
    - [Screen views](#screen-views)
      - [Elements of the update screen:](#elements-of-the-update-screen)
      - [Update habit screen without grabbing any habit](#update-habit-screen-without-grabbing-any-habit)
      - [Update habit screen view with grabbed any habit but didn't copy it from the shelf](#update-habit-screen-view-with-grabbed-any-habit-but-didnt-copy-it-from-the-shelf)
      - [Update habit screen view with grabbed any habit copied from the shelf](#update-habit-screen-view-with-grabbed-any-habit-copied-from-the-shelf)
  - [Testing](#testing)
<!-- end-table-of-content -->

<!-- start-high-level-view -->
## [High-Level Flow](#table-of-contents)

### [Steps to update a habit](#table-of-contents)
  1.  ### [Search for a habit you want to update or Complete](/src/components/search_habits/Readme.md)
  2.  ### Copy habit to the shelf
  3.  ### Update habit
<!-- end-high-level-view -->

  Gif example of the high level flow:
  #### update a habit session
  [![Update Habit Flow](../update_habit/media/update_habit.gif)](../update_habit/media/update_habit.gif)

                                          OR
  #### search and complete a habit session
  [![Complete Habit Session Flow](../update_habit/media/habit_to_complete.gif)](../update_habit/media/habit_to_complete.gif)


- Go back to the home screen (select esc)
- Clear the screen(select clear)
- get help(select help)

---
### [Screen views](#table-of-contents)
  The Update screen is made up of what I call the elements of the update screen. They are explained and shown below. `Please refer to gifs to see how the elements of the update screen  change in different circumstances.`

  #### Elements of the update screen:

  - #### The Shelf: 
    This is where we put the habit session so that it be can be accessed to update,delete, complete etc. The picture shown below shows if the shelf has a habit session or not. Please note the shelf can only have 1 habit session.
    
    [![Update Habit Shelf Image](../delete_habit/media/deletes_shelf.png)](../delete_habit/media/deletes_shelf.png)

  - #### The Status: 
    This is where we see if the habit has been copied from the shelf or not.

    [![Update Habit Status Image](../delete_habit/media/deletes_status.png)](../delete_habit/media/deletes_status.png)

  - #### The Habit Id:
    This is where you see the habit ID of the habit session that has been copied from the shelf.
    
    [![Delete Habit Id Image](../delete_habit/media/deletes_habit_id.png)](../delete_habit/media/deletes_habit_id.png)
    
  #### Update habit screen without grabbing any habit
  [![Update Habit Image](../update_habit/media/update_habit_empty_shelf.png)](../update_habit/media/update_habit_empty_shelf.png)

  #### Update habit screen view with grabbed any habit but didn't copy it from the shelf
  [![Update Habit Image](../update_habit/media/update_habit_not_copied_from_shelf.png)](../update_habit/media/update_habit_not_copied_from_shelf.png)

  #### Update habit screen view with grabbed any habit copied from the shelf
  [![Update Habit Image](../update_habit/media/update_habit_copied_from_shelf.png)](../update_habit/media/update_habit_copied_from_shelf.png)

## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/update_habit/test
```
[⬆ Back to top](#top)