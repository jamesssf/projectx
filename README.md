# projectx
Ereader glasses

/////simplecam.py/////
A simple pupil tracking algorithm using cv2's HoughCircles and threshold.
This module is a test module, however many of the functions in the module are sure to end 
up in a future final version

def showcam() - Print the camera, and launch the pupildetect function.
return null

def pupildetect(img, maxInt) - find the pupil with CHT
img - the captured image from the camera
maxInt - the maximum intensity of a pixel to be detected by
the cht algorithm.  Currently this can be raised or lowerd with
the plus or minus key and starts at the highest intensity, eg there
is no bias

This program is currently not working, it detects the eye probably 1/100~1000 times
