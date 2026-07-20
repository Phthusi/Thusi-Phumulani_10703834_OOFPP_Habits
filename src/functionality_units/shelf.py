class Shelf:
    __habits_shelf = set()

    @classmethod
    def preserve_habit(cls,habit):
        cls.__habits_shelf = set()
        cls.__habits_shelf.add(habit)

    @classmethod
    def take_last_place_habit(cls):
        if len(cls.__habits_shelf)==0:
            return None
        return cls.__habits_shelf.pop()
    
    @classmethod
    def copy_last_place_habit(cls):
        if len(cls.__habits_shelf)!=0:
            return list(cls.__habits_shelf)[0]
        return None
    
