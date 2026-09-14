from datetime import datetime

class HabitDateTimeManagerValidator:
    def is_datetime_valid(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
        
    def is_date_valid(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def is_passed(self,date_str):
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") > datetime.now()

    def is_time_format_valid(self, time_str):
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
                return True
            return False
        except Exception:
            return False
    
    def validate_duration(self,duration):
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            assert 0<=hours<24, 'hours must be greater or equal to zero but it must be less than 24'
            assert 0<=minutes<60, 'Minutes must be greater or equal to zero but it must be less than 60'
            assert 0<=seconds<60 , 'Seconds must be greater or equal to zero but it must be less than 60'
            return "SUCCESSFUL: duration set", True

        except Exception as e:
            return f"UNSUCCESSFUL: {e}", False    
        