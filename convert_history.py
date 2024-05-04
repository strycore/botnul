"""Convert JSON history file to CSV using Pandas."""
import json
import os
import re
import pandas as pd


def list_channels():
    for filename in os.listdir():
        match = re.match(r'backup-(\w+)\.json', filename)
        if match:
            channel_name = match.group(1)
            yield channel_name, filename


def convert_to_csv(channel_name, filename):
    with open(filename) as f:
        data = json.load(f)
    cleaned_data = []
    for row in data:
        if not row['content']:
            continue
        cleaned_data.append({
            'created_at': row['created_at'],
            'username': row['author']['name'],
            'content': row['content']
        })
    df = pd.DataFrame(cleaned_data)
    df.to_csv('{}.csv'.format(channel_name), index=False)


if __name__ == '__main__':
    for channel_name, filename in list_channels():
        print("Converting", channel_name, "to CSV...")
        convert_to_csv(channel_name, filename)

