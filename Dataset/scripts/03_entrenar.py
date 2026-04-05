import cv2
import os
import numpy as np

data_path = 'dataset'
model_path = os.path.join('models', 'trained_model.xml')
os.makedirs('models', exist_ok=True)

lista_personas = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
labels, faces_data = [], []
label = 0

print("Entrenando modelo...")

for name_dir in lista_personas:
    person_path = os.path.join(data_path, name_dir)
    for file_name in os.listdir(person_path):
        img = cv2.imread(os.path.join(person_path, file_name), 0)
        if img is not None:
            faces_data.append(img)
            labels.append(label)
    label += 1

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces_data, np.array(labels))
face_recognizer.write(model_path)
print(f"Modelo guardado en {model_path}")
