import cv2
import numpy

def showcam():
    # Capture the camera feed
    cam = cv2.VideoCapture(0)
    # Loop pupil detection and print webcam
    while True:
        # Take each image from the webcam
        ret_val, img, = cam.read()
        # run pupil detection algorithm
        hough_img = pupildetect(img)
        # print the webcam
        cv2.imshow('my webcam', hough_img)
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
    ret, thresh_img = cv2.threshold(grey_img, 75, 255, cv2.THRESH_TRUNC)
    try:
        # Create hough cricles
        circles = cv2.HoughCircles(thresh_img, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=10, param2=30, minRadius=0, maxRadius=30)
        circles = numpy.uint16(numpy.around(circles))
        # Draw circles
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    # sometimes there are no circles detected and the program poops
    # out not quite sure how to stop it, there's got to be a way to
    # skip something if no circles are detected, fix later
    except:
        print("circle drawing failed")
    return img

def main():
    showcam()


if __name__ == '__main__':
    main()
