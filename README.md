# Inteligencia Artificial — 2026-S6

Repositorio de trabajos, notebooks y proyectos de la asignatura **Inteligencia Artificial** — 6to semestre.

## Estructura

```
0 - Examen Diagnostico/       → Diagnóstico: BST en Python
1 - Historia de la IA/        → PDFs sobre historia de la IA
2 - 8Puzzle y Tabla Comparativa/ → Puzzle 8 en Java + tabla comparativa de algoritmos
3 - 24Puzzle/                 → Puzzle 24 en Java + video demostrativo
4 - Dataset Rostros y Proyecto CNN/ → Reconocimiento facial con OpenCV + LBPH
5 - Notebooks/                → Notebooks Jupyter organizados por tema
6 - Proyecto Fnal (Narrador)/ → Proyecto final (en desarrollo)
```

## 5 - Notebooks (por tema)

| Carpeta | Contenido |
|---|---|
| `CNN/` | Redes convolucionales (CIFAR-10, clasificación de 5 celebridades) |
| `KNN/` | K-Nearest Neighbors desde cero |
| `SVM/` | SVM, SVR, clasificación de documentos, MNIST |
| `KMeans/` | Mean Shift clustering, PCA y reducción de dimensionalidad |
| `Red Neuronal/` | Clasificación básica con redes neuronales |
| `Perceptron (grados Kelvin a centigrados)/` | Conversión de temperatura con un perceptrón |
| `Regresion lineal/` | Lasso y Ridge regression |
| `General/` | Notebooks introductorios: datos categóricos, texto, imágenes, Gradient Boosting, scikit-learn |
| `data/` | Datasets compartidos (Titanic, vinos, exámenes, MNIST — descargar MNIST aparte) |
| `python/` | Scripts `.py` equivalentes a los notebooks |

## Tecnologías

- **Python 3** — NumPy, Pandas, scikit-learn, TensorFlow/Keras, OpenCV, Streamlit
- **Java** — Algoritmos de búsqueda (8-Puzzle, 24-Puzzle)

## Instalación

```bash
pip install -r requirements.txt
```

Los notebooks se ejecutan con:

```bash
jupyter notebook
# o
jupyter lab
```

## Datos

- Los datasets pequeños (`.csv`) están incluidos en `5 - Notebooks/data/`.
- **MNIST** (`train.csv`, `test.csv`) es demasiado grande para GitHub. Descargar de [Kaggle](https://www.kaggle.com/competitions/digit-recognizer/data) y colocarlos en `5 - Notebooks/data/mnist/`.
- El dataset de rostros (~3.800 imágenes) está en `4 - Dataset Rostros y Proyecto CNN/dataset/`.

## Proyectos destacados

- **Reconocimiento Facial** — Pipeline completo: captura con OpenCV, detección Haar Cascade, entrenamiento LBPH, test en tiempo real.
- **CNN 5 celebridades** — Clasificador de celebridades con TensorFlow/Keras + data augmentation.
- **CMS vs Transformer** — Demo en Streamlit comparando memorias complementarias vs transformers (`cms.py`).
