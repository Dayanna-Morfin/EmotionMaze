import cv2
import mediapipe as mp
import math


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def distance(point1, point2):
    """Calcula la distancia entre dos puntos."""
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )


# ============================================================
# MEDIA PIPE
# ============================================================

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ============================================================
# CÁMARA
# ============================================================

# IMPORTANTE:
# Cambia este número por el índice de TU cámara externa.
camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print("Cámara externa iniciada.")
print("Presiona Q para salir.")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: No se pudo leer la cámara.")
        break

    # Imagen tipo espejo
    frame = cv2.flip(frame, 1)

    # Convertir BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detectar rostro
    results = face_mesh.process(rgb_frame)


    # ========================================================
    # SI ENCONTRAMOS UN ROSTRO
    # ========================================================

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        landmarks = face_landmarks.landmark


        # ----------------------------------------------------
        # PUNTOS DEL ROSTRO
        # ----------------------------------------------------

        # Boca
        mouth_left = landmarks[61]
        mouth_right = landmarks[291]

        mouth_top = landmarks[13]
        mouth_bottom = landmarks[14]


        # Ojo izquierdo
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]


        # Ojo derecho
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]


        # Tamaño aproximado de la cara
        face_left = landmarks[234]
        face_right = landmarks[454]

        face_width = distance(
            face_left,
            face_right
        )


        # ----------------------------------------------------
        # MEDIDAS
        # ----------------------------------------------------

        mouth_width = distance(
            mouth_left,
            mouth_right
        )

        mouth_height = distance(
            mouth_top,
            mouth_bottom
        )

        mouth_width_ratio = mouth_width / face_width

        left_eye_height = distance(
            left_eye_top,
            left_eye_bottom
        )

        right_eye_height = distance(
            right_eye_top,
            right_eye_bottom
        )

        # ----------------------------------------------------
        # CEJAS
        # ----------------------------------------------------

        # Ceja izquierda y parte superior del ojo izquierdo
        left_eyebrow = landmarks[105]
        left_eye_upper = landmarks[159]

        # Ceja derecha y parte superior del ojo derecho
        right_eyebrow = landmarks[334]
        right_eye_upper = landmarks[386]

        left_eyebrow_distance = distance(
            left_eyebrow,
            left_eye_upper
        )

        right_eyebrow_distance = distance(
            right_eyebrow,
            right_eye_upper
        )

        eyebrow_ratio = (
            left_eyebrow_distance +
            right_eyebrow_distance
        ) / (2 * face_width)


        # Normalizamos las medidas
        mouth_ratio = mouth_height / face_width

        eye_ratio = (
            left_eye_height +
            right_eye_height
        ) / (2 * face_width)

        # ----------------------------------------------------
        # CLASIFICACIÓN DE EXPRESIONES
        # ----------------------------------------------------

        expression = "NEUTRAL"

        # ----------------------------------------------------
        # 1. BOCA ABIERTA
        # ----------------------------------------------------
        # Si la boca tiene una apertura vertical grande,
        # consideramos que el usuario está haciendo una
        # expresión de boca abierta.

        if mouth_ratio > 0.15:

            expression = "BOCA ABIERTA"


        # ----------------------------------------------------
        # 2. OJOS CERRADOS
        # ----------------------------------------------------
        # Cuando ambos ojos presentan una apertura muy pequeña.

        elif eye_ratio < 0.02:

            expression = "OJOS CERRADOS"


        # ----------------------------------------------------
        # 3. SONRISA
        # ----------------------------------------------------
        # Una sonrisa aumenta el ancho de la boca,
        # pero no debería producir una apertura vertical
        # tan grande como una boca completamente abierta.

        elif (
            mouth_width_ratio > 0.38
            and mouth_ratio > 0.025
        ):

            expression = "SONRISA"

        # ----------------------------------------------------
        # 4. CEJAS LEVANTADAS
        # ----------------------------------------------------

        elif eyebrow_ratio > 0.265:

            expression = "CEJAS LEVANTADAS"

        # ----------------------------------------------------
        # MOSTRAR EXPRESIÓN
        # ----------------------------------------------------

        cv2.putText(
            frame,
            f"EXPRESION: {expression}",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )


        # Mostrar valores para poder calibrarlos
        cv2.putText(
            frame,
            f"Boca: {mouth_ratio:.3f}",
            (20, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Boca ancho: {mouth_width_ratio:.3f}",
            (20, 145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Cejas: {eyebrow_ratio:.3f}",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Ojos: {eye_ratio:.3f}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        # Dibujar landmarks
        mp_drawing.draw_landmarks(
            frame,
            face_landmarks,
            mp_face_mesh.FACEMESH_TESSELATION
        )


    else:

        cv2.putText(
            frame,
            "BUSCANDO ROSTRO...",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )


    # ========================================================
    # MOSTRAR CÁMARA
    # ========================================================

    cv2.imshow(
        "Emotion Maze - Expression Test",
        frame
    )


    # Q = salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CERRAR
# ============================================================

camera.release()
cv2.destroyAllWindows()
face_mesh.close()