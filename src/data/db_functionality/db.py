import sqlite3

class Database:
    def __init__(self, db_name) -> None:
        self.__connect = sqlite3.connect(db_name)
        self.__cursor = self.__connect.cursor()
        self.__name = db_name
        self.__create_table(
            """
            CREATE TABLE IF NOT EXISTS habit
            (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL ,
                start_datetime TEXT NOT NULL, 
                duration TEXT NOT NULL,
                status TEXT NOT NULL,
                periodicity TEXT
            );
            """
        )

    def __create_table(self, sql_query):
        try:
            with self.__connect:
                self.__cursor.execute(sql_query)
                return "success", None
        except Exception as e:
            return "error", e


    def add_habit(self, name, start_datetime, duration,status, periodicity) -> tuple:
        """Insert a habit and return ``('success', id)`` or an error tuple."""
        try:
            self.__cursor.execute(
                "INSERT INTO habit (name, start_datetime, duration, status, periodicity) VALUES (?, ?, ?, ?, ?)",
                [name, start_datetime, duration, status,periodicity]
            )

        except Exception as e:
            self.__connect.rollback()
            return "error", str(e)
    
        self.__connect.commit()
        return "success", self.__cursor.lastrowid

    def get_all_habits(self):
        """Return all habit rows ordered by their scheduled time."""
        try:
            self.__cursor.execute("""SELECT * FROM habit ORDER BY id""")
            return "success", self.__cursor.fetchall()
        except Exception as e:
            return "error", str(e)

    def delete_habit(self, id):
        """Delete a habit by ID and report whether the operation succeeded."""
        try:
            self.__cursor.execute(
            f"DELETE FROM habit WHERE id = ?",
            (id,)
            )
            self.__connect.commit()
            if self.__cursor.rowcount == 0:
                return "error", f"habit with id={id} does not exist"
            return "success", None
        except Exception as e:
            self.__connect.rollback()
            return "error", str(e)
    
    def update_habit(self, id, **kwargs):
        """Update allowed habit columns using parameterised SQL."""
        if not kwargs:
            return "error", "No fields supplied for update."

        valid_fields = {"name", "start_datetime", "duration", "status","periodicity"}   
        if not set(kwargs).issubset(valid_fields):
            return "error", f"Invalid fields for habit table. Valid fields are: {valid_fields}"

        try:
            self.__cursor.execute(
            f"UPDATE habit SET {', '.join([f'{k}=?' for k in kwargs.keys()])} WHERE id = ?",
            (*kwargs.values(), id))
            self.__connect.commit()
            return "success", f"habit Habit(id={id},) has been updated successfully..."
        
        except Exception as e:
            self.__connect.rollback()
            return "error", str(e)        

if __name__=="__main__":
    x = Database()
    # x.add_habit('Exercise', '2023-01-01 08:00:00', '01:00:00', 'MISSED')
    # x.add_habit('Exercise', '2023-01-01 08:00:00', '00:30:00', 'UPCOMING')
    # print("hello world!")
    print(x.get_all_habits())