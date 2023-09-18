import os
import sys

# Obtener el directorio raíz del proyecto
proyecto_dir = os.getcwd()
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(proyecto_dir)

import cv2
from tkinter import Tk, Button, Label, LabelFrame
from PIL import Image, ImageTk
from process_image import get_frame

class_get_image = get_frame.GetFrameFromImage()

class panel_config:
    def __init__(self) -> None:
        # Crear la ventana principal
        self.root = Tk()
        self.root.title("OpenCV y Tkinter")
    
        main_frame = LabelFrame(self.root, text="Principal")
        main_frame.grid(row = 0, column = 0, pady = 5)

        image_frame = LabelFrame(main_frame, text="Imagen")
        image_frame.grid(row = 0, column = 0, pady = 5)

        self.image = Label(image_frame)
        self.image.grid(row = 0, column = 0)
        self.load_image()

        config_frame = LabelFrame(main_frame,text="Configuración")
        config_frame.grid(row = 0, column = 1, pady = 5)

        boton_cargar = Button(config_frame, text="Cargar Imagen")
        boton_cargar.grid()

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



    # def run(self):

    #     # Botón para cargar una imagen
    #     boton_cargar = Button(self.root, text="Cargar Imagen", command=self.load_image)
    #     boton_cargar.grid()

    #     # Etiqueta para mostrar la imagen
    #     self.label_imagen = Label(self.root)
    #     self.label_imagen.grid()

        self.root.mainloop()

a = panel_config()
# a.run()

