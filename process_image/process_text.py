import cv2
import numpy as np
from pytesseract import image_to_string

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
            print(e)
            return "None"

