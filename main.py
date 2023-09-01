import cv2
import pytesseract

class LicensePlateDetector:
    def __init__(self, video_path: str):
        """
        Inicializa el detector de placas de matrícula.

        Args:
            video_path (str): Ruta al video a procesar.
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.reader = pytesseract.image_to_string
        self.real_txt_plate = None
        self.window_size = (1040, 680)
        self.rect_width = 600
        self.rect_height = 300

    def process_frame(self, frame):
        """
        Procesa un marco de video en busca de placas de matrícula.

        Args:
            frame: El marco de video a procesar.

        Returns:
            frame: El marco con las detecciones y texto de placas.
        """
        plate_text = ""
        rect_x = (frame.shape[1] - self.rect_width) // 2
        rect_y = (frame.shape[0] - self.rect_height) // 2

        # Dibuja un rectángulo en el centro del marco para buscar la placa
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + self.rect_width, rect_y + self.rect_height), (0, 0, 255), 2)

        # Extrae la región de interés (ROI) dentro del rectángulo
        roi = frame[rect_y:rect_y + self.rect_height, rect_x:rect_x + self.rect_width]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        edges = cv2.Canny(blurred_roi, threshold1=100, threshold2=200)
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangle_detected = False

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if rectangle_detected:
                break

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if w < h:
                    continue

                aspect_ratio = w / float(h)
                if (w > 150 and h > 50) and (aspect_ratio <= 2.5) and (aspect_ratio >= 1):
                    # Extrae la imagen de la placa y realiza OCR para obtener el texto
                    plate_image = gray_roi[y:y + h, x:x + w]
                    plate_text = self.reader(plate_image, config='--psm 8')
                    long_plate_text = len(plate_text)

                    if long_plate_text < 8:
                        continue

                    # Dibuja un rectángulo alrededor de la placa y muestra el texto en el marco
                    cv2.rectangle(frame, (rect_x + x, rect_y + y), (rect_x + x + w, rect_y + y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f'Placa: {plate_text}', (rect_x, rect_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    self.real_txt_plate = plate_text
                    print(plate_text)
                    rectangle_detected = True

        return frame

    def run(self):
        """
        Ejecuta el proceso de detección de placas en el video.
        Muestra el video procesado en una ventana.
        """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("termino video")
                break

            processed_frame = self.process_frame(frame)
            resized_frame = cv2.resize(processed_frame, self.window_size)
            cv2.imshow('Video con Placas', resized_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_plate_text(self):
        """
        Obtiene el texto de la última placa detectada.

        Returns:
            str: Texto de la placa de matrícula.
        """
        return self.real_txt_plate

if __name__ == "__main__":
    video_path = 'videos/v4.mp4'  # Selecciona el video que deseas procesar
    detector = LicensePlateDetector(video_path)
    detector.run()
