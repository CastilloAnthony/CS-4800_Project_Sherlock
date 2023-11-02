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

print("Data:", data)
print("_id",data['_id'])
print("name",data['name'])
print("presetLists",data['presetLists'])
print("timestamp",data['timestamp'])
