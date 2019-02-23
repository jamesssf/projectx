import cv2
import numpy
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

def crds():
    # Capture the camera feed
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32
    rawCapture = PiRGBArray(cam, size=(640,480))
    # Open the file to write coordinates
    file = open("vals.txt","w")
    # Warm up camera
    time.sleep(0.1)
    #capture the camera
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Take each image from the picamera
        img = frame.array
        # run pupil detection algorithm
        fcrds = pupildetect(img)
        # Print the position and radius of the pupil  x, y, r
        print(str(fcrds[1]) + " " + str(fcrds[0]) + " " + str(fcrds[2]))
        # Write the location of pupil in vars.txt
        file.write(str(fcrds[1]) + ", " + str(fcrds[0]) + ", " + str(fcrds[2]) + "\n")
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
