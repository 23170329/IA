import cv2
import os

# Según tu terminal, tus fotos están en esta ruta exacta:
dataset_dir = os.path.join('Dataset', 'dataset')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print(f"Buscando fotos en: {os.path.abspath(dataset_dir)}")

if not os.path.exists(dataset_dir):
    print(f"Error: No se encuentra la ruta {dataset_dir}")
    exit()

for subdir in os.listdir(dataset_dir):
    path_sujeto = os.path.join(dataset_dir, subdir)

    if not os.path.isdir(path_sujeto) or "Alumno" in subdir:
        continue

    print(f"Procesando fotos de: {subdir}...")

    # Listamos los archivos dentro de cada carpeta de famoso
    for file in os.listdir(path_sujeto):
        img_path = os.path.join(path_sujeto, file)

        # Saltamos archivos que no sean imágenes comunes
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        # Procesamiento
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            roi = img[y:y+h, x:x+w]
        else:
            roi = img

        final_img = cv2.resize(roi, (160, 160))
        cv2.imwrite(img_path, final_img)

print("\n¡Proceso terminado con éxito!")
