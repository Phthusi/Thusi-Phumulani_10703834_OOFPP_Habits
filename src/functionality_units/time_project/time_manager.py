from datetime import datetime, timedelta

class HabitDateTimeManager:
    
    def calculate_time_difference(self, start_time_str, end_time_str):
        if not self.is_date_valid(start_time_str) or not self.is_date_valid(end_time_str):
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
        
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time   = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        
        return end_time - start_time
    
    def is_time_already_passed(self,datetime_to_check):
        datetime_to_check = datetime.strptime(datetime_to_check, "%Y-%m-%d %H:%M:%S")
        return datetime_to_check <= datetime.now()

    def is_clashing(self,datetime1,duration1,datetime2,duration2):
        datetime_pair = {'datetime1':[datetime1,duration1],'datetime2':[datetime2,duration2]}
        
        if datetime1 == datetime2:
            return True
        
        earliest_time_key,latest_time_key = ['datetime1','datetime2'] if datetime1 < datetime2 else ['datetime2','datetime1']
        earliest_time_t_initial,earliest_duration = datetime_pair[earliest_time_key]
        earliest_time_t_final = earliest_time_t_initial+earliest_duration

        latest_time_t_initial,_ = datetime_pair[latest_time_key]

        return earliest_time_t_initial <= latest_time_t_initial <= earliest_time_t_final

    def determine_habit_status(self, start_dt_str: str, duration_str: str):
        try:
            start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M:%S")
            hours, minutes, seconds = map(int, duration_str.split(":"))
            duration_td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            end_dt = start_dt + duration_td
            now = datetime.now()

            if start_dt <= now < end_dt:
                return "ONGOING"

            if start_dt > now:
                return "UPCOMING"

            if now > end_dt + timedelta(days=1):
                return "MISSED"

            return "TO_BE_CONFIRMED"

        except Exception:
            return "UNKNOWN"    
    
    def convert_duration(self,duration_str):
        hours, minutes, seconds = map(int, duration_str.split(":"))
        return timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
    
    def string_to_datetime(self,string_datetime):
        return datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")