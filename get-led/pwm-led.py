import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 26

GPIO.setup(led, GPIO.OUT)

pwm = GPIO.PWM(led, 400)
duty = 0.0

pwm.start(duty)

while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)
    duty += 1.0

    if duty > 100:
        duty = 0.0