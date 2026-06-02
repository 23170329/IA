# Proyecto: Reconocimiento Facial con CNN

## 1. Descripción General
Sistema de reconocimiento facial multiclase usando **Redes Convolucionales (CNN)** con Transfer Learning. Combina imágenes de entorno controlado (alumnos) con imágenes *in-the-wild* de figuras públicas (VGGFace2).

## 2. Composición del Dataset
El conjunto de datos se organiza en 11 categorías con ~300-400 imágenes cada una (~3,800 imágenes totales):
- **Alumno_JeanSaavedra**: ~300 fotos capturadas con diferentes ángulos y expresiones.
- **Famoso_1** a **Famoso_10**: ~350-400 fotos cada uno del dataset VGGFace2.

Todas las imágenes están preprocesadas a **160×160 píxeles en color (RGB)**.

## 3. Pipeline CNN

1. **Captura** (`01_captura.py`): Webcam → detección Haar Cascade → redimensionar a 160×160 → guardar.
2. **Preprocesamiento** (`02_prep.py`): Re-detección de rostros, recorte y estandarización a 160×160 color.
3. **División** (`03_split_dataset.py`): Separa el dataset en **70% train / 15% val / 15% test**.
4. **Entrenamiento** (`03_entrenar_cnn.py`): Transfer Learning con **MobileNetV2** pre-entrenado en ImageNet + Data Augmentation (rotación, zoom, flip, brillo). Dos fases: cabeza con base congelada (15 épocas) + fine-tuning de últimas capas (10 épocas).
5. **Predicción** (`04_test_cnn.py`): Reconocimiento en tiempo real por webcam con umbral de confianza y top-3.

## 4. Estructura del Proyecto
```
dataset/               # Imágenes originales preprocesadas
dataset_split/         # Dataset dividido (train/val/test)
models/
  ├── cnn_model.h5     # Modelo CNN entrenado
  └── class_names.txt  # Nombres de las 11 clases
scripts/
  ├── 01_captura.py        # Captura webcam
  ├── 02_prep.py           # Preprocesamiento
  ├── 03_split_dataset.py  # División train/val/test
  ├── 03_entrenar_cnn.py   # Entrenamiento CNN
  └── 04_test_cnn.py       # Test tiempo real
```

## 5. Ejecución
```bash
# Dividir dataset (si no se ha hecho)
python scripts/03_split_dataset.py

# Entrenar CNN
python scripts/03_entrenar_cnn.py

# Probar en tiempo real
python scripts/04_test_cnn.py
```

## 6. Resultados
- **Arquitectura**: MobileNetV2 → GlobalAvgPooling → Dropout(0.2) → Dense(11, softmax)
- **Precisión en validación**: ~79.2% (fine-tuning incluido)
- **Alumno_JeanSaavedra**: 100% correcto en test (20/20)
- **Parámetros**: 2,272,077 (14,091 entrenables)
