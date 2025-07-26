import os
import shutil
import random

# Define paths
dataset_dir = "Data"  # Root directory of your dataset
images_dir = os.path.join(dataset_dir, "images")
annotations_dir = os.path.join(dataset_dir, "annotations")

# Define split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Seed for reproducibility
random.seed(42)

# Function to create directories within images and annotations
def create_dirs_in_images_and_annotations(base_dir):
    os.makedirs(os.path.join(base_dir, "train"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "val"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "test"), exist_ok=True)


# Create train, val, and test directories inside images and annotations
create_dirs_in_images_and_annotations(images_dir)
create_dirs_in_images_and_annotations(annotations_dir)

# Get list of image files
try:
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png','.WEBP'))]
    print(f"Found {len(image_files)} image files in {images_dir}")  # DEBUG
except FileNotFoundError:
    print(f"Error: Image directory not found: {images_dir}")
    exit()

try:
    annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith(('.txt', '.xml', '.json'))]
    print(f"Found {len(annotation_files)} annotation files in {annotations_dir}")  # DEBUG
except FileNotFoundError:
    print(f"Error: Annotation directory not found: {annotations_dir}")
    exit()

# Shuffle the image files
all_files = image_files
random.shuffle(all_files)

# Calculate split sizes
train_size = int(len(all_files) * train_ratio)
val_size = int(len(all_files) * val_ratio)

# Split the list of files
train_files = all_files[:train_size]
val_files = all_files[train_size:train_size + val_size]
test_files = all_files[train_size + val_size:]

print(f"Train size: {train_size}, Val size: {val_size}, Test size: {len(test_files)}") # Debug

# Function to move files to the destination directories
def move_files(files, source_dir, dest_dir):
    print(f"Moving {len(files)} from {source_dir} to {dest_dir}") # Debug
    for file in files:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file)

        try:
            shutil.move(source_path, dest_path)
        except FileNotFoundError:
            print(f"Warning: File not found: {source_path}. Skipping.")
        except Exception as e:
            print(f"Error moving file {source_path} to {dest_path}: {e}")

# Move image files
move_files(train_files, images_dir, os.path.join(images_dir, "train"))
move_files(val_files, images_dir, os.path.join(images_dir, "val"))
move_files(test_files, images_dir, os.path.join(images_dir, "test"))

# Move annotation files
def move_annotation_files(image_files, image_source_dir, annotation_source_dir):
    print(f"Moving annotations from {annotation_source_dir}") #Debug
    for image_file in image_files:
        name, ext = os.path.splitext(image_file)
        annotation_file = None
        annotation_file_candidate_extensions = ['.txt', '.xml', '.json']
        for annotation_candidate_extension in annotation_file_candidate_extensions:
            annotation_file_candidate_name = name + annotation_candidate_extension
            if annotation_file_candidate_name in os.listdir(annotation_source_dir):
                annotation_file = annotation_file_candidate_name
                break

        if annotation_file:
            #Determine destination directory
            if image_file in train_files:
                dest_dir = os.path.join(annotations_dir, "train")
            elif image_file in val_files:
                dest_dir = os.path.join(annotations_dir, "val")
            else:
                dest_dir = os.path.join(annotations_dir, "test")

            source_path = os.path.join(annotation_source_dir, annotation_file)
            dest_path = os.path.join(dest_dir, annotation_file)

            try:
                shutil.move(source_path, dest_path)

            except FileNotFoundError:
                print(f"Warning: Annotation file not found: {source_path}. Skipping.")
            except Exception as e:
                print(f"Error moving annotation file {source_path} to {dest_path}: {e}")
        else:
            print(f"Warning: No annotation file found for {image_file}")

# Execute the annotation moving
move_annotation_files(all_files, images_dir, annotations_dir)

print("Data split and moved successfully!")
print(f"Train set size: {len(train_files)}")
print(f"Validation set size: {len(val_files)}")
print(f"Test set size: {len(test_files)}")