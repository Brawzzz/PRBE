import cv2 as cv
import numpy as np


def intensity_check(img, regions, hulls):
    
    Regions = []
    Contours = []
    Centers = []

    intensity_threshold = 2 

    for index, (region, cnt) in enumerate(zip(regions, hulls)):

        M = cv.moments(cnt)

        if M["m00"] == 0:
            continue

        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 

        if(0 <= center[0] < img.shape[1]) and (0 <= center[1] < img.shape[0]) :

            bright = img[center[1], center[0]] 
            bright_mean = np.mean([img[p[1], p[0]] for p in region])

            if(bright < bright_mean - intensity_threshold) :
                Regions.append(region)
                Contours.append(cnt)
                Centers.append(center)

    clone = img.copy()
    clone = cv.cvtColor(clone, cv.COLOR_GRAY2RGB)

    cv.polylines(clone, Contours, isClosed=True, color=(0, 255, 0))

    cv.namedWindow('selected MSER from intensity', cv.WINDOW_AUTOSIZE)
    cv.imshow('selected MSER from intensity', clone)
    cv.imwrite('./OUTPUT/selected_MSER_intensity.jpg', clone)

    cv.waitKey()
    cv.destroyAllWindows()

    return Regions, Contours, Centers, clone