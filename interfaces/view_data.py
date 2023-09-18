import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from process_image import get_frame

class_get_image = get_frame.GetFrameFromImage()

class panel_config:
    # Función para cargar una imagen usando OpenCV
    def cargar_imagen(self):
        img = './img/1.jpg'
        frame = class_get_image.get_frame(img)
        self.mostrar_imagen(frame)

    # Función para mostrar una imagen en un widget Tkinter
    def mostrar_imagen(self, imagen):
        imagen = Image.fromarray(imagen)
        imagen = ImageTk.PhotoImage(imagen)
        self.label_imagen.config(image=imagen)
        self.label_imagen.image = imagen

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("OpenCV y Tkinter")

    # Botón para cargar una imagen
    boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
    boton_cargar.pack()

    # Etiqueta para mostrar la imagen
    label_imagen = tk.Label(ventana)
    label_imagen.pack()

    ventana.mainloop()

