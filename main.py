import RPi.GPIO as GPIO
import time

def led_sequence():
    # Danh sách chân LED
    leds = [17, 18, 27, 22, 23]
    
    # Cài đặt GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for led in leds:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)
    
    try:
        while True:
            # Bật LED từ 1 đến 5
            for led in leds:
                GPIO.output(led, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(led, GPIO.LOW)
            
            # Bật LED từ 5 về 1
            for led in reversed(leds):
                GPIO.output(led, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(led, GPIO.LOW)
                
    except KeyboardInterrupt:
        # Tắt tất cả LED khi ngắt chương trình
        for led in leds:
            GPIO.output(led, GPIO.LOW)
        GPIO.cleanup()
        print("Chương trình kết thúc.")

# Gọi hàm
led_sequence()
