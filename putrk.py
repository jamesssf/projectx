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
    # Warm up
    time.sleep(0.1)
    # Loop pupil detection and print webcam
    framecount = 0
    ax = 0
    ay = 0
    ar = 0
    #capture the camera
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Take each image from the webcam
        img = frame.array

        ####TEST CODE####
        #ret_val, img = cam.read()
        #grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #ret_val1, img1 = cam.read()
        #grey_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #img_diff = cv2.subtract(grey_img, grey_img1)
        #result = not numpy.any(img_diff)

        # run pupil detection algorithm
        fcrds = pupildetect(img)
        print(str(fcrds[0]) + " " + str(fcrds[1]) + str(fcrds[2]))
        if fcrds[0] != 0 and fcrds[1] != 0 and fcrds[2] != 0:
            cv2.imwrite(img, filename="img" + str(framecount))
            framecount+=1
        # quit the webcam at esc
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        rawCapture.truncate(0)

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
                                   param1=10, param2=30, minRadius=30, maxRadius=7-)
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
        return avx, avy, avr
    # sometimes there are no circles detected and the program poops
    # out not quite sure how to stop it, there's got to be a way to
    # skip something if no circles are detected, fix later
    except:
        return 0, 0, 0

def main():
    crds()

if __name__ == '__main__':
        main()