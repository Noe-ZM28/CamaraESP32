import cv2
import pytesseract

# Cargar el video desde el archivo (ajusta la ruta según tu archivo)
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

reader = pytesseract.image_to_string

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el frame a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Aplicar la detección de bordes con Canny
    edges = cv2.Canny(blurred_frame, threshold1=50, threshold2=150)

    # Encontrar los contornos en el frame
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Recorrer los contornos en busca de rectángulos
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        # Si el contorno tiene cuatro vértices (rectángulo)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)

            # Descartar rectángulos muy pequeños
            if w > 150 and h > 20:
                # Recortar y procesar el área de la placa
                plate_image = gray_frame[y:y + h, x:x + w]

                # Aplicar OCR con Tesseract al área de la placa
                plate_text = reader(plate_image, config='--psm 8')

                # Dibujar el rectángulo del área de la placa en el frame original
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Dibujar el texto de la placa en el frame original
                cv2.putText(frame, 'Placa: ' + plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar el frame con los rectángulos y el texto de las placas
    cv2.imshow('Video con Placas', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
