import cv2

from face_controller import FaceController, expression_to_command


print("Emotion Maze iniciado.")
print("Presiona Q para salir.")


controller = FaceController(camera_index=1)


while True:

    expression, frame = controller.get_expression()


    # --------------------------------------------------------
    # EXPRESIÓN
    # --------------------------------------------------------

    if expression is None:

        expression_text = "SIN ROSTRO"
        command = None

    else:

        expression_text = expression
        command = expression_to_command(expression)


    # --------------------------------------------------------
    # TEXTO DE EXPRESIÓN
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"EXPRESION: {expression_text}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    # --------------------------------------------------------
    # TEXTO DE COMANDO
    # --------------------------------------------------------

    if command is not None:

        cv2.putText(
            frame,
            f"COMANDO: {command}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "COMANDO: ---",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


    # --------------------------------------------------------
    # MOSTRAR CÁMARA
    # --------------------------------------------------------

    cv2.imshow(
        "Emotion Maze - Controller Test",
        frame
    )


    # --------------------------------------------------------
    # SALIR
    # --------------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


controller.release()
cv2.destroyAllWindows()

print("Programa terminado.")