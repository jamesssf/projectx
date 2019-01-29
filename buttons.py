from gpiozero import LED, Button
from time import sleep

led = LED(27)
button = Button(23)
led.on()
sleep(5)
led.off()
button.wait_for_press()
led.on()
sleep(3)
led.off()