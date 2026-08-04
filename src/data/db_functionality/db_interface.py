from .db import Database
from pathlib import Path

class DB_Interface:
    __cached_data = []
    
    def __init__(self,database_name= Path(__file__).resolve().parent.parent.parent.parent / "habit.db"):
        self.__db = Database(database_name)
        self.get_all_habits()

    def __id_in_db(self,id):
        return id in [entry[0] for entry in self.__cached_data]

    def get_all_habits(self):        
        message,self.__cached_data = self.__db.get_all_habits()
        return self.__cached_data
    
    def update_habit(self, id, **kwargs):
        if self.__id_in_db(id):
            return self.__db.update_habit(id, **kwargs)
        return "error", f"habit with id={id} does not exist"

    def add_habit(self, name, start_datetime, duration, status, periodicity=None):
        success, id = self.__db.add_habit(name, start_datetime, duration, status, periodicity)
        if success == "success":
            self.__cached_data.append((id, name, start_datetime, duration, status, periodicity))
        return success, id

    def delete_habit(self,id):
        if not self.__id_in_db(id):
            return "error",f"habit with id={id} does not exist"
        success, result = self.__db.delete_habit(id)
        if success== "success":
            self.__cached_data = [entry for entry in self.__cached_data if entry[0]!=id]
        return success, result
    
    def get_cached_data(self):
        return self.__cached_data

if __name__=="__main__":
    x = DB_Interface()
    print(x.get_all_habits())