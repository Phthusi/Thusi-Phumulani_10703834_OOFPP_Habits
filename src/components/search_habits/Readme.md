> [Go back home](../../../Readme.md)
 
## Quick Links
[Go to update habit](/src/components/update_habit/Readme.md)

[Go to delete habit](/src/components/delete_habit/Readme.md)

[Go to repeat habit](/src/components/habit_repeats/Readme.md)

# Search Habit

<!-- start-purpose -->
## Search Component Purpose

The **Search Habit Component** component provides functionality to **search for habits** based on various criteria.
<!-- end-purpose -->
Gifs can be used to illustrate steps for the user in action.

---
<!-- start-table-of-content -->
## Table of Contents
- [Search Habit](#search-habit)
  - [Search Component Purpose](#search-component-purpose)
  - [Table of Contents](#table-of-contents)
  - [High-Level Flow](#high-level-flow)
    - [Steps to search for a habit or habits](#steps-to-search-for-a-habit-or-habits)
      - [search for a habit session](#search-for-a-habit-session)
      - [search and complete a habit session](#search-and-complete-a-habit-session)
  - [Testing](#testing)
<!-- end-table-of-content -->

<!-- start-high-level-view -->
## [High-Level Flow](#table-of-contents)

### [Steps to search for a habit or habits](#table-of-contents)
  1.  ### Search for the habit(s) you want based on the criteria of your choice.
  2.  ### Select the habit so that it can be acted on.
<!-- end-high-level-view -->
  Gif example of the high level flow:
  #### search for a habit session
  [![Search Habit Flow](../search_habits/media/search_habit.gif)](../search_habits/media/search_habit.gif)
                          
                                              OR

  #### search and complete a habit session
  [![Search and Complete Habit Flow](../update_habit/media/habit_to_complete.gif)](../update_habit/media/habit_to_complete.gif)
  
- Go back to the home screen (select esc)
- Clear the screen(select clear)
- get help(select help)

---
## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/search_habit/test
```
[⬆ Back to top](#top)