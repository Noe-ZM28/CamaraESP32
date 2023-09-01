import cv2
from urllib.request import urlopen
import numpy as np
import pytesseract
 
stream = urlopen('http://192.168.1.227:81/stream')

reader = pytesseract.image_to_string

real_txt_plate = None

PLATES = ["A-522-JME", "LD-73-546", "LF-55-593"]

window_size = (1040, 680)

rect_width = 600
rect_height = 300


bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        if jpg :
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)


            # Dimensiones y posición del recuadro rojo en el centro
            rect_x = (frame.shape[1] - rect_width) // 2
            rect_y = (frame.shape[0] - rect_height) // 2

            # Dibujar el recuadro rojo en el centro del frame
            cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

            # Redimensionar el frame para mostrarlo en una ventana más pequeña
            resized_frame = cv2.resize(frame, window_size)

            # Mostrar el frame con el recuadro rojo, rectángulos y el texto de las placas
            cv2.imshow('ESP32 CAM', resized_frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
stream.release()
cv2.destroyAllWindows()