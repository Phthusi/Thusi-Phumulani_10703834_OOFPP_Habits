import json

def read_json_files(file_name='config.json'):
    with open(file_name,'r') as f:
        return json.load(f)
    

# print()