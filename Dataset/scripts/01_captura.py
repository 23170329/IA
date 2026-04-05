import cv2
import os

folder = os.path.join('dataset', 'Alumno_JeanSaavedra')
os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0

print("Iniciando captura (300 fotos)...")

while count < 300:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        rostro_color = frame[y:y+h, x:x+w]
        rostro_res = cv2.resize(rostro_color, (160, 160))

        cv2.imwrite(os.path.join(folder, f'foto_{count}.jpg'), rostro_res)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Captura Jean', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
print(f"Dataset listo con {count} fotos.")
