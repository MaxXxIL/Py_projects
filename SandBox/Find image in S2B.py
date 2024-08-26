import os
import pandas as pd
from pathlib import Path


def update_csv_with_image_existence(root_folder, csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    if 'ImageName' not in df.columns:
        print("Error: CSV file does not contain 'ImageName' column.")
        return

    # Get all image files from root folder and immediate subfolders
    image_files = set()
    for folder in [root_folder] + [f.path for f in os.scandir(root_folder) if f.is_dir()]:
        image_files.update([f.name.lower() for f in os.scandir(folder) if
                            f.is_file() and f.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])

    # Add 'exist' column, initialized with 0
    df['exist'] = 0

    # Set 'exist' to 1 where ImageName is found in image_files
    df.loc[df['ImageName'].str.lower().isin(image_files), 'exist'] = 1

    # Save the updated DataFrame back to CSV
    output_csv = Path(csv_file).with_name(f"updated_{Path(csv_file).name}")
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved as: {output_csv}")

    # Print summary
    total_images = len(df)
    existing_images = df['exist'].sum()
    print(f"Total images in CSV: {total_images}")
    print(f"Images found in folders: {existing_images}")
    print(f"Images not found: {total_images - existing_images}")


# Example usage
root_folder = "D:\\Clean Data evaluation\\Visual Layer\\MTK-AHH10989-FQC(Multi)_a-1586ea\\Visual layer - KYEC with Metadata"
csv_file = "D:\\Clean Data evaluation\\Visual Layer\\MTK-AHH10989-FQC(Multi)_a-1586ea\\combined_Surface2Bump.csv"

update_csv_with_image_existence(root_folder, csv_file)