from src.data.db_manager import CompleteHabit
class Shelf:
    __habits_shelf = set()

    @classmethod
    def preserve_habit(cls,habit:CompleteHabit):
        cls.__habits_shelf.append(habit)

    @classmethod
    def take_last_place_habit(cls):
        return cls.__habits_shelf.pop(0)
    
    @classmethod
    def copy_last_place_habit(cls):
        return cls.__habits_shelf[-1].copy_habit()
    
