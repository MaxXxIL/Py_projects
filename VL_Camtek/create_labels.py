import sys
import os
from PIL import Image
import polars as pl

if len(sys.argv) != 3:
    print("Usage: python3 create_labels.py <default_width> <root_folder>")
    print(len(sys.argv[1]))
    sys.exit(1)

bbox_map = {}

default_width = int(sys.argv[1])
default_height = default_width # alter this if you want rectangular boxes.
root_folder = sys.argv[2]
data = []

for dirpath, dirnames, filenames in os.walk(root_folder):
    for file in filenames:
        filepath = os.path.join(dirpath, file)

        try:
            image = Image.open(filepath)
            filename = os.path.relpath(filepath, root_folder)
            label = os.path.dirname(filename)
            bbox_width, bbox_height = bbox_map.get(label, (default_width, default_height))

            center_x, center_y = image.width // 2, image.height // 2
            bbox_x = center_x - bbox_width // 2
            bbox_y = center_y - bbox_height // 2

            data.append((filename, bbox_x, bbox_y, bbox_width, bbox_height, label))
        except Exception as e:
            print(f'failed to load image: {filepath}: {e}')

schema = {
    'filename': pl.Utf8,
    'col_x': pl.Int32,
    'row_y': pl.Int32,
    'width': pl.Int32,
    'height': pl.Int32,
    'label': pl.Utf8
}
annot = pl.DataFrame(data, schema=schema)
annot.write_parquet(os.path.join(root_folder, 'object_annotations.parquet'))
