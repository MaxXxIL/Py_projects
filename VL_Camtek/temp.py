import os
from PIL import Image
import imagehash

def find_similar_images(folder_path, threshold=10):
    image_hashes = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            hash_value = imagehash.phash(image)
            image_hashes[filename] = hash_value

    similar_images = {}
    for filename1, hash1 in image_hashes.items():
        for filename2, hash2 in image_hashes.items():
            if filename1 != filename2:
                distance = hash1 - hash2
                if distance <= threshold:
                    if filename1 not in similar_images:
                        similar_images[filename1] = []
                    similar_images[filename1].append(filename2)

    return similar_images