import os
import shutil
import random
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
dataset_dir = os.path.join(BASE_DIR, 'dataset')
output_dir = os.path.join(BASE_DIR, 'dataset_split')

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

random.seed(42)

if not os.path.exists(dataset_dir):
    print(f"Error: No se encuentra {dataset_dir}")
    exit(1)

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(output_dir, split), exist_ok=True)

classes = sorted([
    d for d in os.listdir(dataset_dir)
    if os.path.isdir(os.path.join(dataset_dir, d))
])

print(f"Clases encontradas: {len(classes)}")
for cls in classes:
    cls_path = os.path.join(dataset_dir, cls)
    images = [
        f for f in os.listdir(cls_path)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    random.shuffle(images)

    total = len(images)
    n_train = int(total * TRAIN_RATIO)
    n_val = int(total * VAL_RATIO)

    train_files = images[:n_train]
    val_files = images[n_train:n_train + n_val]
    test_files = images[n_train + n_val:]

    for split_name, file_list in [('train', train_files), ('val', val_files), ('test', test_files)]:
        split_dir = os.path.join(output_dir, split_name, cls)
        os.makedirs(split_dir, exist_ok=True)
        for f in file_list:
            shutil.copy2(
                os.path.join(cls_path, f),
                os.path.join(split_dir, f)
            )

    print(f"  {cls}: {total} imagenes -> train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")

print(f"\nDataset dividido guardado en: {output_dir}")
