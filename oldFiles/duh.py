import json

input_string = '{"_id": "ObjectId(6542ea752079dc2a9c74ca6c)", "name": "adfa", "presetLists": ["www.csustan.edu", "www.microsoft.com", "www.nasa.gov", "chat.openai.com"], "timestamp": 1698884213.945767}'

# Convert the modified JSON string to a dictionary
my_dict = json.loads(input_string)

# Now, 'my_dict' is a Python dictionary
print(type(my_dict),my_dict)
