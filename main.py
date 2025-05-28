import cv2 as cv
import glob
import random
import setup as stp
from mser import detect_mser


#-------------------------- IMAGE SELECTION --------------------------#
IMG_INDEX = 0

image_names = glob.glob(stp.NOISE_PATH + '*.bmp')
img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_GRAYSCALE)

cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()

print("\n#============================#")
index = image_names[IMG_INDEX].find('\\')
if index != -1:
    print(f"Selected image : {image_names[IMG_INDEX][(index+1):]}")
    print(f"Image index : {IMG_INDEX}")
else:
    tronquee = image_names[IMG_INDEX]
print("#============================#\n")

#------------------------- PARAMS -------------------------#
if stp.CAM == 'B1':

    x0 = 150
    y0 = 250   

    window_width = 1280
    window_height = 500

elif stp.CAM == 'B2':

    x0 = 150
    y0 = 265

    window_width = 1280
    window_height = 600

#-------------------------- IMAGE ROI --------------------------#
roi_rect = [x0, y0, window_width, window_height] 
roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

cv.imshow('roi_img', roi_img)
cv.waitKey(0)
cv.destroyAllWindows()

(mser_regions, mser_contours, mser_centers) = detect_mser(roi_img)