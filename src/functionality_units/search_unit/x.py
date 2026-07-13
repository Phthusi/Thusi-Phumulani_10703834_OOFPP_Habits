# from ....data.db_manager import Habits
import re
'''
(status is UPCOMING) and (duration is 00:15:00) and (startdatetime islessthan 2018-10-12 14:00:00)

name          : is, has
status        : is
duration      : is, is less than, is greater than
startdatetime : is, is before, is after
'''
class Search:
    def __user_input_spliter(self,string,operator='and'):
        results = list(map(lambda i:i.strip(),string.split(operator)))
        return [result.replace(')','').replace('(','') for result in results]

    def __used_brackets_correctly(self,string):
        pass

    def __remove_brackets(self,text):
        return re.sub(r'\(.*?\)','',text)
    
    def __is_operation_uniform(self,text):
        operations=self.__remove_brackets(text)
        operations = set(operations.split(' '))
        operations = {operation for operation in operations if operation!=''}
        return len(operations)==1,operations
    
    def __extract_operator(self,text):
        if 'is less than' in text:
            return text.replace('is less than',''),'is less than'
        elif 'is greater than' in text:
            return text.replace('is greater than',''),'is greater than'
        elif 'is before' in text:
            return text.replace('is before',''),'is before'
        elif 'is after' in text:
            return text.replace('is before',''),'is after'
        elif 'has' in text:
            return text.replace('has',''),'has'
        elif 'is' in text:
            return text.replace('is',''),'is'
        return text, None
    
    # def check_
    
    def __match_fields(self,user_inputs):
        results = []
        for user_input in user_inputs:
            field_and_value, operator = self.__extract_operator(user_input)
            # check if operator is none
            field_and_value = [entity for entity in field_and_value.split(' ') if entity!='']
            if field_and_value[0]=='startdatetime':
                field_and_value = [field_and_value[0],' '.join(field_and_value[1:])]
            field,value = field_and_value
            results.append(
                {
                'field': field,
                'operator' :operator,
                'value' :value
                }
            )
        return results

if __name__=='__main__':
    x = Search()
    text = '(status is UPCOMING) and (duration is 00:15:00) and (startdatetime is less than 2018-10-12 14:00:00)'
    is_operation_uniform,operations = x._Search__is_operation_uniform(text)
    operation = operations.pop()
    y = x._Search__user_input_spliter(text)
    #used brackets 
    print(x._Search__match_fields(y))