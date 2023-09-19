import os
import sys

# Obtener el directorio raíz del proyecto
proyecto_dir = os.getcwd()
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(proyecto_dir)

import cv2
from tkinter import Tk, Button, Label, LabelFrame, Frame, Scale
from PIL import Image, ImageTk
from process_image import get_frame, tools, process_frame, process_text
from enum import Enum

class_get_image = get_frame.GetFrameFromImage()
class_process_frame = process_frame.ProcessFrame()
clean = process_text.CleanData()
tools_instance =  tools.Tools()

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class panel_config:
    def __init__(self) -> None:

        # Definir las dimensiones deseadas del ROI
        self.roi_width = 150
        self.roi_height = 300

        # Color verde
        self.color_green = (0, 255, 0)

        # Color rojo
        self.color_red = (255, 0, 0)

        # Grosor de la línea del rectángulo
        self.thickness = 2

        self.number_image = 0

        self.real_txt_plate = "N/E"

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

        frame_botones = Frame(config_frame)
        frame_botones.grid(row = 0, column = 0, pady = 5)

        boton_cargar = Button(frame_botones, text="<- Anterior", command=lambda:self.next_image(Direction.BACKWARD))
        boton_cargar.grid(row = 0, column = 0, pady = 5)
        boton_cargar = Button(frame_botones, text="Siguiente ->", command=lambda:self.next_image(Direction.FORWARD))
        boton_cargar.grid(row = 0, column = 1, pady = 5)

        frame_data_config= Frame(config_frame)
        frame_data_config.grid(row = 1, column = 0, pady = 5)

        roi_scale = Scale(frame_data_config, from_=10, to=500, label="Tamaño ROI", orient="horizontal", command=self.update_roi_size)
        roi_scale.set(self.roi_width)  # Establece el valor inicial del tamaño del ROI
        roi_scale.grid(row=0, column=0, padx=10, pady=10)

        # Muestra la escala del ROI en una etiqueta
        self.scale_label = Label(frame_data_config, text=f'Scala ROI: {self.roi_width}')
        self.scale_label.grid(row=1, column=0)

        # Muestra el texto de la placa en una etiqueta
        self.plate_label = Label(frame_data_config, text=f'Texto de la placa: {self.real_txt_plate}')
        self.plate_label.grid(row=2, column=0)

        self.update_roi_size(self.roi_width)

        self.load_image(self.list_images[self.number_image])

        self.root.mainloop()

    def update_roi_size(self, new_size):
        self.roi_width = int(new_size)
        self.roi_height = int(new_size)
        self.load_image(self.list_images[self.number_image])
        self.scale_label.config(text = f'Scala ROI: {new_size}')

    def resize_image(self, frame, frame_height, frame_width,scale:int = 2):
        new_high = int(frame_height // scale)
        new_width = int(frame_width // scale)

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
        original_frame = class_get_image.get_frame(img)
        if original_frame is None:
            return

        self.frame_height, self.frame_width = original_frame.shape[:2]

        resize_frame = self.resize_image(original_frame, self.frame_height, self.frame_width, 1)

        # Calcular las coordenadas para que el ROI esté en el centro del frame
        x_roi = (self.frame_width - self.roi_width) // 2  # Resta la mitad del ROI al ancho del frame
        y_roi = (self.frame_height - self.roi_height) // 2  # Resta la mitad del ROI a la altura del frame

        # Recortar el frame al área del ROI
        ROI_frame = resize_frame[y_roi:y_roi + self.roi_height, x_roi:x_roi + self.roi_width]

        contours, frame_proceed = class_process_frame.process_frame(ROI_frame)

        # Dibujar el rectángulo del área de interés (ROI) en el frame original
        cv2.rectangle(original_frame, (x_roi, y_roi), (x_roi + self.roi_width, y_roi + self.roi_height), self.color_red, self.thickness)

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

            # Descargar rectángulos pequeños
            # if (w > 150 and h > 50):continue

            if(aspect_ratio <= 3) and (aspect_ratio > 2):
                # Recortar y procesar el área de la placa
                plate_image = frame_proceed[y-5:y + h+5, x-5:x + w+5]

                txt_plate = clean.image_to_txt(plate_image)

                if txt_plate[0].islower():
                    continue

                #Si la cantidad de letras detectadas es menor a 7 o la cantidad de guines es menor a 1 pasa al siguiente Frame 
                if len(txt_plate) < 7 or txt_plate.count("-") < 1:
                    continue
                if show_plate:
                    cv2.imshow('plate_image', plate_image)
                clean_txt_plate = clean.remove_strange_caracteres(txt_plate)

                # Dibujar el rectángulo del área de la placa en el frame original
                cv2.rectangle(original_frame, (x_roi + x-5, y_roi + y-5), (x_roi + x + w+5, y_roi + y + h+5), self.color_green, self.thickness)

                # Se actualiza valor
                self.real_txt_plate = clean_txt_plate
                self.plate_label.config(text = f'Texto de la placa: {self.real_txt_plate}')

                # Dibujar el texto de la placa sobre el recuadro rojo
                cv2.putText(original_frame, f'Texto: {self.real_txt_plate}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.color_green, 2)

                print("Ancho: ",w)
                print("Alto: ",h)
                print("Relación: ",aspect_ratio)
                print("Placa: ",self.real_txt_plate)
                rectangle_detected = True

        self.show_image(original_frame)

    def next_image(self, direction: Direction):
        self.number_image += direction.value
        if self.number_image > self.long_list_number:
            self.number_image = 0

        if self.number_image < 0:
            self.number_image = self.long_list_number

        self.load_image(self.list_images[self.number_image])


a = panel_config()
# a.run()
