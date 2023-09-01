import cv2
import pytesseract
import requests
import numpy as np

# URL de la cámara ESP32
camera_url = 'http://192.168.1.227/'

reader = pytesseract.image_to_string

window_size = (1040, 680)

rect_width = 600
rect_height = 300

while True:
    try:
        response = requests.get(camera_url, stream=True)
        if response.status_code == 200:
            bytes_data = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # Dimensiones y posición del recuadro rojo en el centro
                    rect_x = (frame.shape[1] - rect_width) // 2
                    rect_y = (frame.shape[0] - rect_height) // 2

                    # Dibujar el recuadro rojo en el centro del frame
                    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

                    # Recortar el área de interés (rectángulo rojo) de la imagen
                    roi = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]

                    # Convertir el área de interés a escala de grises
                    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                    # Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
                    blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

                    # Aplicar la detección de bordes con Canny
                    edges = cv2.Canny(blurred_roi, threshold1=100, threshold2=200)

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
                        if len(approx) == 4:
                            x, y, w, h = cv2.boundingRect(approx)

                            if w < h:
                                continue

                            # Descartar rectángulos muy pequeños y los que sean más largos que anchos
                            aspect_ratio = w / float(h)
                            if (w > 150 and h > 50) and (aspect_ratio <= 2.5) and (aspect_ratio >= 1):
                                # Recortar y procesar el área de la placa
                                plate_image = gray_roi[y:y + h, x:x + w]

                                # Aplicar OCR con Tesseract al área de la placa
                                plate_text = reader(plate_image, config='--psm 8')
                                long_plate_text = len(plate_text)

                                #Si la cantidad de letras detectadas es menor a 8 pasa al siguiene Frame
                                if long_plate_text < 8:
                                    continue

                                # Dibujar el rectángulo del área de la placa en el recuadro rojo
                                cv2.rectangle(frame, (rect_x + x, rect_y + y), (rect_x + x + w, rect_y + y + h), (0, 255, 0), 2)

                                # Dibujar el texto de la placa sobre el recuadro rojo
                                cv2.putText(frame, f'Placa: {plate_text}', (rect_x, rect_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                real_txt_plate = plate_text

                                print(plate_text)
                                rectangle_detected = True

                    # Redimensionar el frame para mostrarlo en una ventana más pequeña
                    resized_frame = cv2.resize(frame, window_size)

                    # Mostrar el frame con el recuadro rojo, rectángulos y el texto de las placas
                    cv2.imshow('Video con Placas', resized_frame)
                    print("muestra video")

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    except Exception as e:
        print("Error:", e)
        cv2.destroyAllWindows()


