'''    def __init__(self):
        self.__state = "main_menu"
        self.__dir = "Home"
        self.__message = ""

    def set_state(self, state):
        self.__state = state
    
    def set_dir(self, dir):
        self.__dir = dir
    
    def set_message(self, message):
        self.__message = message

    def display_message(self,symbol):
        symbols = {
            "Error":"✖",
            "Success": "✔",
            "Warning":"⚠",
            "Information":"ℹ",
            "Critical Error":"❌",
            "Confirmed":"✅",
            "Hot":"🔥",
            "Idea":"💡",
            "Pinned":"📌",
            "Location":"📍",
            "Empty":" ○ ",
            "Filled":" ● ",
            "Loading": "⏳"
        }
        return f"[{symbols.get(symbol, '')}] {self.__message}"'''