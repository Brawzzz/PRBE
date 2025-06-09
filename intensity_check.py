import cv2 as cv
import numpy as np
import setup as stp

def intensity_check(img, regions, hulls, intensity_th = 5):
    
    new_regions = []
    new_contours = []
    new_centers = []

    for index, (region, cnt) in enumerate(zip(regions, hulls)):

        M = cv.moments(cnt)

        if M["m00"] == 0:
            continue

        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 

        if(0 <= center[0] < img.shape[1]) and (0 <= center[1] < img.shape[0]) :

            bright = img[center[1], center[0]] 
            bright_mean = np.mean([img[p[1], p[0]] for p in region])

            if(bright <= bright_mean - intensity_th) :
                new_regions.append(region)
                new_contours.append(cnt)
                new_centers.append(center)

    #------------------- DISPLAY -------------------#
    img_clone = img.copy()
    img_clone = cv.cvtColor(img_clone, cv.COLOR_GRAY2RGB)

    cv.polylines(img_clone, new_contours, isClosed=True, color=(0, 255, 0))

    if(stp.SHOW_IMAGE):
        cv.namedWindow('selected MSER from intensity', cv.WINDOW_AUTOSIZE)
        cv.imshow('selected MSER from intensity', img_clone)
        cv.waitKey()
        cv.destroyAllWindows()
    
    cv.imwrite(stp.IMG_MSER_SELECTED_INTENSITY, img_clone)

    return(new_regions, new_contours, new_centers, img_clone)