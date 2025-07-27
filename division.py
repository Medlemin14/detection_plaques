import shutil
import random
import os 

images_dir = "Data2/images"
annotations_dir = "Data2/annotations"

os.makedirs(annotations_dir + "/train", exist_ok=True)
os.makedirs(annotations_dir + "/val", exist_ok=True)
os.makedirs(annotations_dir + "/test", exist_ok=True)
os.makedirs(images_dir + "/train", exist_ok=True)
os.makedirs(images_dir + "/val", exist_ok=True)
os.makedirs(images_dir + "/test", exist_ok=True)

images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg')) and os.path.isfile(os.path.join(images_dir, f))]
random.shuffle(images)
n = len(images)
train, val = int(0.7*n), int(0.9*n)

for i, img_file in enumerate(images):
    base = os.path.splitext(img_file)[0]
    label_file = base + ".txt"

    if i < train:
        split = "train"
    elif i < val:
        split = "val"
    else:
        split = "test"

    shutil.move(os.path.join(images_dir, img_file), os.path.join(images_dir, split, img_file))
    if os.path.exists(os.path.join(annotations_dir, label_file)):
        shutil.move(os.path.join(annotations_dir, label_file), os.path.join(annotations_dir, split, label_file))