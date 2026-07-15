    # @retry_until_success
    # def sort_habits(self):
    #     commands = ['asc','desc']
    #     history_file_name = 'sort_results'
    #     if self.__habits==[]:
    #         return True, 'sorry there are no habits to sort'

    #     order = self.__my_input('Enter the way you want to sort habits: ',history_file_name,commands)
    #     # ********* start of common functions ************        
    #     did_run_common_func = ran_common_functions(order)
    #     message_to_display = find_message(order)
    #     if did_run_common_func==False:
    #         return True, message_to_display
    #     elif did_run_common_func==True:
    #         return False, message_to_display
    #     # ********** end of common functions ************
    #     if order not in commands:
    #         return False, f'\'{order}\' is not a valid input'
        
    #     return True,'hello'
    
    # @retry_until_success
    # def sort_by(self,message):
    #     commands = ['name','datetime','status','duration']
    #     history_file_name = 'sort_by'
    #     order_by = self.__my_input(message,history_file_name,commands)
    #     # ********* start of common functions ************        
    #     did_run_common_func = ran_common_functions(order_by)
    #     message_to_display = find_message(order_by)
    #     if did_run_common_func==False:
    #         return True, message_to_display
    #     elif did_run_common_func==True:
    #         return False, message_to_display
    #     # ********** end of common functions ************
    #     return True,'hello'

    # @retry_until_success
    # def sort_by_name(self):
    #     pass

    # @retry_until_success
    # def sort_by_time(self):
    #     pass

    # @retry_until_success
    # def sort_by_date(self):
    #     pass

    # @retry_until_success
    # def sort_by_datetime(self):
    #     pass

    # @retry_until_success
    # def sort_by_status(self):
        # pass

class View:
    def display_habit(self, habit):
        pass