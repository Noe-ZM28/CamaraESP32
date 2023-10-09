from process_image.get_frame import GetFrameFromImage
from process_image.process_frame import ProcessFrame
from process_image.process_text import CleanData

import cv2

# Color verde
color_green = (0, 255, 0)

# Color rojo
color_red = (0, 0, 255)

# Grosor de la línea del rectángulo
thickness = 2

# Definir las dimensiones deseadas del ROI
roi_width = 400
roi_height = 600

def run(path_image, show_process, show_plate):
    p_frame = ProcessFrame()
    clean = CleanData()
    frame_class = GetFrameFromImage()

# while True: 

    frame = frame_class.get_frame(path_image)

    # Obtener las dimensiones del frame
    frame_height, frame_width, _ = frame.shape

    if frame is None:
        return

    # Calcular las coordenadas para que el ROI esté en el centro del frame
    x_roi = (frame_width - roi_width) // 2  # Resta la mitad del ROI al ancho del frame
    y_roi = (frame_height - roi_height) // 2  # Resta la mitad del ROI a la altura del frame

    # Recortar el frame al área del ROI
    roi = frame[y_roi:y_roi + roi_height, x_roi:x_roi + roi_width]

    contours, frame_proceed = p_frame.process_frame(roi, show_process)

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

            # Dibujar el rectángulo del área de la placa
            cv2.rectangle(frame, (x-5, y-5), (x + w+5, y + h+5), color_green, thickness)

            # Dibujar el rectángulo del area de interes
            cv2.rectangle(frame, (x_roi, y_roi), (x_roi + roi_width, y_roi + roi_height), color_red, thickness)


            # Se actualiza valor
            real_txt_plate = clean_txt_plate

            # Dibujar el texto de la placa sobre el recuadro rojo
            cv2.putText(frame, f'Texto: {real_txt_plate}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_green, 2)

            print("Ancho: ",w)
            print("Alto: ",h)
            print("Relación: ",aspect_ratio)
            print("Placa: ",real_txt_plate)
            rectangle_detected = True

    # Mostrar el frame con el recuadro rojo, rectángulos y el texto de las placas
    cv2.imshow('ESP32 CAM', frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

show_process_frame = True
show_plate = True
path_image= 'img/plates/8.jpg'

run(path_image, show_process_frame, show_plate)



