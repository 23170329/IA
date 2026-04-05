# 👁️ Proyecto: Dataset Híbrido de Reconocimiento Facial

## 1. Descripción General
Este proyecto implementa un sistema de reconocimiento facial multiclase con un enfoque de **Dataset Híbrido**. Combina imágenes de un entorno controlado (estudiante) con imágenes de entornos silvestres (*in-the-wild*) de figuras públicas internacionales.

## 2. Composición del Dataset
El conjunto de datos se organiza en 11 categorías con 300 imágenes cada una (3,300 imágenes totales):
* **Entorno Controlado:** 300 fotos de `Alumno_JeanSaavedra` capturadas con diferentes ángulos y expresiones.
* **Entorno Silvestre:** 3,000 fotos de 10 sujetos provenientes del dataset **VGGFace2** (Carpeta `train`).

## 3. Metodología Técnica
1. **Adquisición:** Uso de OpenCV para captura de video y extracción de frames.
2. **Preprocesamiento:** - Detección de rostros mediante **Haar Cascades**.
   - Recorte y alineación automática.
   - Conversión a escala de grises.
   - Estandarización de resolución a **160x160 píxeles**.
3. **Entrenamiento:** Implementación del algoritmo **LBPH** (Local Binary Patterns Histograms) para la generación del modelo jerárquico.

## 4. Estructura del Proyecto
- `dataset/`: Carpetas con las imágenes estandarizadas.
- `models/`: Archivo `trained_model.xml` (modelo entrenado).
- `scripts/`: Scripts de captura, procesamiento, entrenamiento y test.

## 🚀 Ejecución rápida
1. Instalar dependencias: `pip install opencv-contrib-python numpy`
2. Entrenar: `python scripts/03_entrenar.py`
3. Probar: `python scripts/04_test_rt.py`
