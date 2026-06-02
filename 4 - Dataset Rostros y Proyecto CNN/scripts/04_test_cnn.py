import os
import cv2
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'cnn_model.h5')
CLASSES_PATH = os.path.join(BASE_DIR, 'models', 'class_names.txt')
CONFIDENCE_THRESHOLD = 0.5

if not os.path.exists(MODEL_PATH):
    print(f"Error: Modelo no encontrado en {MODEL_PATH}")
    print("Ejecuta primero 03_entrenar_cnn.py")
    exit(1)

if not os.path.exists(CLASSES_PATH):
    print(f"Error: class_names.txt no encontrado en {CLASSES_PATH}")
    exit(1)

with open(CLASSES_PATH, 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f if line.strip()]

print(f"Cargando modelo desde {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"Modelo cargado. Clases ({len(class_names)}): {class_names}")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

if not cap.isOpened():
    print("Error: No se pudo abrir la camara.")
    exit(1)

print("\nPresiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (160, 160))
        face_norm = face_resized.astype('float32')
        face_batch = np.expand_dims(face_norm, axis=0)

        predictions = model.predict(face_batch, verbose=0)[0]
        best_idx = np.argmax(predictions)
        confidence = float(predictions[best_idx])

        if confidence >= CONFIDENCE_THRESHOLD:
            name = class_names[best_idx]
            label = f"{name} ({confidence:.2f})"

            top3 = np.argsort(predictions)[-3:][::-1]
            info_lines = []
            for i, idx in enumerate(top3):
                info_lines.append(
                    f"{i+1}. {class_names[idx]}: {predictions[idx]:.2f}"
                )
        else:
            name = "Desconocido"
            label = f"Desconocido ({confidence:.2f})"
            info_lines = [label]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        label_y = y - 10
        for line in info_lines:
            cv2.putText(
                frame, line, (x, label_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
            )
            label_y -= 25

    cv2.imshow('Reconocimiento Facial CNN', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
