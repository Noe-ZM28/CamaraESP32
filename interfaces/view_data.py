import os
import sys

# Obtener el directorio raíz del proyecto
proyecto_dir = os.getcwd()
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(proyecto_dir)

import cv2
from tkinter import Tk, Button, Label, LabelFrame
from PIL import Image, ImageTk
from process_image import get_frame, tools, process_frame, process_text
from enum import Enum

class_get_image = get_frame.GetFrameFromImage()
class_process_frame = process_frame.ProcessFrame()
clean = process_text.CleanData()
tools_instance =  tools.Tools()

# Color verde
color_green = (0, 255, 0)

# Color rojo
color_red = (255, 0, 0)

# Grosor de la línea del rectángulo
thickness = 2

# Definir las dimensiones deseadas del ROI
roi_width = 150
roi_height = 300

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class panel_config:
    def __init__(self) -> None:
        self.list_images = tools_instance.list_images()
        self.long_list_number = len(self.list_images) - 1
        # Crear la ventana principal
        self.root = Tk()
        self.root.title("OpenCV y Tkinter")
    
        main_frame = LabelFrame(self.root, text="Principal")
        main_frame.grid(row = 0, column = 0, pady = 5)

        image_frame = LabelFrame(main_frame, text="Imagen")
        image_frame.grid(row = 0, column = 0, pady = 5)

        self.image = Label(image_frame)
        self.image.grid(row = 0, column = 0)

        config_frame = LabelFrame(main_frame,text="Configuración")
        config_frame.grid(row = 0, column = 1, pady = 5)

        boton_cargar = Button(config_frame, text="Siguiente ->", command=lambda:self.next_image(Direction.FORWARD))
        boton_cargar.grid(row = 0, column = 0, pady = 5)
        boton_cargar = Button(config_frame, text="<- Anterior", command=lambda:self.next_image(Direction.BACKWARD))
        boton_cargar.grid(row = 1, column = 0, pady = 5)

        self.load_image(self.list_images[0])
        self.number_image = -1

        self.root.mainloop()


    def resize_image(self, frame, scale:int = 2):
        new_high = int(self.frame_height // scale)
        new_width = int(self.frame_width // scale)

        # Redimensionar la imagen
        return cv2.resize(frame, (new_width, new_high))

    # Función para mostrar una imagen en un widget Tkinter
    def show_image(self, frame):
        cv2.imshow('IMAGEN CV2', frame)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.image.config(image=frame)
        self.image.image = frame

    # Función para cargar una imagen usando OpenCV
    def load_image(self, img:str = './img/tools/none_image.jpg', show_plate:bool = False):
        frame = class_get_image.get_frame(img)
        if frame is None:
            return

        self.frame_height, self.frame_width = frame.shape[:2]

        frame = self.resize_image(frame, 1)

        # Calcular las coordenadas para que el ROI esté en el centro del frame
        x_roi = (self.frame_width - roi_width) // 2  # Resta la mitad del ROI al ancho del frame
        y_roi = (self.frame_height - roi_height) // 2  # Resta la mitad del ROI a la altura del frame

        contours, frame_proceed = class_process_frame.process_frame(frame)

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

        self.show_image(frame)

    def next_image(self, direction: Direction):
        self.number_image += direction.value
        if self.number_image > self.long_list_number:
            self.number_image = 0

        if self.number_image < 0:
            self.number_image = self.long_list_number

        self.load_image(self.list_images[self.number_image])


a = panel_config()
# a.run()

