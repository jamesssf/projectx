import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True:
    input_state_23 = GPIO.input(23)  # Bottom Button
    if input_state_23:
        print("Exit")