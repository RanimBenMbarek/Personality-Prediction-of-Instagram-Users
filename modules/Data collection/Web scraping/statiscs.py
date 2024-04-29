import json

def count_photo_starting_captions_by_user(data):
    user_caption_counts = []  # List to store user caption counts as tuples (user, caption count)
    for user_data in data:
        user = user_data["user"]
        caption_count = 0
        for post in user_data["posts"]:
            caption = post["caption"]
            if caption.lower().startswith("photo"):
                caption_count += 1
        user_caption_counts.append((user, caption_count))

    # Sort the user_caption_counts list based on caption count (descending order)
    sorted_user_caption_counts = sorted(user_caption_counts, key=lambda x: x[1], reverse=True)
    return sorted_user_caption_counts

# Load JSON data from file
file_path = "data1.json"  # Update this with the actual file path
output_file_path = "output.txt"  # Output file path

with open(file_path, "r") as json_file:
    data = json.load(json_file)

# Call the function with the loaded JSON data
sorted_caption_counts = count_photo_starting_captions_by_user(data)

# Write the sorted caption counts to a text file and also write them in an array format
with open(output_file_path, "w") as output_file:
    output_file.write("Sorted caption counts (user, caption count):\n")
    for user, caption_count in sorted_caption_counts:
        output_file.write(f"User: {user}, Captions starting with 'photo': {caption_count}\n")

    # Write the sorted caption counts in an array format
    output_file.write("\nSorted caption counts in array format:\n")
    output_file.write(json.dumps(sorted_caption_counts))

print(f"Output written to {output_file_path}")

#%%
