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
                name TEXT,
                start_datetime TEXT, 
                duration TEXT,
                status TEXT
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


    def add_habit(self, name, start_datetime, duration, status) -> tuple:
        try:
            self.__cursor.execute(
                "INSERT INTO habit (name, start_datetime, duration, status) VALUES (?, ?, ?, ?)",
                [name, start_datetime, duration, status]
            )

        except Exception as e:
            return "error", str(e)
    
        self.__connect.commit()
        return "success", self.__cursor.lastrowid

    def get_all_habits(self):
        try:
            self.__cursor.execute("""SELECT * FROM habit""")
            return "success", self.__cursor.fetchall()
        except Exception as e:
            return "error", str(e)

    def delete_habit(self, id):
        try:
            self.__cursor.execute(
            f"DELETE FROM habit WHERE id = ?",
            (id,)
            )
            self.__connect.commit()
            return "success", None
        except Exception as e:
            return "error", str(e)
    
    def update_habit(self, id, **kwargs):
        try:
            valid_fields = {"name", "start_datetime", "duration", "status"}
            if not all([field in valid_fields for field in kwargs.keys()]):
                return "error", f"Invalid fields for habit table. Valid fields are: {valid_fields}"
            
            self.__cursor.execute(
            f"UPDATE habit SET {', '.join([f'{k}=?' for k in kwargs.keys()])} WHERE id = ?",
            (*kwargs.values(), id))
            self.__connect.commit()
            return "success", None
        except Exception as e:
            return "errpr", str(e)        

if __name__=="__main__":
    x = Database()
    # x.add_habit('Exercise', '2023-01-01 08:00:00', '01:00:00', 'MISSED')
    # x.add_habit('Exercise', '2023-01-01 08:00:00', '00:30:00', 'UPCOMING')
    # print("hello world!")
    print(x.get_all_habits())