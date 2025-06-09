import cv2 as cv
import numpy as np
import glob
import sys
import setup as stp
from intensity_check import intensity_check
from duplicated_check import duplicated_check

#--------------------------------------------------------------------------------------------------#
#----------------------------------------------- MSER ---------------------------------------------#
#--------------------------------------------------------------------------------------------------#
def detect_mser(img, intensity_th):

    #---------------- MSER DETECTION ----------------#
    mser = cv.MSER_create(delta=2, min_area=9, max_area=20, max_variation=2)
    (regions, b_box) = mser.detectRegions(img)

    hulls = [cv.convexHull(p) for p in regions]

    img_clone = img.copy()
    img_clone = cv.cvtColor(img, cv.COLOR_GRAY2RGB) 

    cv.polylines(img_clone, hulls, 1, (0, 255, 0))

    if(stp.SHOW_IMAGE):
        cv.namedWindow('all MSER', cv.WINDOW_AUTOSIZE) 
        cv.imshow('all MSER', img_clone) 
        cv.waitKey()
        cv.destroyAllWindows()
        
    cv.imwrite(stp.IMG_MSER_ALL, img_clone)

    #----------------- MSER SELECTION ---------------#
    (regions_int, contours_int, Centers_int, img_clone_int) = intensity_check(img, regions, hulls, intensity_th)
    (regions, contours, centers, b_box, img_clone_selection) = duplicated_check(img, regions_int, contours_int, Centers_int)

    centers.sort(key=lambda x : x[1], reverse=False)

    result_centroid = []
    for ind in b_box:

        temp = []
        corner_min = np.array((ind[0], ind[1]))
        corner_max = np.array((ind[0] + ind[2], ind[1] + ind[3]))

        for centroid in centers:
            if ((np.array(centroid) < corner_max).all() and (np.array(centroid) > corner_min).all()):
                temp.append(centroid)

        if temp:
            result_centroid.append(tuple(np.mean(temp, axis=0, dtype=int)))
    
    result_centroid = list(set(result_centroid))
    result_centroid.sort(key=lambda x : x[1], reverse=False)

    print(f"Number of myre detected : {len(result_centroid)} \n")

    #------------------- VISUALIZATION -------------------#
    img_clone_selection_col = img_clone_selection.copy()
    img_clone_selection_col = cv.cvtColor(img_clone_selection, cv.COLOR_BGR2RGB)

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)
    thickness = 1

    for i, c in enumerate(result_centroid):
        number = str(i)
        cv.putText(img_clone_selection_col, number, (c[0] + 10, c[1] - 10), font, font_scale, color, thickness)

    cv.polylines(img_clone_selection_col, contours, isClosed=True, color=(0, 255, 0), thickness=2)

    cv.namedWindow('selected MSER', cv.WINDOW_AUTOSIZE)
    cv.imshow('selected MSER', img_clone_selection_col) 
    cv.waitKey()
    cv.destroyAllWindows()

    cv.imwrite(stp.IMG_MSER_SELECTED, img_clone_selection_col)

    return(regions, contours, result_centroid)

#--------------------------------------------------------------------------------------------------#
#-------------------------------------------- MATCHING --------------------------------------------#
#--------------------------------------------------------------------------------------------------#
def find_matching_centers(mser_centers):

    centers_b1 = mser_centers[0]
    centers_b2 = mser_centers[1]

    matching_centers = []

    for c1_i in centers_b1 :

        d_min = sys.float_info.max

        for c2_i in centers_b2 :

            x0 = c1_i[0]
            y0 = c1_i[1]
            x1 = c2_i[0]
            y1 = c2_i[1]

            d = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)

            if(d < d_min):
                d_min = d
                c2_i_min = c2_i

        matching_centers.append((c1_i, c2_i_min))
    
    return matching_centers

#--------------------------------------------------------------------------------------------------#
#---------------------------------------------- LOCAL MAIN ----------------------------------------#
#--------------------------------------------------------------------------------------------------#
if __name__ == "__main__":

    image_names = glob.glob(stp.GROUND_MOTION_PATH + '*.bmp')
    img = cv.imread(image_names[0], cv.IMREAD_GRAYSCALE)

    #------------- ROI IMAGE -------------#
    x0 = 150
    y0 = 265

    window_width = 1280
    window_height = 650

    roi_rect = [x0, y0, window_width, window_height] 
    roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

    cv.imshow('roi_img', roi_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    (regions, contours, centers) = detect_mser(roi_img)

    

















