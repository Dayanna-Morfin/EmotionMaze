import cv2

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("ERROR: No se pudo abrir la cámara USB.")
    exit()

print("Camara USB iniciada correctamente.")
print("Presiona Q para cerrar.")

while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: No se pudo obtener imagen.")
        break

    frame = cv2.flip(frame, 1)

    cv2.putText(
        frame,
        "CAMARA USB",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Emotion Maze - Camara USB", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()