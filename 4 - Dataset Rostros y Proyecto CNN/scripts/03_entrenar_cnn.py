import os
import sys
import math
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_DIR = os.path.join(BASE_DIR, 'dataset_split')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = (160, 160)
BATCH_SIZE = 32
EPOCHS_BASE = 15
EPOCHS_FINETUNE = 10

if not os.path.exists(SPLIT_DIR):
    print("No se encuentra dataset_split/. Ejecutando 04_split_dataset.py...")
    split_script = os.path.join(os.path.dirname(__file__), '04_split_dataset.py')
    if os.path.exists(split_script):
        os.system(f'"{sys.executable}" "{split_script}"')
    else:
        print("Error: 04_split_dataset.py no encontrado.")
        exit(1)

train_dir = os.path.join(SPLIT_DIR, 'train')
val_dir = os.path.join(SPLIT_DIR, 'val')

train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

class_names = list(train_gen.class_indices.keys())
num_classes = len(class_names)
print(f"Clases ({num_classes}): {class_names}")

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(*IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))
x = layers.Rescaling(scale=1./127.5, offset=-1)(inputs)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

steps_per_epoch = max(1, math.ceil(train_gen.samples / BATCH_SIZE))
validation_steps = max(1, math.ceil(val_gen.samples / BATCH_SIZE))

print("\n--- Fase 1: Entrenar cabeza (base congelada) ---")
history = model.fit(
    train_gen,
    steps_per_epoch=steps_per_epoch,
    validation_data=val_gen,
    validation_steps=validation_steps,
    epochs=EPOCHS_BASE,
    verbose=1
)

print("\n--- Fase 2: Fine-tuning (descongelar ultimas capas) ---")
base_model.trainable = True
fine_tune_at = len(base_model.layers) // 2
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history_fine = model.fit(
    train_gen,
    steps_per_epoch=steps_per_epoch,
    validation_data=val_gen,
    validation_steps=validation_steps,
    epochs=EPOCHS_FINETUNE,
    verbose=1
)

val_loss, val_acc = model.evaluate(val_gen, verbose=0)
print(f"\nPrecision final en validacion: {val_acc:.4f}")

model_path = os.path.join(MODEL_DIR, 'cnn_model.h5')
model.save(model_path)
print(f"Modelo guardado en: {model_path}")

classes_path = os.path.join(MODEL_DIR, 'class_names.txt')
with open(classes_path, 'w', encoding='utf-8') as f:
    for name in class_names:
        f.write(name + '\n')
print(f"Nombres de clases guardados en: {classes_path}")
