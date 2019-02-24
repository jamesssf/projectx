import cv2
import numpy
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import epd2in13d
from PIL import Image, ImageDraw, ImageFont
import textwrap
import RPi.GPIO as GPIO
from subprocess import call

GPIO.setmode(GPIO.BCM)
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
    while True:
        print("ProjectX Testing Utility\n"
              "1: Turn on the lights\n"
              "2: Begin Pupil Tracking Test\n"
              "3: Exit")
        lights = GPIO.input(27)  # status of lights
        inp = input()
        if inp == "3":
            print("Exit")
            break
        if inp == "2":
            time.sleep(0.2)
            crds()
        if inp == "1":
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



def crds():
    epd = epd2in13d.EPD()
    index = 0
    epd.init()
    epd.Clear(0xFF)
    text = book()
    print("Running Pupil Tracking\nGenerating New Page")
    index = write_to_display(text, index, epd)
    # Capture the camera feed
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32
    rawCapture = PiRGBArray(cam, size=(640,480))
    # Open the file to write coordinates
    file = open("vals.txt","w")
    # Warm up camera
    time.sleep(0.1)
    crdtrk = numpy.zeroes(2)
    i = 0
    #capture the camera
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Take each image from the picamera
        img = frame.array
        # run pupil detection algorithm
        crdtrk[i] = pupildetect(img)
        # Print the position and radius of the pupil  x, y, r
        print(str(crdtrk[i][1]) + " " + str(crdtrk[i][0]) + " " + str(crdtrk[i][2]))
        # Write the location of pupil in vars.txt
        file.write(str(crdtrk[i][1]) + ", " + str(crdtrk[i][0]) + ", " + str(crdtrk[i][2]) + "\n")
        if i >= 20:
            errcnt = 0
            for crd in crdtrk:
                if crd[0] > 317 or crd[0] < 270 or crd[1] > 134 or crd[1] < 122:
                    errcnt += 1
                if errcnt > 2:
                    break
            if errcnt <= 2:
                index = write_to_display(text, index, epd)
        # quit the webcam at esc
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        rawCapture.truncate(0)
    file.close()

# Pupil detection algorithm
# Img, the source of the image
# returns the webcam image with
# hough circles printed on it
def pupildetect(img):
    # Blurs the image to make it easier to detect
    blur_img = cv2.medianBlur(img, 5)
    # Turn the image greyscale
    grey_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
    # Binary threshold (source, threshold, white color, type)
    # Currently using trunc that turns values over threshold pure white
    ret, thresh_img = cv2.threshold(grey_img, 60, 255, cv2.THRESH_TRUNC)
    image = cv2.add(thresh_img, numpy.array([50.0]))
    try:
        # Create hough cricles
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=10, param2=30, minRadius=40, maxRadius=55)
        circles = numpy.uint16(numpy.around(circles))
        # Holds a group of circles to find an average
        # find average circle positions
        xgroup = numpy.zeros(1)
        ygroup = numpy.zeros(1)
        rgroup = numpy.zeros(1)
        j = 0
        for i in circles[0, :]:
            xgroup[j] = i[0]
            ygroup[j] = i[1]
            rgroup[j] = i[2]
        avx = numpy.uint16(numpy.around(numpy.average(xgroup)))
        avy = numpy.uint16(numpy.around(numpy.average(ygroup)))
        avr = numpy.uint16(numpy.around(numpy.average(rgroup)))
        draw(image, avx, avy, avr)
        return avx, avy, avr
    # sometimes there are no circles detected and the program poops
    # out not quite sure how to stop it, there's got to be a way to
    # skip something if no circles are detected, fix later
    except:
        return 0, 0, 0

# Draw the circle on the pupil image and save it
def draw(img, x, y, r):
    # draw the outer circle
    cv2.circle(img, (x, y), r, (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(img, (x, y), 2, (0, 0, 255), 3)
    cv2.imwrite("img" + str(r) + "_"+str(y)+"_"+str(x) + ".bmp", img)

def main():
    crds()

if __name__ == '__main__':
        main()
