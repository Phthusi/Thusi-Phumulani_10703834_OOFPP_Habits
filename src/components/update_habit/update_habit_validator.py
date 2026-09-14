
class UpdateHabitValidator:
    def is_valid_habit_field_number(self,habit_field_number):
        try:
            assert '-' not in habit_field_number, f"{habit_field_number} must be postive"
            assert '.' not in habit_field_number, f"{habit_field_number} must be a whole number"
            return 0 < int(habit_field_number) <=4
        except Exception:
            return False

    def is_field_name_valid(self,field_name):
        return field_name in ['name','start_datetime','duration']
