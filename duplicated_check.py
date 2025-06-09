import cv2 as cv
import numpy as np
import setup as stp

def duplicated_check(img, regions, cnt, centers):

    n_atol = 10 

    box = [cv.boundingRect(i) for i in cnt]
    B = np.array(box)
    remove_boxes = np.zeros(B.shape[0], dtype=bool)

    for i in range(B.shape[0]):
        similar = np.isclose(B[i, :], B[(i + 1):, :], atol=n_atol)
        equals = np.all(similar, axis=1)
        remove_boxes[(i + 1):] = np.logical_or(remove_boxes[(i + 1):], equals)

    index = np.where(np.logical_not(remove_boxes))[0]
    b_box = B[index]

    new_regions = [regions[p] for p in index]
    new_contours = [cnt[p] for p in index]
    new_centers = [centers[p] for p in index]

    #------------------- DISPLAY -------------------#
    clone = img.copy()
    clone = cv.cvtColor(clone, cv.COLOR_GRAY2RGB)
    cv.polylines(clone, new_contours, isClosed=True, color=(0, 255, 0))

    if(stp.SHOW_IMAGE):
        cv.namedWindow('duplicated MSER suppression', cv.WINDOW_AUTOSIZE)
        cv.imshow('duplicated MSER suppression', clone)
        cv.waitKey()
        cv.destroyAllWindows()
        
    cv.imwrite(stp.IMG_MSER_DUPLICATED_SUPRESSION, clone)

    return(new_regions, new_contours, new_centers, b_box, clone)

