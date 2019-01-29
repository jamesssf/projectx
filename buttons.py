import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True:
    input_state_7 = GPIO.input(7)  # Bottom Button
    if input_state_7:
        print("Exit")