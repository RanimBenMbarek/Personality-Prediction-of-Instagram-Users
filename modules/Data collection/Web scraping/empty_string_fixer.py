import json

# Load the JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Function to recursively replace empty strings with "N/A"
def replace_empty_strings(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and value == "":
                obj[key] = "N/A"
            elif isinstance(value, (dict, list)):
                replace_empty_strings(value)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            if isinstance(obj[i], str) and obj[i] == "":
                obj[i] = "N/A"
            elif isinstance(obj[i], (dict, list)):
                replace_empty_strings(obj[i])

replace_empty_strings(data)

# Save the modified data back to the JSON file
with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
print('done')

#%%
