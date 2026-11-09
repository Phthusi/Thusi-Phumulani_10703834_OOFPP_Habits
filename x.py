from colorama import Back, Style

table = '''| Command | Description | GIF |
| ------- | ----------- | --- |
| `run daily repeat pattern` | Repeats the copied habit for a specified number of days | [![Daily Repeat](../habit_repeats/media/repeat_daily.gif)](../habit_repeats/media/repeat_daily.gif) |
| `run weekly repeat pattern` | Repeats a selected week pattern for a specified number of weeks | [![Weekly Repeat](../habit_repeats/media/repeat_weekly.gif)](../habit_repeats/media/repeat_weekly.gif) |
| `run custom repeat pattern` | Creates a custom recurrence schedule using week, month, and multi-month patterns | [![Custom Repeat](../habit_repeats/media/repeat_custom.gif)](../habit_repeats/media/repeat_custom.gif) |
'''

table_list = table.split('\n')
table_list.pop(1)
table_first_row = [i.strip() for i in table_list[0].split('|') if i.strip()!='']
table_list = [i for i in table_list if i.strip()!='']
table_rows = list({i:[k.strip() for k in j.split('|') if k.strip()!=''] for i,j in enumerate(table_list[1:])}.values())
cleaned_rows = {i[0].replace('`',''):i[1:] for i in table_rows}

def match_content(word,cleaned_rows):
    print(f'➡️  {Style.BRIGHT+word.capitalize()} : {Style.NORMAL + cleaned_rows[word][0].capitalize()}')
    print(f'   {Style.BRIGHT}Press ctrl and click at this : { Style.NORMAL+ Back.LIGHTMAGENTA_EX + Style.BRIGHT + cleaned_rows[word][1].split('(')[1].replace(')','').replace(']','') + Back.BLACK + Style.NORMAL} to see the GIF')

match_content('run custom repeat pattern',cleaned_rows)