
class Habit:
    def __init__(self, name, session_duration, start_date, status="UPCOMING",id=None):
        self.__name = name
        self.__session_duration = session_duration
        self.__start_date = start_date
        self.__status = status
        self.__id = id
        self.__periodicity = None

    def get_periodicity(self):
        return self.__periodicity

    def get_name(self):
        return self.__name
    
    def get_session_duration(self):
        return self.__session_duration
    
    def get_start_date(self):
        return self.__start_date
    
    def get_status(self):
        return self.__status
    
    def get_id(self):
        return self.__id
    
    def set_name(self, name):
        self.__name = name
    
    def set_session_duration(self, session_duration):
        self.__session_duration = session_duration
    
    def set_start_date(self, start_date):
        self.__start_date = start_date
    
    def set_status(self, status):
        self.__status = status

    def set_periodicity(self,perioditicy):
        self.__periodicity = perioditicy

    def set_id(self,id):
        self.__id = id

    def __str__(self):
        return f"Habit(id={self.__id}, name='{self.__name}', session_duration='{self.__session_duration}', start_date='{self.__start_date}', status='{self.__status}')"
    
