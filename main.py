from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

# --- Cấu hình GPIO cho servo ---
servo_pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM với tần số 50Hz (servo chuẩn)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

# --- Hàm điều khiển servo theo góc ---
def set_servo_angle(angle):
    duty = 2 + (angle / 18)  # Tính duty cycle từ góc 0-180
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

# --- Flask App ---
app = Flask(__name__)

@app.route("/")
def index():
    # Trang web có form nhập góc servo
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    angle = int(request.form["angle"])
    if 0 <= angle <= 180:
        set_servo_angle(angle)
        return f"Servo đã quay tới góc {angle}°"
    else:
        return "Góc phải nằm trong khoảng 0-180°"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        pwm.stop()
        GPIO.cleanup()
