
class UpdateHabitValidator:
    """Validates user input arguments for habit modification forms."""
    def is_valid_habit_field_number(self,habit_field_number):
        """Validates whether an input represents a valid habit field count choice.

        Args:
            habit_field_number (str): Raw input string representing the target field count.

        Returns:
            bool: True if input is a positive integer between 1 and 4 inclusive, False otherwise.
        """
        try:
            assert '-' not in habit_field_number, f"{habit_field_number} must be postive"
            assert '.' not in habit_field_number, f"{habit_field_number} must be a whole number"
            return 0 < int(habit_field_number) <=4
        except Exception:
            return False

    def is_field_name_valid(self,field_name):
        """Checks if a field string matches supported mutable habit attributes.

        Args:
            field_name (str): Identifier name of the habit field.

        Returns:
            bool: True if field_name is 'name', 'start_datetime', or 'duration'.
        """
        return field_name in ['name','start_datetime','duration']
