import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#print(cv2.__version__)

# Leer la imagen de la placa del auto
img = cv2.imread('c.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro de umbralización adaptativa para obtener una imagen binaria
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Encontrar contornos en la imagen binaria
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Buscar el contorno que corresponde a la placa del auto
plate_contour = None
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    if len(approx) == 4:
        plate_contour = approx
        break

# Recortar la imagen de la placa del auto utilizando el contorno
x, y, w, h = cv2.boundingRect(plate_contour)
plate_img = img[y:y+h, x:x+w]

# Aplicar OCR (reconocimiento óptico de caracteres) a la imagen de la placa del auto
text = ''
for i in range(1, 7):
    # Recortar cada caracter de la placa y aplicar OCR
    char_img = plate_img[:, (i-1)*w//6:i*w//6]

    char_img = plate_img[:, (i-1)*w//6:i*w//6]
    if not char_img.size:
        continue
    char_gray = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)

    char_thresh = cv2.threshold(char_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    char_text = pytesseract.image_to_string(char_thresh, config='--psm 10')
    text += char_text.strip()

print(f'Texto de la placa del auto: {text}')

# crear entorno virtual con virtualenv

# #########################
# instalar opencv y pytesseract

# sudo apt-get python3-opencv
# sudo apt-get install tesseract-ocr
# sudo apt-get install tesseract-ocr-spa
# pip3 install pytesseract

# ##########################
# instalar pytesseract



# instalar los requerimientos

# pip install requirements.txt




# import numpy as np
# import cv2

# # Cargamos la imagen
# img = cv2.imread('d.jpg')

# # Convertimos la imagen a espacio de color HSV
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # Definimos los rangos de color de la pelota
# lower_red = np.array([0, 50, 50])
# upper_red = np.array([10, 255, 255])

# # Creamos una máscara utilizando el rango de color definido
# mask = cv2.inRange(hsv, lower_red, upper_red)

# # Aplicamos una serie de transformaciones morfológicas para eliminar ruido en la máscara
# kernel = np.ones((5,5),np.uint8)
# mask = cv2.erode(mask, kernel, iterations = 2)
# mask = cv2.dilate(mask, kernel, iterations = 2)

# # Buscamos contornos en la máscara
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Dibujamos los contornos encontrados en la imagen original
# for c in contours:
#     area = cv2.contourArea(c)
#     if area > 100:
#         x,y,w,h = cv2.boundingRect(c)
#         cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

# # Mostramos la imagen original con los contornos detectados
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
