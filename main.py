# -*- coding: utf-8 -*-

import epd2in13d
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time
import RPi.GPIO as GPIO
from subprocess import call


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)


def book():
    book_open = open('/home/pi/projectx/sample.txt', 'r')
    book_file = book_open.read()
    book_text = textwrap.wrap(book_file, 30)  # word wraps for the size of font and screen

    return book_text


def write_to_display(text, index_counter, epd):
    draw_counter = 0  # Determines the Y coordinate where to draw the line on the screen
    line_counter = 1  # Determines how many lines to read
    image = Image.new('1', (epd2in13d.EPD_HEIGHT, epd2in13d.EPD_WIDTH), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/georgia.ttf', 12)
    for line in text[index_counter:]:  # iterate through the text
        if line_counter < 7:
            draw.text((2, draw_counter), line, font=font, fill=0)
            index_counter += 1
            draw_counter += 14
            line_counter += 1
    draw.text((0, 92), 'MENU', font=font, fill=0)
    draw.text((184, 92), 'EXIT', font=font, fill=0)
    epd.display(epd.getbuffer(image))

    return index_counter  # Keeps track of the index from the list


def main():
    epd = epd2in13d.EPD()
    index = 0
    epd.init()
    epd.Clear(0xFF)
    text = book()

    while True:
        lights = GPIO.input(27)  # status of lights
        input_state_7 = GPIO.input(36)  # Bottom Button
        input_state_18 = GPIO.input(38)  # Middle Button
        input_state_23 = GPIO.input(40)  # Top Button DONT REPROGRAM
        if not input_state_7:
            print("Exit")
            break
        if not input_state_18:
            print("Turning Page")
            index = write_to_display(text, index, epd)
            time.sleep(0.2)
        if not input_state_23:
            if lights == 0:
                print("Lights on")
                GPIO.output(27, GPIO.HIGH)
            else:
                print("Lights off")
                GPIO.output(27, GPIO.LOW)
            time.sleep(0.2)

    epd.init()
    epd.Clear(0xFF)
    GPIO.output(27, GPIO.LOW)
    call("sudo shutdown -h now", shell=True)


main()
