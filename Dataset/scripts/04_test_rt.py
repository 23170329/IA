import cv2
import os

data_path = os.path.join('Dataset', 'dataset')
lista_personas = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(os.path.join('models', 'trained_model.xml'))

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = cv2.resize(gray[y:y+h, x:x+w], (160, 160))
        label_id, conf = face_recognizer.predict(rostro)

        nombre = lista_personas[label_id] if conf < 80 else "Desconocido"
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, nombre, (x, y-10), 1, 1.5, (0, 255, 0), 2)

    cv2.imshow('Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
