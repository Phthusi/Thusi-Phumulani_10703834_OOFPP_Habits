'''
longest streak
---------------------------
get all habit sessions
sort them by date
count=0
loop through each
if completed count+1
if not completed append count, 

remove all of the zeroes and find max, min,ave,std
'''

# from ...data.db_manager import CompleteHabit, Habits
# from ..ui.command_autocomplete import AutoCompleter

# class Analytics:
#     pass
from itertools import groupby

people = [
    ("John", "A"),
    ("Mary", "B"),
    ("Peter", "A"),
]

groupby_obj = groupby(people, key=lambda x: x[1])

current = ''
previous = 'a'
while current!=previous:
    previous = current
    try:
        current, items = next(groupby_obj)
    except Exception:
        previous=current
    print(current,items)
    print(list(items))