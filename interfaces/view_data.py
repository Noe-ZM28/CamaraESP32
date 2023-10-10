import os
import sys

# Obtener el directorio raíz del proyecto
proyecto_dir = os.getcwd()
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(proyecto_dir)

import cv2
from tkinter import Tk, Toplevel, Button, Label, LabelFrame, Frame, Scale, NSEW
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

        self.font = ("Arial", 16)

        # Definir las dimensiones deseadas del ROI
        self.roi_width = 360
        self.roi_height = 260

        # Definir las coordenadas iniciales del ROI
        self.roi_x = 500
        self.roi_y = 150

        self.frame_height = 100
        self.frame_width = 100

        # Color verde
        self.color_green = (0, 255, 0)

        # Color rojo
        self.color_red = (255, 0, 0)

        # Grosor de la línea del rectángulo
        self.thickness = 2

        self.number_image = 0

        self.real_txt_plate = "S/P"

        self.list_images = tools_instance.list_images()
        self.long_list_number = len(self.list_images) - 1
        # Crear la ventana principal
        self.root = Tk()
        self.root.title("OpenCV y Tkinter")
        self.interface()
        self.root.mainloop()

    def interface(self):
        main_frame = LabelFrame(self.root, text="Principal")
        main_frame.grid(row = 0, column = 0, pady = 5)

        image_frame = LabelFrame(main_frame, text="Imagen")
        image_frame.grid(row = 0, column = 0, pady = 5)

        self.image = Label(image_frame)
        self.image.grid(row = 0, column = 0)

        self.root_config = Toplevel()
        self.root_config.title("Configuración")

        config_frame = LabelFrame(self.root_config,text="Configuración")
        config_frame.grid(row = 0, column = 0, pady = 5)

        frame_placa = Frame(config_frame)
        frame_placa.grid(row = 0, column = 0, pady = 5)

        # Muestra el texto de la placa en una etiqueta
        self.plate_label = Label(frame_placa, text=f'Texto de la placa: {self.real_txt_plate}', font=self.font)
        self.plate_label.grid(row=0, column=0, sticky=NSEW)

        self.load_image(self.list_images[self.number_image])

        frame_botones = LabelFrame(config_frame,text="Datos")
        frame_botones.grid(row = 1, column = 0, pady = 5)

        boton_cargar = Button(frame_botones, text="<- Anterior", command=lambda:self.next_image(Direction.BACKWARD), font=self.font)
        boton_cargar.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        boton_cargar = Button(frame_botones, text="Siguiente ->", command=lambda:self.next_image(Direction.FORWARD), font=self.font)
        boton_cargar.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=NSEW)

        frame_data_config= Frame(config_frame)
        frame_data_config.grid(row = 2, column = 0, pady = 5)

        # Controles deslizantes para ajustar el ancho y alto del ROI
        self.roi_scale_width = Scale(frame_data_config, from_=10, to=self.frame_width, label="Ancho ROI", orient="horizontal", command=self.update_roi_width_size, font=self.font, length=300, resolution=25)
        self.roi_scale_width.set(self.roi_width)  # Establece el valor inicial del ancho del ROI
        self.roi_scale_width.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        self.roi_scale_height = Scale(frame_data_config, from_=10, to=self.frame_height, label="Alto ROI", orient="horizontal", command=self.update_roi_height_size, font=self.font, length=300, resolution=25)
        self.roi_scale_height.set(self.roi_height)  # Establece el valor inicial del alto del ROI
        self.roi_scale_height.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        # Controles deslizantes para ajustar la posición horizontal (X) y vertical (Y) del ROI
        self.roi_scale_x = Scale(frame_data_config, from_=0, to=self.frame_width, label="Posición X", orient="horizontal", command=self.update_roi_x_position, font=self.font, length=300, resolution=25)
        self.roi_scale_x.set(self.roi_x)  # Establece el valor inicial de la posición X del ROI
        self.roi_scale_x.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        self.roi_scale_y = Scale(frame_data_config, from_=0, to=self.frame_height, label="Posición Y", orient="horizontal", command=self.update_roi_y_position, font=self.font, length=300, resolution=25)
        self.roi_scale_y.set(self.roi_y)  # Establece el valor inicial de la posición Y del ROI
        self.roi_scale_y.grid(row=3, column=0, padx=10, pady=10, sticky=NSEW)

        # Muestra la escala del ROI en una etiqueta
        self.scale_label = Label(frame_data_config, text=f'Scala ROI: \n Ancho: {self.roi_width}, Alto: {self.roi_height},\nX: {self.roi_x}, Y: {self.roi_y}', width=20, font=self.font)
        self.scale_label.grid(row=4, column=0, sticky=NSEW)



    def update_roi_width_size(self, new_size):
        self.roi_width = int(new_size)
        self.load_image(self.list_images[self.number_image])
        self.scale_label.config(text = f'Scala ROI: \n Ancho: {new_size}, Alto: {self.roi_height},\nX: {self.roi_x}, Y: {self.roi_y}')

    def update_roi_height_size(self, new_size):
        self.roi_height = int(new_size)
        self.load_image(self.list_images[self.number_image])
        self.scale_label.config(text = f'Scala ROI: \n Ancho: {self.roi_width}, Alto: {new_size},\nX: {self.roi_x}, Y: {self.roi_y}')

    def update_roi_x_position(self, new_position):
        self.roi_x = int(new_position)
        self.load_image(self.list_images[self.number_image])
        self.scale_label.config(text = f'Scala ROI: \n Ancho: {self.roi_width}, Alto: {self.roi_height},\nX: {new_position}, Y: {self.roi_y}')

    def update_roi_y_position(self, new_position):
        self.roi_y = int(new_position)
        self.load_image(self.list_images[self.number_image])
        self.scale_label.config(text = f'Scala ROI: \n Ancho: {self.roi_width}, Alto: {self.roi_height},\nX: {self.roi_x}, Y: {new_position}')

    def resize_image(self, frame, frame_height, frame_width,scale:int = 1):
        new_high = int(frame_height // scale)
        new_width = int(frame_width // scale)

        # Redimensionar la imagen
        return cv2.resize(frame, (new_width, new_high))

    # Función para mostrar una imagen en un widget Tkinter
    def show_image(self, frame):
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.image.config(image=frame)
        self.image.image = frame

    # Función para cargar una imagen usando OpenCV
    def load_image(self, img:str = './img/tools/none_image.jpg'):
        self.None_plate()
        original_frame = class_get_image.get_frame(img)
        if original_frame is None:
            self.None_plate()
            return

        self.frame_height, self.frame_width = original_frame.shape[:2]

        resize_frame = self.resize_image(original_frame, self.frame_height, self.frame_width)

        frame_height, frame_width = original_frame.shape[:2]
        original_frame = self.resize_image(original_frame, frame_height, frame_width)

        # Calcular las coordenadas para el ROI
        x_roi = self.roi_x
        y_roi = self.roi_y

        # Recortar el frame al área del ROI
        ROI_frame = resize_frame[y_roi:y_roi + self.roi_height, x_roi:x_roi + self.roi_width]

        data_image_proced = class_process_frame.process_frame(frame= ROI_frame)

        if data_image_proced is None:
            self.None_plate()
            return

        contours, frame_proceed = data_image_proced

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
                self.None_plate()
                continue

            x, y, w, h = cv2.boundingRect(approx)

            if w < h:
                self.None_plate()
                continue

            aspect_ratio = w / float(h)

            # Descargar rectángulos pequeños
            # if (w > 150 and h > 50):continue

            if(aspect_ratio > 3) and (aspect_ratio < 2):
                self.None_plate()
                continue

            # Recortar y procesar el área de la placa
            plate_image = frame_proceed[y-5:y + h+5, x-5:x + w+5]

            txt_plate = clean.image_to_txt(plate_image)

            if txt_plate == "None" or txt_plate[0].islower() or len(txt_plate) < 7 or txt_plate.count("-") < 1:
                self.None_plate()
                continue

            clean_txt_plate = clean.remove_strange_caracteres(txt_plate)

            # Dibujar el rectángulo del área de la placa en el frame original
            cv2.rectangle(original_frame, (x_roi + x, y_roi + y), (x_roi + x + w, y_roi + y + h), self.color_green, self.thickness)

            # Se actualiza valor
            self.real_txt_plate = clean_txt_plate
            self.plate_label.config(text = f'Texto de la placa: {self.real_txt_plate}')

            # Dibujar el texto de la placa sobre el recuadro rojo
            cv2.putText(original_frame, f'Texto: {self.real_txt_plate}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.color_green, 2)

            print("Ancho: ",w)
            print("Alto: ",h)
            print("Relación: ",aspect_ratio)
            print(f"Placa: {self.get_plate_text()}")
            rectangle_detected = True

        self.show_image(original_frame)

    def next_image(self, direction: Direction):
        self.number_image += direction.value
        if self.number_image > self.long_list_number:
            self.number_image = 0

        if self.number_image < 0:
            self.number_image = self.long_list_number

        self.load_image(self.list_images[self.number_image])
    
    def None_plate(self):
        self.real_txt_plate = "S/P"
        self.plate_label.config(text = f'Texto de la placa: {self.real_txt_plate}')
    
    def get_plate_text(self):
        return self.real_txt_plate


a = panel_config()
# a.load_image('/home/pi/Documentos/WORKSPACE/CamaraESP32/img/plates/2.jpg')
# print(a.get_plate_text())

