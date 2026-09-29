from colorama import Back, Fore
class Shelf:
    __habits_shelf = set()

    @classmethod
    def preserve_habit(cls,habit):
        cls.__habits_shelf = set()
        cls.__habits_shelf.add(habit)
        if len(cls.__habits_shelf)!=1:
            cls.__habits_shelf.pop(0)
    
    @classmethod
    def display_state(cls):
        return 'Shelf Status    : ❌ Empty' if len(cls.__habits_shelf)!=1 else f'Shelf Status    : ✅ Shelf has the follwing habit\n{cls.display_habit()}'

    @classmethod
    def display_habit(cls):
        id,name,start_datetime,duration,status,periodicity = list(cls.__habits_shelf)[0]
        return f'''
{Back.BLUE} Habit                                             {Back.RESET}
 id             :{id}
 name           :{name}
 start datetime :{start_datetime}
 duration       :{duration}
 status         :{status} 
 periodicity    :{periodicity}

 {Fore.RED}Note: You cannot modify a missed/completed habit,
 you can only view it.{Fore.RESET}
'''

    @classmethod
    def copy_last_place_habit(cls):
        if len(list(cls.__habits_shelf))!=0:
            return list(cls.__habits_shelf)[0]
        return None
    
    @classmethod
    def empty_shelf(cls):
        try:
            cls.__habits_shelf.clear()
        except Exception as e:
            pass