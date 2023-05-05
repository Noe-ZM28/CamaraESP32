import cv2
import numpy as np
from urllib.request import urlopen
from PIL import Image, ImageTk
import tkinter as tk

class StreamIP():
    def __init__(self, ip):
        self.ip = ip
        self.url = F"http://{self.ip}:81/stream"

        # Crea la ventana principal de Tkinter
        self.root = tk.Tk()
        self.root.title("Stream IP")

        # Crea un widget Label para mostrar la imagen
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Abre el stream de video
        self.stream = urlopen(self.url)
        self.bytes = bytes()

        # Programa la actualización inicial de la imagen
        self.root.after(0, self.update_image)

        # Inicia el bucle principal de Tkinter
        self.root.mainloop()

        # Cierra el stream de video al salir del bucle principal
        self.stream.close()

    # Función para actualizar la imagen en el widget Label
    def update_image(self):
        largo = self.stream._get_chunk_left()
        self.bytes += self.stream.read(1024)
        a = self.bytes.find(b'\xff\xd8')
        b = self.bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            if jpg:
                # Convierte la imagen en formato OpenCV a formato PIL
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                # Convierte la imagen PIL a formato Tkinter PhotoImage
                tk_img = ImageTk.PhotoImage(pil_img)
                # Actualiza la imagen en el widget Label
                self.image_label.configure(image=tk_img)
                self.image_label.image = tk_img
        # Programa la actualización de la imagen después de 1 ms
        self.root.after(1, self.update_image)




