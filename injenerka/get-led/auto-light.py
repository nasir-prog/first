import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
led=26
GPIO.setup(led, GPIO.OUT)
auto = 6
state=0
GPIO.setup(auto,GPIO.IN)
while True:
    if GPIO.input(auto)==0:
        GPIO.output(led,1)
    else:
        GPIO.output(led,0)
        

