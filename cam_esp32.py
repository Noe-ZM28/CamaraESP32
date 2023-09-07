import cv2
from urllib.request import urlopen
import numpy as np
from pytesseract import image_to_string
 
url = 'http://192.168.1.160:81/stream'
stream = urlopen(url)
real_txt_plate = None
bytes = bytes()

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')

    if a == -1 and b == -1:
        continue

    jpg = bytes[a:b+2]
    bytes = bytes[b+2:]

    if not jpg:
        continue

    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Convertir el área de interés a escala de grises
    gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
    blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

    # Aplicar un filtro de nitidez para mejorar la nitidez de la imagen
    sharpened_roi = cv2.filter2D(blurred_roi, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))

    # Aplicar la detección de bordes con Canny
    edges = cv2.Canny(sharpened_roi, threshold1=100, threshold2=200)

    # Encontrar los contornos en el área de interés
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variable para rastrear si se ha detectado un rectángulo en este frame
    rectangle_detected = False

    # Recorrer los contornos en busca de rectángulos
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if rectangle_detected:
            break  # Salir del bucle si ya se ha detectado un rectángulo

        # Si el contorno tiene cuatro vértices (rectángulo)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)

        if w < h:
            continue

        aspect_ratio = w / float(h)

        # Descargar rectangulos pequeños
        # if (w > 150 and h > 50):continue

        if(aspect_ratio <= 3) and (aspect_ratio > 2):
            # Recortar y procesar el área de la placa
            plate_image = gray_roi[y:y + h, x:x + w]

            # Aplicar OCR con Tesseract al área de la placa
            plate_text = image_to_string(plate_image, config='--psm 8')

            # Se convierte la respuesta de Tesseract a texto y  se eliminan los saltos de linea o u utros caracteres especiales
            txt_plate = str(plate_text).strip()

            long_plate_text = len(txt_plate)

            #Si la cantidad de letras detectadas es menor a 7 pasa al siguiene Frame
            if long_plate_text < 7:
                continue

            # Dibujar el rectángulo del área de la placa en el recuadro rojo
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Se actualiza valor
            real_txt_plate = txt_plate

            # Dibujar el texto de la placa sobre el recuadro rojo
            cv2.putText(frame, f'Texto: {real_txt_plate}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            print("Ancho: ",w)
            print("Alto: ",h)
            print("Relación: ",aspect_ratio)
            print("Placa: ",real_txt_plate+"\n")
            rectangle_detected = True

    # Mostrar el frame con el recuadro rojo, rectángulos y el texto de las placas
    cv2.imshow('ESP32 CAM', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break



