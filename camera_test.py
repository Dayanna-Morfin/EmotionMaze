import cv2

# Abrir la cámara
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print("Cámara detectada correctamente.")
print("Presiona Q para cerrar.")

while True:
    # Leer un frame
    success, frame = camera.read()

    if not success:
        print("ERROR: No se pudo leer la cámara.")
        break

    # Mostrar la imagen
    cv2.imshow("Prueba de camara - Emotion Maze", frame)

    # Presionar Q para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar la cámara
camera.release()
cv2.destroyAllWindows()