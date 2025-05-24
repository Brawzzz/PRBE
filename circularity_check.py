import cv2 as cv
import numpy as np


CIRCULARITY_THRESHOLD = 0.85

#----------------------------------------------------#
def circularity_check(img, regions, hulls):

    new_regions = []
    new_contours = []

    for index, (region, cnt) in enumerate(zip(regions, hulls)):
        area = cv.contourArea(cnt) 
        perimeter = cv.arcLength(cnt, True)

        if(perimeter == 0) : 
            continue

        circularity = 4 * np.pi * area / (perimeter ** 2) 

        if(circularity > CIRCULARITY_THRESHOLD) :
            new_regions.append(region) 
            new_contours.append(cnt)

    #------------------- DISPLAY -------------------#
    img_clone = img.copy()
    img_clone = cv.cvtColor(img, cv.COLOR_GRAY2RGB) 

    cv.polylines(img_clone, new_contours, isClosed=True, color=(0, 255, 0))

    cv.namedWindow('circular MSER', cv.WINDOW_AUTOSIZE) 
    cv.imshow('circular_MSER', img_clone)
    cv.imwrite('./OUTPUT/circular_MSER.jpg', img_clone)

    cv.waitKey()
    cv.destroyAllWindows()

    return (new_regions, new_contours, img_clone)
