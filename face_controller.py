import cv2
import mediapipe as mp
import math


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )


# ============================================================
# CONTROLADOR FACIAL
# ============================================================

class FaceController:

    def __init__(self, camera_index=1):

        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            raise RuntimeError(
                "No se pudo abrir la cámara."
            )

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )


    # ========================================================
    # LEER CÁMARA Y DETECTAR EXPRESIÓN
    # ========================================================

    def get_expression(self):

        success, frame = self.camera.read()

        if not success:
            return None, None

        # Imagen espejo
        frame = cv2.flip(frame, 1)

        # BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(
            rgb_frame
        )

        # ----------------------------------------------------
        # NO HAY ROSTRO
        # ----------------------------------------------------

        if not results.multi_face_landmarks:
            return None, frame


        face_landmarks = results.multi_face_landmarks[0]

        landmarks = face_landmarks.landmark


        # ====================================================
        # PUNTOS DEL ROSTRO
        # ====================================================

        # Boca
        mouth_left = landmarks[61]
        mouth_right = landmarks[291]

        mouth_top = landmarks[13]
        mouth_bottom = landmarks[14]


        # Ojos
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]

        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]


        # Tamaño de la cara
        face_left = landmarks[234]
        face_right = landmarks[454]

        face_width = distance(
            face_left,
            face_right
        )


        # ====================================================
        # MEDICIONES
        # ====================================================

        mouth_width = distance(
            mouth_left,
            mouth_right
        )

        mouth_height = distance(
            mouth_top,
            mouth_bottom
        )

        mouth_width_ratio = (
            mouth_width / face_width
        )


        left_eye_height = distance(
            left_eye_top,
            left_eye_bottom
        )

        right_eye_height = distance(
            right_eye_top,
            right_eye_bottom
        )


        # ====================================================
        # CEJAS
        # ====================================================

        left_eyebrow = landmarks[105]
        left_eye_upper = landmarks[159]

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


        # ====================================================
        # RATIOS
        # ====================================================

        mouth_ratio = (
            mouth_height / face_width
        )

        eye_ratio = (
            left_eye_height +
            right_eye_height
        ) / (2 * face_width)


        # ====================================================
        # CLASIFICACIÓN
        # ====================================================

        expression = "NEUTRAL"


        # 1. Boca abierta
        if mouth_ratio > 0.15:

            expression = "BOCA ABIERTA"


        # 2. Ojos cerrados
        elif eye_ratio < 0.02:

            expression = "OJOS CERRADOS"


        # 3. Sonrisa
        elif (
            mouth_width_ratio > 0.38
            and mouth_ratio > 0.025
        ):

            expression = "SONRISA"


        # 4. Cejas levantadas
        elif eyebrow_ratio > 0.265:

            expression = "CEJAS LEVANTADAS"


        return expression, frame


    # ========================================================
    # CERRAR
    # ========================================================

    def release(self):

        self.camera.release()
        self.face_mesh.close()


# ============================================================
# CONVERTIR EXPRESIÓN EN COMANDO
# ============================================================

def expression_to_command(expression):

    if expression == "SONRISA":
        return "RIGHT"

    elif expression == "BOCA ABIERTA":
        return "UP"

    elif expression == "OJOS CERRADOS":
        return "DOWN"

    elif expression == "CEJAS LEVANTADAS":
        return "LEFT"

    return None