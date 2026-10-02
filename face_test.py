import cv2
import mediapipe as mp

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Abrir cámara
camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print("Cámara iniciada.")
print("Buscando rostro...")
print("Presiona Q para cerrar.")

while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: No se pudo leer la cámara.")
        break

    # Voltear la imagen para que funcione como espejo
    frame = cv2.flip(frame, 1)

    # OpenCV utiliza BGR y MediaPipe necesita RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostro
    results = face_mesh.process(rgb_frame)

    # Si encontramos un rostro
    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # Dibujar los puntos del rostro
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION
            )

        cv2.putText(
            frame,
            "ROSTRO DETECTADO",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "BUSCANDO ROSTRO...",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # Mostrar cámara
    cv2.imshow(
        "Emotion Maze - Face Detection",
        frame
    )

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cerrar todo
camera.release()
cv2.destroyAllWindows()
face_mesh.close()