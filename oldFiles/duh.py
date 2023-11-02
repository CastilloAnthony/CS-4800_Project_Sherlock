import re

# The provided string
data_str = "{'_id': ObjectId('6542ea752079dc2a9c74ca6c'), 'name': 'adfa', 'presetLists': ['www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com'], 'timestamp': 1698884213.945767}"

# Define a regular expression pattern to match key-value pairs
pattern = r"'(\w+)': (?:'([^']*)'|(?:\[(.*?)\])|(\d+\.\d+)|ObjectId\('([^']*)'\))"

# Find all key-value pairs in the string
matches = re.findall(pattern, data_str)

# Create a dictionary from the matches
data = {}
for key, value_str, list_str, float_str, obj_id in matches:
    value = value_str if value_str else (list_str.split(', ') if list_str else (float(float_str) if float_str else obj_id))
    data[key] = value
print('data: ',type(data), '  ', data)


original_dict = {
    '_id': '6542ea752079dc2a9c74ca6c',
    'name': 'adfa',
    'presetLists': ["'www.csustan.edu'", "'www.microsoft.com'", "'www.nasa.gov'", "'chat.openai.com'"],
    'timestamp': 1698884213.945767
}

def remove_double_quotes(item):
    if isinstance(item, list):
        return [remove_double_quotes(element) for element in item]
    elif isinstance(item, dict):
        return {key: remove_double_quotes(value) for key, value in item.items()}
    elif isinstance(item, str):
        return item.replace('"', '').replace("'", '')  # Remove both double and single quotes
    else:
        return item

modified_dict = remove_double_quotes(original_dict)

print('modified_dict: ',type(modified_dict), '  ', modified_dict)
