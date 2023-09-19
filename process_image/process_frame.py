import cv2
import numpy as np
from numpy import ndarray

class ProcessFrame:
    """Clase para procesar frames de imagen."""
    def process_frame(self,
            frame: ndarray,
            show: bool = False,
            count_gasussian = 1,
            sharpen_kernel: ndarray = np.array([[-1, -1, -1],
                                                [-1, 9, -1],
                                                [-1, -1, -1]]),
            canny_threshold1: int = 100, 
            canny_threshold2: int = 200) -> list:
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

        if count_gasussian > 1:
            for i in range(count_gasussian):
                blurred_roi = cv2.GaussianBlur(blurred_roi, (5, 5), 0)


        # Aplicar un filtro de nitidez para mejorar la nitidez de la imagen
        sharpened_roi = cv2.filter2D(blurred_roi, -1, sharpen_kernel)
        frame_proceed = sharpened_roi

        # Aplicar la detección de bordes con Canny
        edges = cv2.Canny(sharpened_roi, threshold1=canny_threshold1, threshold2=canny_threshold2)

        # Encontrar los contornos en el área de interés
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if show:
            cv2.imshow('Original', frame)
            cv2.imshow('Escala de Grises', gray_roi)
            cv2.imshow('Filtro Gaussiano', blurred_roi)
            cv2.imshow('Filtro de Nitidez', sharpened_roi)
            cv2.imshow('Detección de Bordes', edges)

        return contours, frame_proceed


