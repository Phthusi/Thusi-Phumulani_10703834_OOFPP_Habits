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
  - [Search Filters](#search-filters)
    - [Filter overview](#filter-overview)
    - [Date filters](#date-filters)
    - [Time filters](#time-filters)
    - [Duration filters](#duration-filters)
    - [Name filters](#name-filters)
    - [Status and completion filters](#status-and-completion-filters)
    - [Input and navigation tips](#input-and-navigation-tips)
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

## Search Filters

From the search screen, choose **get habit(s)**, then choose one filter category. Each filter runs its own search and displays the matching habit sessions. The current menus do not combine multiple filters into one query.

### Filter overview

| Filter category | Available options | What it matches |
| --- | --- | --- |
| `date` | `before`, `after`, `on` | Sessions scheduled before, after, or on a calendar date. |
| `time` | `before`, `after`, `on` | Sessions scheduled before, after, or at a clock time. |
| `duration` | `less than`, `greater than`, `on` | Session durations shorter than, longer than, or equal to a duration. |
| `name` | `is`, `has` | Habit names that exactly match a value or contain it. |
| `status` | `MISSED`, `ONGOING`, `UPCOMING` | Sessions with the selected status. |
| `habit to complete` | No additional input | Sessions awaiting completion confirmation (`TO_BE_CONFIRMED`). |

### Date filters

| Option | Result | Input format | Example |
| --- | --- | --- | --- |
| `before` | Sessions with a scheduled date earlier than the entered date. The selected date itself is excluded. | `YYYY-MM-DD` | `2026-06-30` |
| `after` | Sessions with a scheduled date later than the entered date. The selected date itself is excluded. | `YYYY-MM-DD` | `2026-06-30` |
| `on` | Sessions scheduled on the exact entered date. | `YYYY-MM-DD` | `2026-06-30` |

### Time filters

| Option | Result | Input format | Example |
| --- | --- | --- | --- |
| `before` | Sessions whose scheduled clock time is earlier than the entered time. The entered time itself is excluded. | `HH:MM:SS` | `15:30:45` |
| `after` | Sessions whose scheduled clock time is later than the entered time. The entered time itself is excluded. | `HH:MM:SS` | `20:18:50` |
| `on` | Sessions scheduled at exactly the entered clock time. | `HH:MM:SS` | `04:15:09` |

Time searches compare the time-of-day component and do not filter by date.

### Duration filters

| Option | Result | Input format | Example |
| --- | --- | --- | --- |
| `less than` | Sessions with a duration shorter than the entered duration. | `HH:MM:SS` | `01:15:40` |
| `greater than` | Sessions with a duration longer than the entered duration. | `HH:MM:SS` | `05:37:48` |
| `on` | Sessions whose duration exactly equals the entered duration. | `HH:MM:SS` | `01:15:40` |

The `before`/`after` date and time options and the `less than`/`greater than` duration options use strict comparisons, so an exact match is not included in those results.

### Name filters

| Option | Result | Example input | Example match |
| --- | --- | --- | --- |
| `is` | Matches the complete habit name exactly. | `Read` | Habit named `Read` |
| `has` | Matches habit names containing the entered text. | `read` | A habit name containing the exact substring `read` |

Name matching is case-sensitive: the search uses the supplied text without converting the stored name or search term to a common case.

### Status and completion filters

| Option | Matches |
| --- | --- |
| `MISSED` | Sessions whose status is `MISSED`. |
| `ONGOING` | Sessions whose status is `ONGOING`. |
| `UPCOMING` | Sessions whose status is `UPCOMING`. |
| `habit to complete` | Sessions marked `TO_BE_CONFIRMED`, meaning they are waiting for the user to confirm completion. |

The status menu accepts the three displayed status values without regard to the case typed; the input is converted to uppercase before the search. `TO_BE_CONFIRMED` is available through **habit to complete**, rather than the regular status menu.

### Input and navigation tips

- Dates must use `YYYY-MM-DD`; times and durations must use `HH:MM:SS` (24-hour clock for times).
- Invalid date, time, or duration formats are rejected by input validation.
- Use **Space** to display available menu choices, **Enter** to select, and **Esc** to leave a submenu.
- Search results can be selected and placed on the shelf for other actions. Choose **view selected habit** to inspect the currently selected session.

---
## [Testing](#table-of-contents)
```bash
python -m unittest discover -s src/components/search_habit/test
```
[⬆ Back to top](#top)
