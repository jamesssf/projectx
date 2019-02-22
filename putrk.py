import cv2
import numpy
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

# crds

def crds():


# Uses the Hough Transform
# To find the position of the pupil,
# Takes the average of all pupils detected
# in a single frame
# return avx, avy, avr
# avx, avy - The averagehorizontal and vertical position
# of the pupil as detected
# avr - the radius of the detected circle
# Returns all zeros if there is no circle detected.
def pupildetect(img):
    # Blurs the image to make it easier to detect
    blur_img = cv2.medianBlur(img, 5)
    # Turn the image greyscale
    grey_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
    # Binary threshold (source, threshold, white color, type)
    # Currently using trunc that turns values over threshold pure white
    ret, thresh_img = cv2.threshold(grey_img, 60, 255, cv2.THRESH_TRUNC)
    # image = cv2.add(thresh_img, numpy.array([50.0]))
    try:
        # Create hough cricles
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=10, param2=30, minRadius=50, maxRadius=75)
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
    # Capture the camera feed
    cam = PiCamera()
    # count the images
    pcount = 0
    # Lower this to increase performance?
    cam.resolution = (640, 480)
    cam.framerate = 32
    rawCapture = PiRGBArray(cam, size=(640,480))
    # Warm up
    time.sleep(0.1)
    #capture the camera
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Capture the image from the picamera
        img = frame.array
        # run pupil detection algorithm
        fcrds = pupildetect(img)
        # print the position and radius of the pupil
        print(str(fcrds[0]) + " " + str(fcrds[1]) + str(fcrds[2]))
        if fcrds[0] != 0 and fcrds[1] != 0 and fcrds[2] != 0:
            cv2.imwrite(img, filename="file"+ str(pcount) + ".jpg")
            pcount += 1
        # quit the webcam at esc
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        rawCapture.truncate(0)

if __name__ == '__main__':
        main()