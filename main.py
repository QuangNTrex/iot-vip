import cv2
import RPi.GPIO as GPIO
import time

# --- Cấu hình GPIO ---
led_pins = [17, 18, 27, 22, 23]  # 5 LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# --- Load Haar cascade để nhận diện khuôn mặt ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# --- Mở camera ---
cap = cv2.VideoCapture(0)  # 0 = camera mặc định (Pi Camera hoặc USB)

if not cap.isOpened():
    print("Không mở được camera!")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không nhận được hình ảnh!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Nhận diện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_count = len(faces)

        # Giới hạn tối đa 5
        if face_count > 5:
            face_count = 5

        # Bật LED theo số lượng khuôn mặt
        for i, pin in enumerate(led_pins):
            if i < face_count:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)

        # Hiển thị hình ảnh kèm khung khuôn mặt
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Detection", frame)

        # Nhấn q để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Dừng chương trình...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
