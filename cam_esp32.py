import cv2
from urllib.request import urlopen
import numpy as np
from numpy import ndarray
from pytesseract import image_to_string

class ProcessFrame:
    """Clase para procesar frames de imagen."""
    def process_frame(self, frame: ndarray, show: bool = False) -> list:
        """
        Procesa un frame de imagen para mejorar la detección de texto.

        Args:
            frame (ndarray): El frame de imagen a procesar.
            show (bool): Indica si mostrar ventanas de depuración.

        Returns:
            list: Contornos encontrados y frame procesado.
        """
        # Convertir el área de interés a escala de grises
        gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
        blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

        # Aplicar un filtro de nitidez para mejorar la nitidez de la imagen
        sharpened_roi = cv2.filter2D(blurred_roi, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
        frame_proceed = sharpened_roi

        # Aplicar la detección de bordes con Canny
        edges = cv2.Canny(sharpened_roi, threshold1=100, threshold2=200)

        # Encontrar los contornos en el área de interés
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if show:
            cv2.imshow('Original', 1)
            cv2.imshow('Escala de Grises', 2)
            cv2.imshow('Filtro Gaussiano', 3)
            cv2.imshow('Filtro de Nitidez', 4)
            cv2.imshow('Detección de Bordes', 5)

        return contours, frame_proceed

class CleanData:
    """Clase para limpiar datos de texto."""
    def remove_strange_caracteres(self, txt_to_clean: str, strange_caracteres: str = "|[]{}()") -> str:
        """
        Elimina caracteres extraños de una cadena de texto.

        Args:
            txt_to_clean (str): La cadena de texto a limpiar.
            strange_caracteres (str): Caracteres extraños a eliminar.

        Returns:
            str: La cadena de texto sin caracteres extraños.
        """
        # Crear una tabla de traducción que mapea cada carácter a None (eliminar)
        tablae_traduction = str.maketrans("", "", strange_caracteres)

        return txt_to_clean.translate(tablae_traduction)

    def image_to_txt(self, image: np.ndarray, config: str = '--psm 8', line_break: bool = True) -> str:
        """
        Convierte una imagen en texto utilizando OCR (Optical Character Recognition).

        Args:
            image (np.ndarray): La imagen de entrada.
            config (str): Opciones de configuración para el OCR.
            line_break (bool): Indica si agregar un salto de línea al resultado.

        Returns:
            str: El texto extraído de la imagen.
        """
        try:
            # Aplicar OCR con Tesseract al área de la placa
            txt = image_to_string(image, config=config)

            # Se convierte la respuesta de Tesseract a texto y se eliminan los saltos de línea u otros caracteres especiales, así como espacios en blanco
            txt_image = str(txt).strip().replace(" ", "")

            return txt_image + "\n" if line_break else txt_image

        except Exception as e:
            return "None"

class GetFrame:
    """Clase para obtener frames de video desde una URL."""

    def __init__(self, url:str) -> str:
        """
        Inicializa la instancia de GetFrame.

        Args:
            url (str): La URL del video de la que se obtendrán los frames.
        """
        self.stream = urlopen(url)

    def get_frame(self, bytes_buffer):
        """
        Obtiene un frame de video desde una URL.

        Args:
            bytes_buffer: Un búfer de bytes para almacenar datos.

        Returns:
            tuple: El frame de imagen y el búfer de bytes actualizado.
        """
        try:
            bytes_buffer += self.stream.read(1024)
            a = bytes_buffer.find(b'\xff\xd8')
            b = bytes_buffer.find(b'\xff\xd9')

            if a == -1 or b == -1:
                return None, bytes_buffer

            jpg = bytes_buffer[a:b+2]
            bytes_buffer = bytes_buffer[b+2:]

            if not jpg:
                return None, bytes_buffer

            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            return frame, bytes_buffer
        except Exception as e:
            print(f"Error al obtener el cuadro de la URL: {str(e)}")
            return None, bytes_buffer


def run(url, show_process, show_plate):
    p_frame = ProcessFrame()
    clean = CleanData()
    frame_class = GetFrame(url)
    bytes_buffer = bytes()

    while True:
        frame, bytes_buffer = frame_class.get_frame(bytes_buffer)

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

show_process_frame = True
show_plate = True
ip = "192.168.1.160"
ip = "192.168.1.227"
URL = f'http://{ip}:81/stream'

run(URL, show_process_frame, show_plate)
