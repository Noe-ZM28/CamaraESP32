from process_image.get_frame import GetFrame
from process_image.process_frame import ProcessFrame
from process_image.process_text import CleanData

import cv2

def run(url, show_process, show_plate):
    p_frame = ProcessFrame()
    clean = CleanData()
    frame_class = GetFrame(url=url)
    bytes_buffer = bytes()

    while True:
        frame, bytes_buffer = frame_class.get_frame_from_url(bytes_buffer)

        if frame is None:
            continue

        contours, frame_proceed = p_frame.process_frame(frame, show_process)

        # Variable para rastrear si se ha detectado un rectángulo en este frame
        rectangle_detected = False

        # Recorrer los contornos en busca de rectángulos
        for contour in contours:
            if rectangle_detected:
                break  # Salir del bucle si ya se ha detectado un rectángulo

            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

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
                plate_image = frame_proceed[y-5:y + h+5, x-5:x + w+5]

                txt_plate = clean.image_to_txt(plate_image)

                if txt_plate[0].islower():
                    continue

                #Si la cantidad de letras detectadas es menor a 7 o la cantidad de guines es menor a 1 pasa al siguiene Frame 
                if len(txt_plate) < 7 or txt_plate.count("-") < 1:
                    continue
                if show_plate:
                    cv2.imshow('plate_image', plate_image)
                clean_txt_plate = clean.remove_strange_caracteres(txt_plate)

                # Dibujar el rectángulo del área de la placa en el recuadro rojo
                cv2.rectangle(frame, (x-5, y-5), (x + w+5, y + h+5), (0, 255, 0), 2)

                # Se actualiza valor
                real_txt_plate = clean_txt_plate

                # Dibujar el texto de la placa sobre el recuadro rojo
                cv2.putText(frame, f'Texto: {real_txt_plate}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                print("Ancho: ",w)
                print("Alto: ",h)
                print("Relación: ",aspect_ratio)
                print("Placa: ",real_txt_plate)
                rectangle_detected = True

        # Mostrar el frame con el recuadro rojo, rectángulos y el texto de las placas
        cv2.imshow('ESP32 CAM', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

show_process_frame = False
show_plate = True
ip = "192.168.1.160"
# ip = "192.168.1.227"
URL = f'http://{ip}:81/stream'

run(URL, show_process_frame, show_plate)
