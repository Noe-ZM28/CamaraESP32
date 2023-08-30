import cv2
import pytesseract

# Cargar la imagen desde el archivo
image = cv2.imread('c.jpg')

# Convertir la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Aplicar la detección de bordes con Canny
edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

# Encontrar los contornos en la imagen
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ordenar los contornos por área de mayor a menor
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Inicializar una variable para el contorno de la placa
plate_contour = None

# Recorrer los contornos en busca de la placa
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    if len(approx) == 4:
        plate_contour = approx
        break

# Si se encontró el contorno de la placa
if plate_contour is not None:
    # Dibujar el contorno de la placa en la imagen original
    cv2.drawContours(image, [plate_contour], -1, (0, 255, 0), 2)
    
    # Recortar y procesar el área de la placa
    x, y, w, h = cv2.boundingRect(plate_contour)
    plate_image = gray_image[y:y + h, x:x + w]
    
    # Aplicar OCR con Tesseract al área de la placa
    plate_text = pytesseract.image_to_string(plate_image, config='--psm 8')
    
    # Imprimir el texto de la placa
    print("Texto de la placa:", plate_text)
    
    # Mostrar la imagen con el contorno y el texto de la placa
    cv2.imshow('Placa con Contorno y Texto', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No se pudo encontrar la placa en la imagen.")
