import json
import os
from PIL import Image

def convert_vgg_to_yolo(vgg_json_path, output_dir):
    """
    Convertit les annotations VGG JSON au format YOLO txt.

    Args:
        vgg_json_path (str): Chemin vers le fichier JSON VGG.
        output_dir (str): Chemin vers le dossier de sortie pour les fichiers txt YOLO.
    """
    with open(vgg_json_path, 'r') as f:
        vgg_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)  # Crée le dossier de sortie s'il n'existe pas

    for image_name, image_data in vgg_data.items():
        image_path = os.path.join("./Data/images", image_name)  # Remplacez par le chemin réel de vos images
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
            if shape_attributes['name'] == 'polygon': #Verifie si la shape est bien un polygone
              all_points_x = shape_attributes['all_points_x']
              all_points_y = shape_attributes['all_points_y']

              # Calcul de la bounding box
              x_min = min(all_points_x)
              y_min = min(all_points_y)
              x_max = max(all_points_x)
              y_max = max(all_points_y)

              # Calcul du centre, de la largeur et de la hauteur
              center_x = (x_min + x_max) / 2
              center_y = (y_min + y_max) / 2
              width = x_max - x_min
              height = y_max - y_min

              # Normalisation
              center_x /= width_image
              center_y /= height_image
              width /= width_image
              height /= height_image

              # Création de la ligne YOLO
              class_id = 0  # Assurez-vous que l'ID de classe est correct
              yolo_line = f"{class_id} {center_x} {center_y} {width} {height}\n"
              yolo_lines.append(yolo_line)
            else:
              print(f"Region {region_id} in {image_name} is not a polygon. Skipping...")

        # Écriture du fichier YOLO
        output_file = os.path.join(output_dir, os.path.splitext(image_name)[0] + '.txt')
        with open(output_file, 'w') as outfile:
            outfile.writelines(yolo_lines)

# Exemple d'utilisation
vgg_json_path = 'vgg_annotation.json'  # Remplacez par le chemin vers votre fichier JSON
output_dir = './Data/annotations'  # Remplacez par le chemin vers votre dossier de sortie
convert_vgg_to_yolo(vgg_json_path, output_dir)