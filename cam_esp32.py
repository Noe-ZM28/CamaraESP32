import cv2
import pytesseract

# Cargar la imagen desde el archivo
image = cv2.imread('a.jpg')

# Coordenadas del rectángulo (p1: esquina superior izquierda, p2: esquina inferior derecha)
p1 = (100, 100)
p2 = (300, 300)

# Recortar el área del rectángulo
cropped_area = image[p1[1]:p2[1], p1[0]:p2[0]]

# Convertir el área recortada a escala de grises
gray_cropped = cv2.cvtColor(cropped_area, cv2.COLOR_BGR2GRAY)

# Aplicar OCR con Tesseract
texto_extraido = pytesseract.image_to_string(gray_cropped)

# Mostrar el texto extraído
print("Texto extraído:", texto_extraido)
