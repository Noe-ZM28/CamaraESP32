import cv2
import pytesseract

# Cargar el video desde el archivo 
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

reader = pytesseract.image_to_string

real_plate=None

PLATES = ["A-522-JME", "A522JME", "A 522 JME"]

while cap.isOpened():
    plate = ""
    ret, frame = cap.read()
    if not ret:
        print("error")
        continue
        #break

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
            if w < h:
                # print("es mas largo que ancho")
                continue

            # Descartar rectángulos muy pequeños y los que sean más largos que anchos
            aspect_ratio = w / float(h)
            if (w > 150 and h > 50) and (aspect_ratio <= 2.5) and (aspect_ratio >= 0.5):
                # Recortar y procesar el área de la placa
                plate_image = gray_frame[y:y + h, x:x + w]

                # Aplicar OCR con Tesseract al área de la placa
                plate_text = reader(plate_image, config='--psm 8')
                long_plate_text = len(plate_text)

                if long_plate_text < 5:
                    continue

                # Dibujar el rectángulo del área de la placa en el frame original
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Dibujar el texto de la placa en el frame original
                cv2.putText(frame, 'Placa: ' + plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if plate_text in PLATES:
                    print("*"*50)
                    print("Funciona!")
                print(plate_text)

    # Redimensionar el frame para mostrarlo en una ventana más pequeña
    resized_frame = cv2.resize(frame, (640, 480))

    # Mostrar el frame redimensionado con los rectángulos y el texto de las placas
    cv2.imshow('Video con Placas', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


