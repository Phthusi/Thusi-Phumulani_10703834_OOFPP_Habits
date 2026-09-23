class SearchHabitTimeRepeats:
    def __init__(self, habit_time_repeats_repository):
        self.habit_time_repeats_repository = habit_time_repeats_repository

    def search(self, habit_id):
        return self.habit_time_repeats_repository.search(habit_id)