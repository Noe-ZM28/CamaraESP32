import os
import sys

# Obtener el directorio raíz del proyecto
proyecto_dir = os.getcwd()
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(proyecto_dir)

import cv2
from tkinter import Tk, Button, Label, LabelFrame
from PIL import Image, ImageTk
from process_image import get_frame, tools
from enum import Enum

class_get_image = get_frame.GetFrameFromImage()
tools_instance =  tools.Tools()

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

        self.load_image()
        self.number_image = -1

        self.root.mainloop()


    def resize_image(self, frame, scale:int|float = 2):
        frame_height, frame_width, _ = frame.shape
        new_high = int(frame_height // scale)
        new_width = int(frame_width // scale)

        # Redimensionar la imagen
        return cv2.resize(frame, (new_width, new_high))

    # Función para mostrar una imagen en un widget Tkinter
    def show_image(self, frame):
        new_frame = self.resize_image(frame)
        frame = Image.fromarray(new_frame)
        frame = ImageTk.PhotoImage(frame)
        self.image.config(image=frame)
        self.image.image = frame

    # Función para cargar una imagen usando OpenCV
    def load_image(self, img:str = './img/tools/none_image.jpg'):
        frame = class_get_image.get_frame(img)
        if frame is None:
            return
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

