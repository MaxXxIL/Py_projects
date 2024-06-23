import os
import shutil
import random

def random_move_images(source_dir, destination_dir, num_images_to_copy):
    # Get a list of all files in the source directory
    all_files = os.listdir(source_dir)

    # Filter out non-image files (you may need to adjust this based on your file types)
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Ensure that the number of images to copy does not exceed the total number of available images
    num_images_to_copy = min(num_images_to_copy, len(image_files))

    # Randomly select images to copy
    selected_images = random.sample(image_files, num_images_to_copy)

    # Copy the selected images to the destination directory
    for image in selected_images:
        source_path = os.path.join(source_dir, image)
        destination_path = os.path.join(destination_dir, image)
        shutil.move(source_path, destination_path)

# Example usage:
source_directory = "F:\\sandisk\\sandisk_new\\training\\defect"
destination_directory = "F:\\sandisk\\sandisk_new\\test\\defect"
number_of_images_to_copy = 500

random_move_images(source_directory, destination_directory, number_of_images_to_copy)