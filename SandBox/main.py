import pandas as pd
import json
import ast


import json
import csv
import os
import sys


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_csv(json_file_path, output_dir):
    # Read JSON file
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {json_file_path} is not a valid JSON file.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process info section
    info_flattened = flatten_dict(data['info'])
    with open(os.path.join(output_dir, 'info.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(info_flattened.keys())
        writer.writerow(info_flattened.values())

    # Process media section
    if data['media']:
        media_keys = set()
        for item in data['media']:
            media_keys.update(flatten_dict(item).keys())

        with open(os.path.join(output_dir, 'media.csv'), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(media_keys))
            writer.writeheader()
            for item in data['media']:
                writer.writerow(flatten_dict(item))

    # Process metadata section
    if data['metadata']:
        metadata_keys = set()
        for item in data['metadata']:
            metadata_keys.update(flatten_dict(item).keys())

        with open(os.path.join(output_dir, 'metadata.csv'), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(metadata_keys))
            writer.writeheader()
            for item in data['metadata']:
                writer.writerow(flatten_dict(item))

    print(f"CSV files have been created in the '{output_dir}' directory.")


if __name__ == "__main__":

    json_file_path = 'D:\\Visual Layer\\metadata.json'
    output_dir = 'D:\\Visual Layer\\metadata.csv'
    #file = 'D:\\Visual Layer\\metadata.json'
    json_to_csv(json_file_path, output_dir)