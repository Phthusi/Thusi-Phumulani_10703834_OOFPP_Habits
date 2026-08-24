from ...data.db_manager import Habits

class Analytics:

    @classmethod
    def find_statuses(cls):
        sorted_habits = list(sorted(Habits().get_habits(),key=lambda x:x[2]))
        sorted_statuses = [ habit[4] for habit in sorted_habits if habit[4] in ['MISSED','COMPLETED']]
        return sorted_habits, sorted_statuses
    
    @classmethod
    def streaks_calculator(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        count = 0
        streaks = []
        for status in sorted_statuses:
            if status == 'COMPLETED':
                count+=1
            else:
                streaks.append(count)
                count = 0
        return [streak for streak in streaks if streak!=0]

    @classmethod
    def longest_streak(cls):
        return f'{max(cls.streaks_calculator())} days'

    @classmethod
    def current_streak(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        count = 0
        for status in reversed(sorted_statuses):
            if status == 'COMPLETED':
                count+=1
            else:
                break
        return f'{count} days'

    @classmethod
    def total_completed_sessions(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if sorted_statuses==[]:
            return 'N\A'
        return f'{sorted_statuses.count('COMPLETED')}'

    @classmethod
    def completion_rate(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if sorted_statuses==[]:
            return 'N\A'
        return f'{round((sorted_statuses.count('COMPLETED')/len(sorted_statuses))*100,2)}%'

    @classmethod
    def total_missed_sessions(cls):
        sorted_habits, sorted_statuses = cls.find_statuses()
        if sorted_statuses==[]:
            return 'N\A'
        return f'{sorted_statuses.count('MISSED')}'
