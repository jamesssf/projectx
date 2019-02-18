import cv2
import numpy

def crds():
    # Capture the camera feed
    cam = cv2.VideoCapture('test6.h264')
    # Loop pupil detection and print webcam
    framecount = 0
    frameav = 1
    ax = 0
    ay = 0
    ar = 0
    while True:
        # Take each image from the webcam
        ret_val, img, = cam.read()

        ####TEST CODE####
        #ret_val, img = cam.read()
        #grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #ret_val1, img1 = cam.read()
        #grey_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        #img_diff = cv2.subtract(grey_img, grey_img1)
        #result = not numpy.any(img_diff)

        # run pupil detection algorithm
        fcrds = pupildetect(img)
        if framecount > frameav and fcrds[0] != 0 and fcrds[1] != 0 and fcrds[2] != 0:
            ax = numpy.uint16(numpy.around(numpy.average(fcrds[0])))
            ay = numpy.uint16(numpy.around(numpy.average(fcrds[1])))
            ar = numpy.uint16(numpy.around(numpy.average(fcrds[2])))
            print(str(ax) + " " + str(ay))
            framecount = 0
        elif fcrds[0] != 0 and fcrds[1] != 0 and fcrds[2] != 0:
            framecount += 1
        # quit the webcam at esc
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    # close the window
    cv2.destroyAllWindows()

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
                                   param1=10, param2=30, minRadius=60, maxRadius=75)
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




if __name__ == '__main__':
    main()