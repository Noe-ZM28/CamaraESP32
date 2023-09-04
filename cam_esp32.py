from cv2 import imdecode, IMREAD_COLOR, COLOR_BGR2GRAY, cvtColor, GaussianBlur, filter2D, Canny, findContours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, arcLength, approxPolyDP, boundingRect, rectangle, putText, FONT_HERSHEY_SIMPLEX, imshow, waitKey, destroyAllWindows

from urllib.request import urlopen
import numpy as np
import pytesseract
#Reemplazar por la ip
url = "http://192.168.1.160:81/stream"

stream = urlopen(url)

reader = pytesseract.image_to_string

real_txt_plate = None

rect_width = 175
rect_height = 100

rect_x = 75
rect_y = 100

bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        if not jpg:
            continue
        frame = imdecode(np.frombuffer(jpg, dtype=np.uint8), IMREAD_COLOR)
        gray_roi = cvtColor(frame, COLOR_BGR2GRAY)
        blurred_roi = GaussianBlur(gray_roi, (5, 5), 0)
        sharpened_roi = filter2D(blurred_roi, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
        edges = Canny(sharpened_roi, threshold1=100, threshold2=200)
        contours, _ = findContours(edges.copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        rectangle_detected = False
        for contour in contours:
            perimeter = arcLength(contour, True)
            approx = approxPolyDP(contour, 0.04 * perimeter, True)
            if rectangle_detected:break
            if len(approx) != 4:continue
            x, y, w, h = boundingRect(approx)
            if w < h:continue

            aspect_ratio = w / float(h)
            if (w > 150 and h > 50) and (aspect_ratio <= 2.5) and (aspect_ratio >= 1):
                plate_image = gray_roi[y:y + h, x:x + w]
                plate_text = reader(plate_image, config='--psm 8')
                long_plate_text = len(plate_text)
                if long_plate_text < 5:
                    continue
                rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                putText(frame, f'Texto: {plate_text}', (rect_x, rect_y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                real_txt_plate = str(plate_text)

                print(real_txt_plate)
                rectangle_detected = True
        imshow('ESP32 CAM', frame)
    if waitKey(1) & 0xFF == ord('q'):break #Precionar Q para salir

destroyAllWindows()

