import json

def count_photo_starting_captions_by_user(data):
    # Initialize dictionaries to store users based on their caption counts
    users_10=[]
    users_10_to_20 = []
    users_20_to_30 = []
    users_30_to_40 = []
    users_above_40 = []

    for user_data in data:
        user = user_data["user"]
        caption_count = 0
        for post in user_data["posts"]:
            caption = post["caption"]
            if caption.lower().startswith("photo"):
                caption_count += 1

        # Categorize users based on their caption counts
        if caption_count < 10:
            users_10.append(user)
        elif 10 <= caption_count < 20:
            users_10_to_20.append(user)
        elif 20 <= caption_count < 30:
            users_20_to_30.append(user)
        elif 30 <= caption_count < 40:
            users_30_to_40.append(user)
        else:
            users_above_40.append(user)

    user_categories = {
        "0_to10":users_10,
        "10_to_20": users_10_to_20,
        "20_to_30": users_20_to_30,
        "30_to_40": users_30_to_40,
        "above_40": users_above_40
    }

    # Print the length of each array
    for category, users_list in user_categories.items():
        print(f"Length of {category}: {len(users_list)}")

    return user_categories

# Load JSON data from file with UTF-8 encoding
file_path = "data.json"  # Update this with the actual file path
output_file_path = "output_all_info.json"  # Output file path

try:
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Unable to load JSON data from '{file_path}'.")
    exit(1)

# Call the function with the loaded JSON data
user_categories = count_photo_starting_captions_by_user(data)

# Write all information to a single JSON file
with open(output_file_path, "w") as output_file:
    output_file.write(json.dumps(user_categories, indent=4))

print(f"Output written to {output_file_path}")
