import cv2
from urllib.request import urlopen
import numpy as np

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
