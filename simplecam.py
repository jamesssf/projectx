
import cv2
import numpy

def showcam():
    cam = cv2.VideoCapture(0)
    #Initially let all intensities through the filter
    maxInt = 255
    while True:
        if cv2.waitKey(1) == 43:
            print("UP")
            maxInt += 10
        if cv2.waitKey(1) == 45:
            maxInt -= 10
            print("DOWN")
        ret_val, img, = cam.read()
        thresh1 = pupildetect(img, maxInt)
        cv2.imshow('my webcam', thresh1)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()

def pupildetect(img, maxInt):
    #Blurs the image to make it easier to detect
    bimg = cv2.medianBlur(img, 5)
    #Turn the image greyscale
    gimg = cv2.cvtColor(bimg, cv2.COLOR_BGR2GRAY)
    #Turn every pixel above maxInt white
    ret, cimg = cv2.threshold(gimg, maxInt, 0, cv2.THRESH_TOZERO_INV)
    ##thresh1 = cv2.adaptiveThreshold(thresh2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,.5)
    try:
        circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=10, param2=30, minRadius=0, maxRadius=30)
        circles = numpy.uint16(numpy.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        print("circle drawing failed")
    return cimg



def main():
    showcam()


if __name__ == '__main__':
    main()
