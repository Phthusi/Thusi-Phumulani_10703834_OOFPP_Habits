from src.data.db_manager import CompleteHabit
class Pipe:
    __habits:list[CompleteHabit] = []

    @classmethod
    def take_habit(cls,habit:dict):
        id, name, start_datetime, duration, status = habit
        habit = CompleteHabit(name,duration,start_datetime,status,id)
        cls.__habits.append(habit)
        return True, "Habit taken"
    
    @classmethod
    def take_habits(cls,habits:list[CompleteHabit]):
        cls.__habits.extend(habits)
        return True, "Habits taken"
    
    @classmethod
    def release_last_taken(cls):
        return cls.__habits.pop() if cls.__habits else None
    
    @classmethod
    def release_last_taken_copy(cls):
        habit = cls.release_last_taken()
        return habit.copy_habit() if habit else None

    @classmethod
    def release_all(cls):
        habits = cls.__habits.copy()
        cls.__habits.clear()
        return habits