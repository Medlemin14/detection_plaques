import os
import json
from PIL import Image

def convert_vgg_to_yolo(vgg_json_path, output_dir):
    with open(vgg_json_path, 'r') as f:
        vgg_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    for image_name, image_data in vgg_data.items():
        image_path = os.path.join("Data2/images", image_name)
        try:
            img = Image.open(image_path)
            width_image, height_image = img.size
        except FileNotFoundError:
            print(f"Image not found: {image_path}")
            continue

        regions = image_data['regions']
        yolo_lines = []
        for region_id, region_data in regions.items():
            shape_attributes = region_data['shape_attributes']
            if shape_attributes['name'] == 'polygon':
                all_points_x = shape_attributes['all_points_x']
                all_points_y = shape_attributes['all_points_y']

                x_min = min(all_points_x)
                y_min = min(all_points_y)
                x_max = max(all_points_x)
                y_max = max(all_points_y)

                center_x = (x_min + x_max) / 2 / width_image
                center_y = (y_min + y_max) / 2 / height_image
                width = (x_max - x_min) / width_image
                height = (y_max - y_min) / height_image

                yolo_line = f"0 {center_x} {center_y} {width} {height}\n"
                yolo_lines.append(yolo_line)

        output_file = os.path.join(output_dir, os.path.splitext(image_name)[0] + '.txt')
        with open(output_file, 'w') as outfile:
            outfile.writelines(yolo_lines)

# Exécution
convert_vgg_to_yolo("vgg_annotation.json", "Data2/annotations")