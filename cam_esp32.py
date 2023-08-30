import cv2
import pytesseract

# Cargar la imagen desde el archivo
image = cv2.imread('a.jpg')

# Convertir la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro gaussiano para reducir el ruido y mejorar la detección del texto
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Aplicar la detección de bordes con Canny
edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

# Encontrar los contornos en la imagen
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Recorrer los contornos en busca de rectángulos
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    
    # Si el contorno tiene cuatro vértices (rectángulo)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        
        # Descartar rectángulos muy pequeños (ajusta este valor según tus necesidades)
        if w > 100 and h > 20:
            # Recortar y procesar el área de la placa
            plate_image = gray_image[y:y + h, x:x + w]
            
            # Aplicar OCR con Tesseract al área de la placa
            plate_text = pytesseract.image_to_string(plate_image, config='--psm 8')
            
            # Dibujar el rectángulo del área de la placa en la imagen original
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Dibujar el texto de la placa en la imagen original
            cv2.putText(image, 'Placa: ' + plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Mostrar la imagen con los rectángulos y el texto de las placas
cv2.imshow('Imagen con Placas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
