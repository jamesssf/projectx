# -*- coding: utf-8 -*-

import epd2in13d
from PIL import Image, ImageDraw, ImageFont
import traceback
import textwrap
import time


def book():
    book_file = open('sample.txt', 'r')
    book = book_file.read()
    book_text = textwrap.wrap(book, 30) # word wraps for the size of font and screen

    return book_text


def write_to_display(text, index_counter, epd):
    draw_counter = 0    # Determines the Y coordinate where to draw the line on the screen
    line_counter = 1    # Determines how many lines to read
    image = Image.new('1', (epd2in13d.EPD_HEIGHT, epd2in13d.EPD_WIDTH), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 12)
    for line in text[index_counter:]:   # iterate through the text
        if line_counter < 7:
            draw.text((2, draw_counter), line, font=font, fill=0)
            index_counter += 1
            draw_counter += 14
            line_counter += 1
    draw.text((0, 92), 'MENU', font=font, fill=0)
    draw.text((184, 92), 'EXIT', font=font, fill=0)
    epd.display(epd.getbuffer(image))

    return index_counter    # Keeps track of the index from the list


def main():
    epd = epd2in13d.EPD()
    index = 0
    epd.init()
    epd.Clear(0xFF)
    option = input("next page = 0\n"
                   "exit = 1\n: ")
    text = book()
    while option < 1:
        if option == 0:
            index = write_to_display(text, index, epd)
            option = int(input("Turn the page? "))
    epd.init()
    epd.Clear(0xFF)

main()
