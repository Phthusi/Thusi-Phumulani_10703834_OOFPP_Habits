from ...data.db_manager import Habits
from colorama import Fore, Back, Style
from ..ui.terminal_utils import clear_screen
from ..time_project.time_manager import HabitDateTimeManager
from rich.table import Table
from rich.text import Text
from rich.console import Console

class Analytics:

    @classmethod
    def find_statuses(cls):
        sorted_habits = list(sorted(Habits().get_habits(), key=lambda habit: habit[2]))
        sorted_statuses = [habit[4] for habit in sorted_habits if habit[4] in ['MISSED', 'COMPLETED']]
        return sorted_habits, sorted_statuses

    @classmethod
    def long_streak_duration_ave(cls):
        habit_date_time_manager = HabitDateTimeManager()
        streaks_totals, streak_habits = cls.streaks_calculator()
        
        streak_habits = [sh for sh in streak_habits if sh]
        if not streak_habits:
            return 'N/A'

        max_index = streaks_totals.index(max(streaks_totals)) if streaks_totals else 0
        target_streak = streak_habits[max_index] if max_index < len(streak_habits) else streak_habits[0]

        if not target_streak:
            return 'N/A'

        duration_list = list(map(lambda habit: habit_date_time_manager.convert_duration(habit[3]), target_streak))
        start = habit_date_time_manager.convert_duration('00:00:00')
        total_streak_duration = sum(duration_list, start=start)
        average_duration = f'{total_streak_duration / len(target_streak)}'
        
        hours, minutes, seconds = average_duration.split(':')
        result = ''
        result += '' if hours in ('0', '00') else f'{hours} Hrs'
        mins_str = f'{minutes} mins' if result == '' else f',{minutes} mins'
        result += '' if minutes in ('0', '00') else mins_str
        return result if result else '0 mins'

    @classmethod
    def streaks_calculator(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        count = 0
        streaks_totals = []
        streak_habits = []
        temporary_streak_habits = []
        
        for status, habit in zip(sorted_statuses, sorted_habits):
            if status == 'COMPLETED':
                count += 1
                temporary_streak_habits.append(habit)
            else:
                if count > 0:
                    streaks_totals.append(count)
                    streak_habits.append(temporary_streak_habits)
                temporary_streak_habits = []
                count = 0
                
        # Catch any trailing active streak at the end of the list
        if count > 0:
            streaks_totals.append(count)
            streak_habits.append(temporary_streak_habits)

        return streaks_totals, streak_habits

    @classmethod
    def longest_streak(cls):
        totals, _ = cls.streaks_calculator()
        if not totals:
            return '0 days'
        return f'{max(totals)} days'

    @classmethod
    def current_streak(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        count = 0
        for status in reversed(sorted_statuses):
            if status == 'COMPLETED':
                count += 1
            else:
                break
        return f'{count} days'

    @classmethod
    def total_completed_sessions(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if not sorted_statuses:
            return 'N/A'
        return f"{sorted_statuses.count('COMPLETED')}"

    @classmethod
    def completion_rate(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if not sorted_statuses:
            return 'N/A'
        return f"{round((sorted_statuses.count('COMPLETED') / len(sorted_statuses)) * 100, 2)}%"

    @classmethod
    def completion_ratio(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if not sorted_statuses:
            return 'N/A'
        return f"{sorted_statuses.count('COMPLETED')} / {len(sorted_statuses)}"

    @classmethod
    def count_days(cls):
    #    (5, 'studying for hours', '2026-06-01 14:10:00', '00:15:00', 'MISSED', None)
        sorted_habits, sorted_statuses = cls.find_statuses() 
        sorted_habits = [habit for habit in sorted_habits if habit[4] in ['MISSED', 'COMPLETED']]
        return len(set([habit[2].split(' ')[0].strip() for habit in sorted_habits]))

    @classmethod
    def total_missed_sessions(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if not sorted_statuses:
            return 'N/A'
        return f"{sorted_statuses.count('MISSED')}"

    @classmethod
    def display_detailed_analytics(cls):
        day_of_week_completion_table = Table(width=80, header_style="bold white on blue")
        console = Console()
        day_of_week_completion_table.add_column("Day", style="bold",width=1)
        day_of_week_completion_table.add_column("Completion", justify="center", style="bold")
        day_of_week_completion_table.add_column("Sessions", justify="center", style="bold")
        day_of_week_completion_table.add_row("Mon","89%",'8/9')
        day_of_week_completion_table.add_row("Tue","89%",'8/9')
        day_of_week_completion_table.add_row("Wed","89%",'8/9')
        day_of_week_completion_table.add_row("Thurs","89%",'8/9')
        day_of_week_completion_table.add_row("Fri","89%",'8/9')
        day_of_week_completion_table.add_row("Sat","89%",'8/9')
        day_of_week_completion_table.add_row("Sun","89%",'8/9')
# 
        daily_load_vs_completion     = Table(header_style="bold white on blue", width=80)
        special_val = Text("6+ hrs", style="bold cyan on #ca7c57", justify="center")
        daily_load_vs_completion.add_column("Committed Time(Load)", justify="center",width=10, style="bold")
        daily_load_vs_completion.add_column("Completion", justify="center", style="bold")
        daily_load_vs_completion.add_column("Sessions", justify="center", style="bold")
        daily_load_vs_completion.add_row('0 hrs ≤ load < 01 hr','50%','5/10')
        daily_load_vs_completion.add_row('01 hr ≤ load < 2 hrs','50%','5/10')
        daily_load_vs_completion.add_row('2 hrs ≤ load < 3 hrs','50%','5/10')
        daily_load_vs_completion.add_row('3 hrs ≤ load < 4 hrs','50%','5/10')
        daily_load_vs_completion.add_row('4 hrs ≤ load < 5 hrs','50%','5/10')
        daily_load_vs_completion.add_row('5 hrs ≤ load < 6 hrs','50%','5/10')
        daily_load_vs_completion.add_row(special_val,'50%','5/10')

        special_val = Text("5+ sessions", style="bold cyan on #ca7c57", justify="center")
        overall_baseline_session_vol_distribution = Table( width=80, header_style="bold white on blue")
        overall_baseline_session_vol_distribution.add_column("Sessions", justify="center",width=10, style="bold")
        overall_baseline_session_vol_distribution.add_column("Share of Days", justify="center", style="bold")
        overall_baseline_session_vol_distribution.add_column("Ave commited time", justify="center", style="bold")
        overall_baseline_session_vol_distribution.add_row('0 sessions','50%','None')
        overall_baseline_session_vol_distribution.add_row('1 - 2 sessions','85%','1 /day')
        overall_baseline_session_vol_distribution.add_row('3 - 4 sessions','23%','2 hrs/day')
        overall_baseline_session_vol_distribution.add_row(special_val,'80%','4hrs 40mins/day')

        current_streak_session_vol_distribution = Table( width=80, header_style="bold white on blue")
        current_streak_session_vol_distribution.add_column("Sessions", justify="center",width=10, style="bold")
        current_streak_session_vol_distribution.add_column("Share of Days", justify="center", style="bold")
        current_streak_session_vol_distribution.add_column("Ave commited time", justify="center", style="bold")
        current_streak_session_vol_distribution.add_row('0 sessions','50%','None')
        current_streak_session_vol_distribution.add_row('1 - 2 sessions','85%','1 /day')
        current_streak_session_vol_distribution.add_row('3 - 4 sessions','23%','2 hrs/day')
        current_streak_session_vol_distribution.add_row(special_val,'80%','4hrs 40mins/day')

        longest_streak_session_vol_distribution = Table( width=80, header_style="bold white on blue")
        longest_streak_session_vol_distribution.add_column("Sessions", justify="center",width=10, style="bold")
        longest_streak_session_vol_distribution.add_column("Share of Days", justify="center", style="bold")
        longest_streak_session_vol_distribution.add_column("Ave commited time", justify="center", style="bold")
        longest_streak_session_vol_distribution.add_row('0 sessions','50%','None')
        longest_streak_session_vol_distribution.add_row('1 - 2 sessions','85%','1 /day')
        longest_streak_session_vol_distribution.add_row('3 - 4 sessions','23%','2 hrs/day')
        longest_streak_session_vol_distribution.add_row(special_val,'80%','4hrs 40mins/day')
        clear_screen()
        print(f'''--------------------------------------------------------------------------------
                        📊  BASIC ANALYTICS
--------------------------------------------------------------------------------
                            
I. {Back.BLUE}🌐 OVERALL PERFORMANCE                                                       {Style.RESET_ALL}
     • Analysis Period    : {cls.count_days()} days
     • Avg Sessions       : 5 sessions/day
     • Completion Rate    : {cls.completion_rate()} ({cls.completion_ratio()} sessions)
     • Avg Committed Time : 1.80 hrs/day
     • Peak Zone          : Afternoon (75.0% share)
     • Maximum Daily Commit : 5h
     • Minimum Daily Commit : 0m
''')
        console.print(overall_baseline_session_vol_distribution)
        print(f'''
II.  {Back.BLUE}🔥 CURRENT STREAK                                                          {Style.RESET_ALL} 
     • Streak Length      : {cls.current_streak()}
     • Avg Committed Time : 2.4 hrs/day
     • Peak Zone          : Morning (85.0% share)
     • Maximum Daily Commit : 5h
     • Minimum Daily Commit : 0m
''')
        console.print(current_streak_session_vol_distribution)
        print(f'''
III. {Back.BLUE}🏆 LONGEST STREAK                                                          {Style.RESET_ALL}
     • Streak Length      : {cls.longest_streak()}
     • Avg Committed Time : {cls.long_streak_duration_ave()}/day
     • Peak Zone          : Not enough distribution
     • Maximum Daily Commit : 5h
     • Minimum Daily Commit : 0m
''')        
        console.print(longest_streak_session_vol_distribution)
        print(f'''
IV. {Back.BLUE}📅 COMPLETION RATE BY DAY OF WEEK                                           {Style.RESET_ALL}
''')
        console.print(day_of_week_completion_table)
        print(f'''
V.  {Back.BLUE}🏋️  COMPLETION RATE BY DAILY COMMITTED TIME                                  {Style.RESET_ALL}
''')
        console.print(daily_load_vs_completion)
        print('''----------------------------------------------------------------------------------''')
        input('                         Press Enter to continue')
