import os
import csv
from tkinter import filedialog
# Define the path to the top level folder containing the subfolders
top_level_folder = filedialog.askdirectory()

# List to hold all the data for the csv file
data = []

# Walk through the directory structure
for root, dirs, files in os.walk(top_level_folder):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            # Get the path to the file relative to the top level folder
            relative_path = os.path.relpath(os.path.join(root, file), start=top_level_folder)

            relative_path=relative_path.replace("\\",'/')
            # Get the class from the name of the folder
            class_name = os.path.basename(root)
            # Check for the folder with a blank name and assign an empty label
            if class_name == '0':  # Assuming this is how the "blank" folder is represented
                class_name = ''
            # Append the data to the list
            data.append({'image': relative_path, 'label': class_name})

# Define the path to the output CSV file
output_csv_path = os.path.join(top_level_folder, 'metadata.csv')

# Write the data to a CSV file
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['image', 'label'])
    writer.writeheader()
    writer.writerows(data)

print(f'Metadata CSV file has been created at: {output_csv_path}')