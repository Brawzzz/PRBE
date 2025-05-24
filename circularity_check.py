import cv2 as cv
import numpy as np


CIRCULARITY_THRESHOLD = 0.80

#----------------------------------------------------#
def circularity_check(img, regions, hulls):

    Regions = []
    Contours = []

    for index, (region, cnt) in enumerate(zip(regions, hulls)):
        area = cv.contourArea(cnt) 
        perimeter = cv.arcLength(cnt, True)

        if(perimeter == 0) : 
            continue

        circularity = 4 * np.pi * area / (perimeter ** 2) 

        if(circularity > CIRCULARITY_THRESHOLD) :
            Regions.append(region) 
            Contours.append(cnt)

    clone = img.copy()
    clone = cv.cvtColor(img, cv.COLOR_GRAY2RGB) 

    cv.polylines(clone, Contours, isClosed=True, color=(0, 255, 0))

    cv.namedWindow('circular MSER', cv.WINDOW_AUTOSIZE) 
    cv.imshow('circular_MSER', clone)
    cv.imwrite('./OUTPUT/circular_MSER.jpg', clone)

    cv.waitKey()
    cv.destroyAllWindows()

    return Regions, Contours, clone
