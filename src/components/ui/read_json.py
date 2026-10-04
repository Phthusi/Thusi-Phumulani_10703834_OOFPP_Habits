import json

def read_json_files(file_name='config.json'):
    """Reads and parses data from a JSON file.

    Args:
        file_name (str, optional): Path to the target JSON file. 
            Defaults to 'config.json'.

    Returns:
        dict | list: Parsed Python data structure containing the JSON contents.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        json.JSONDecodeError: If the file contains invalid JSON syntax.
    """
    with open(file_name,'r') as f:
        return json.load(f)
