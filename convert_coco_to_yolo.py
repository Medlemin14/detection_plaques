import os
import json
from pycocotools.coco import COCO

def convert_coco_to_yolo_single_class(coco_json, output_dir):
    # Lecture brute du JSON
    with open(coco_json, "r") as f:
        raw_data = json.load(f)

    # Filtrage des annotations valides
    annotations = [ann for ann in raw_data.get("annotations", []) if "bbox" in ann and "image_id" in ann]

    # Indexer les annotations par image_id
    anns_by_image = {}
    for ann in annotations:
        anns_by_image.setdefault(ann["image_id"], []).append(ann)

    # Indexer les images
    images = {img["id"]: img for img in raw_data.get("images", [])}

    os.makedirs(output_dir, exist_ok=True)

    for img_id, anns in anns_by_image.items():
        img_info = images[img_id]
        width, height = img_info["width"], img_info["height"]
        file_name = img_info["file_name"]

        lines = []
        for ann in anns:
            x, y, w, h = ann["bbox"]
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            w /= width
            h /= height
            lines.append(f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")  # toujours class_id 0

        txt_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".txt")
        with open(txt_path, "w") as f:
            f.writelines(lines)

# Utilisation
convert_coco_to_yolo_single_class("coco_annotation.json", "Data2/annotations")
