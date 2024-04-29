import json
import csv
import os

# Load JSON data from file
with open('data1.json', 'r') as file:
    data = json.load(file)

# Specify the CSV file path
csv_file = '../../../data/data.csv'

# Define CSV header
csv_header = [
    'username', 'posts_count', 'followers_count', 'followees_count',
    'post_ids', 'post_captions', 'posts', 'primary_bio', 'secondary_bio',
    'most_recent_date', 'least_recent_date'
]

# Check if the CSV file already exists
write_header = not os.path.exists(csv_file)

# Create and open CSV file for writing
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_header)

    # Write header only if the file is new
    if write_header:
        writer.writeheader()

    # Iterate over each user data
    for user_data in data:
        # Get user details
        username = user_data['user']
        posts_count = user_data['posts_count']
        followers_count = user_data['followers_count']
        followees_count = user_data['followees_count']
        primary_bio, secondary_bio = user_data['bio']
        most_recent_date = user_data['most_recent_date']
        least_recent_date = user_data['least_recent_date']

        # Get post details
        post_ids = [post['post_id'] for post in user_data['posts']]
        post_captions = [post['caption'] for post in user_data['posts']]

        # Assuming that the images are stored in folders named after the username
        # and the image name is the same as the post_id
        posts_folder = f'posts\{username}'
        posts = [os.path.join(posts_folder, f"{post_id}.jpg") for post_id in post_ids]

        # Write user data to CSV file
        writer.writerow({
            'username': username,
            'posts_count': posts_count,
            'followers_count': followers_count,
            'followees_count': followees_count,
            'post_ids': '|'.join(post_ids),
            'post_captions': '|'.join(post_captions),
            'posts': '|'.join(posts),
            'primary_bio': primary_bio,
            'secondary_bio': secondary_bio,
            'most_recent_date': most_recent_date,
            'least_recent_date': least_recent_date
        })

print("CSV file updated successfully.")
