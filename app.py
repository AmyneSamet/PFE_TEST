import cv2
import os
import pygame
from datetime import datetime

# Initialiser Pygame pour les alertes sonores
pygame.mixer.init()
alert_sound = pygame.mixer.Sound('audio/alert.wav')  # Assurez-vous d'avoir un fichier 'alert.wav' dans le même répertoire

# Charger les classificateurs en cascade pour la détection de visage et d'yeux
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Démarrer la capture vidéo
video_capture = cv2.VideoCapture(0)

# Vérifier si la webcam est accessible
if not video_capture.isOpened():
    print("Erreur : Impossible d'accéder à la webcam.")
    exit()

# Paramètres pour le zoom
zoom_factor = 1.0  # Facteur de zoom initial
zoom_step = 0.1  # Pas de zoom
max_zoom = 2.0  # Zoom maximal
min_zoom = 1.0  # Zoom minimal

# Variables pour le suivi des visages
faces_detected = []  # Liste pour stocker les visages détectés
last_detection_time = None  # Temps de la dernière détection

# Dossier pour sauvegarder les images des visages détectés
output_folder = "detected_faces"
os.makedirs(output_folder, exist_ok=True)

while True:
    # Lire une image de la webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Erreur : Impossible de lire une image de la webcam.")
        break

    # Redimensionner l'image en fonction du zoom
    height, width = frame.shape[:2]
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    x1 = int((width - new_width) / 2)
    y1 = int((height - new_height) / 2)
    x2 = x1 + new_width
    y2 = y1 + new_height
    zoomed_frame = frame[y1:y2, x1:x2]

    # Convertir l'image zoomée en niveaux de gris pour la détection
    gray = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Si des visages sont détectés
    if len(faces) > 0:
        last_detection_time = datetime.now()  # Mettre à jour le temps de la dernière détection
        faces_detected = faces  # Mettre à jour la liste des visages détectés

        # Dessiner un rectangle autour de chaque visage et détecter les yeux
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(zoomed_frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)

            # Détecter les yeux dans la région du visage
            roi_gray = gray[fy:fy + fh, fx:fx + fw]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Dessiner des cercles autour des yeux
            for (ex, ey, ew, eh) in eyes:
                cv2.circle(zoomed_frame, (fx + ex + ew // 2, fy + ey + eh // 2), 10, (0, 0, 255), 2)

        # Zoom progressif sur les visages
        if zoom_factor < max_zoom:
            zoom_factor += zoom_step

        # Sauvegarder les images des visages détectés
        for i, (fx, fy, fw, fh) in enumerate(faces):
            face_img = zoomed_frame[fy:fy + fh, fx:fx + fw]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(os.path.join(output_folder, f"face_{timestamp}_{i}.jpg"), face_img)

    else:
        # Si aucun visage n'est détecté, dézoomer progressivement
        if zoom_factor > min_zoom:
            zoom_factor -= zoom_step
        faces_detected = []

        # Alerte si aucun visage n'est détecté pendant plus de 5 secondes
        if last_detection_time and (datetime.now() - last_detection_time).total_seconds() > 2:
            alert_sound.play()  # Jouer une alerte sonore
            cv2.putText(zoomed_frame, "Alerte : Aucun visage detecte !", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Afficher l'image zoomée avec les annotations
    cv2.imshow('Face Detection and Tracking', zoomed_frame)

    # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et fermer les fenêtres
video_capture.release()
cv2.destroyAllWindows()