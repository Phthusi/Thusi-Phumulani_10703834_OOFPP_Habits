"""Functional analytics for habit sessions."""

from functools import reduce
from datetime import timedelta
from ...data.db_manager import Habits
from ..time_project.time_manager import HabitDateTimeManager
from rich.table import Table
from rich.text import Text
from rich.console import Console
from ..ui.terminal_utils import clear_screen


def completion_streaks(statuses):
    """Return consecutive COMPLETED run lengths from a status sequence."""
    def step(acc, status):
        current, completed_runs = acc
        if status == "COMPLETED":
            return current + 1, completed_runs
        return 0, completed_runs + ([current] if current else [])
    current, runs = reduce(step, statuses, (0, []))
    return runs + ([current] if current else [])


def longest_streak_for_habit(habits):
    """Return the longest consecutive completed run in one habit's sessions."""
    ordered = sorted(habits, key=lambda h: h[2])
    return max(completion_streaks([h[4] for h in ordered]), default=0)


class Analytics:
    """Calculate habit statistics using functional transformations."""

    @classmethod
    def find_statuses(cls):
        """Return chronological rows and their completed/missed statuses."""
        rows = sorted(Habits().get_habits(), key=lambda habit: habit[2])
        tracked = [habit for habit in rows if habit[4] in {"MISSED", "COMPLETED"}]
        return rows, [habit[4] for habit in tracked]

    @classmethod
    def _tracked(cls):
        """Return chronologically ordered completed/missed rows."""
        rows = sorted(Habits().get_habits(), key=lambda habit: habit[2])
        return [h for h in rows if h[4] in {"MISSED", "COMPLETED"}]

    @classmethod
    def streaks_calculator(cls):
        """Return completed streak lengths and the rows belonging to each streak."""
        tracked = cls._tracked()
        streaks, groups, current = [], [], []
        for habit in tracked:
            if habit[4] == "COMPLETED":
                current.append(habit)
            elif current:
                streaks.append(len(current)); groups.append(current); current = []
        if current:
            streaks.append(len(current)); groups.append(current)
        return streaks, groups

    @classmethod
    def all_habits(cls):
        """Return all currently tracked habit sessions."""
        return Habits().get_habits()

    @classmethod
    def habits_by_periodicity(cls, periodicity):
        """Return habit sessions matching ``DAILY`` or ``WEEKLY`` periodicity."""
        return list(filter(lambda habit: habit[5] == periodicity, cls.all_habits()))

    @classmethod
    def longest_streak_for_habit(cls, habit_id):
        """Return the longest completed streak for a specific habit ID."""
        return f"{longest_streak_for_habit([h for h in cls.all_habits() if h[0] == habit_id])} days"

    @classmethod
    def longest_streak(cls):
        """Return the longest tracked streak as a human-readable value."""
        totals, _ = cls.streaks_calculator()
        return f"{max(totals)} days" if totals else "0 days"

    @classmethod
    def current_streak(cls):
        """Return the number of consecutive completed tracked sessions at the end."""
        statuses = [h[4] for h in cls._tracked()]
        count = 0
        for status in reversed(statuses):
            if status == "COMPLETED":
                count += 1
            else:
                break
        return f"{count} days"

    @classmethod
    def total_completed_sessions(cls):
        """Return the number of completed tracked sessions."""
        count = sum(1 for h in cls._tracked() if h[4] == "COMPLETED")
        return str(count) if count else "N/A"

    @classmethod
    def total_missed_sessions(cls):
        """Return the number of missed tracked sessions."""
        count = sum(1 for h in cls._tracked() if h[4] == "MISSED")
        return str(count) if count else "N/A"

    @classmethod
    def completion_rate(cls):
        """Return completed sessions as a percentage of tracked sessions."""
        statuses = [h[4] for h in cls._tracked()]
        return "N/A" if not statuses else f"{round(statuses.count('COMPLETED') / len(statuses) * 100, 2)}%"

    @classmethod
    def completion_ratio(cls):
        """Return completed sessions over all tracked sessions."""
        statuses = [h[4] for h in cls._tracked()]
        return "N/A" if not statuses else f"{statuses.count('COMPLETED')} / {len(statuses)}"

    @classmethod
    def count_days(cls):
        """Return the number of distinct days containing tracked sessions."""
        return len({h[2].split(" ")[0] for h in cls._tracked()})

    @classmethod
    def long_streak_duration_ave(cls):
        """Return average duration of the longest completed streak."""
        totals, groups = cls.streaks_calculator()
        if not totals:
            return "N/A"
        group = groups[totals.index(max(totals))]
        manager = HabitDateTimeManager()
        total = sum((manager.convert_duration(h[3]) for h in group), timedelta())
        average = total / len(group)
        minutes = int(average.total_seconds() // 60)
        hours, mins = divmod(minutes, 60)
        return f"{hours} Hrs,{mins} mins" if hours else f"{mins} mins"

    @classmethod
    def display_detailed_analytics(cls):
        """Display a compact, data-driven analytics report in the terminal."""
        console = Console()
        table = Table(title="Basic Habit Analytics")
        table.add_column("Metric")
        table.add_column("Value")
        metrics = [
            ("Analysis period", f"{cls.count_days()} days"),
            ("Longest streak", cls.longest_streak()),
            ("Current streak", cls.current_streak()),
            ("Completion rate", cls.completion_rate()),
            ("Completed sessions", cls.total_completed_sessions()),
            ("Missed sessions", cls.total_missed_sessions()),
            ("Completion ratio", cls.completion_ratio()),
        ]
        for name, value in metrics:
            table.add_row(name, str(value))
        clear_screen()
        console.print(table)
        input('Press enter to continue')