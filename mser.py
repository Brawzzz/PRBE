import cv2 as cv
import numpy as np
import glob
from circularity_check import circularity_check
from intensity_check import intensity_check
from duplicated_check import duplicated_check
from interactive_binarization import interactive_binarization

#---------- PATH ----------#
CAM = 'B2'

EXTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Intrinsic/"

GROUND_MOTION_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Ground motion/"

image_names = glob.glob(GROUND_MOTION_PATH + '*.bmp')
img = cv.imread(image_names[5], cv.IMREAD_GRAYSCALE)

#------------- ROI IMAGE -------------#
x0 = 150
y0 = 225

window_width = 1280
window_height = 650

roi_rect = [x0, y0, window_width, window_height] 
roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

cv.imshow('roi_img', roi_img)
cv.waitKey(0)
cv.destroyAllWindows()

#------------- IMAGE PROCESSING -------------#
sobel_x = np.array([[ 1,  0,  -1], [ 1,  0,  -1], [1, 0, -1]])
sobel_y = np.array([[ 1,  1,  1], [ 0,  0,  0], [-1, -1, -1]])

img_sobel_x = cv.filter2D(roi_img, -1, kernel=sobel_x)
img_sobel_y = cv.filter2D(roi_img, -1, kernel=sobel_y)

img_sobel = cv.addWeighted(img_sobel_x, 0.5, img_sobel_y, 0.5, 0)
img_blur = cv.GaussianBlur(roi_img, (3,3), 0)

cv.imshow('img_blur', img_sobel)
cv.waitKey(0)
cv.destroyAllWindows()

# # th_min = 50
# # th_max = 255

# (th_min, th_max) = interactive_binarization(img_blur)
# (ret, img_bw) = cv.threshold(img_blur, th_min, th_max, cv.THRESH_BINARY)

#---------------- MSER DETECTION ----------------#
mser = cv.MSER_create(delta=2, min_area=2, max_area=500, max_variation=0.5)
(regions, a_1) = mser.detectRegions(img_blur)

hulls = [cv.convexHull(p) for p in regions]

img_clone = roi_img.copy()
img_clone = cv.cvtColor(roi_img, cv.COLOR_GRAY2RGB) 

cv.polylines(img_clone, hulls, 1, (0, 255, 0))

cv.namedWindow('all MSER', cv.WINDOW_AUTOSIZE) 
cv.imshow('all MSER', img_clone) 
cv.imwrite('./OUTPUT/all_MSER.jpg', img_clone)

cv.waitKey()
cv.destroyAllWindows()

#----------------- MSER SELECTION ---------------#
(Regions_circ, Contours_circ, img_clone_circ) = circularity_check(roi_img, regions, hulls)
(Regions_int, Contours_int, Centers_int, img_clone_int) = intensity_check(roi_img, Regions_circ, Contours_circ)
(Regions, Contours, Centers, Bbox, img_clone_selection) = duplicated_check(roi_img, Regions_int, Contours_int, Centers_int)

# 3.4 Evaluate mean centroid
result_centroid = []
for ind in Bbox:

    temp = []
    corner_min = np.array((ind[0], ind[1]))
    corner_max = np.array((ind[0] + ind[2], ind[1] + ind[3]))

    for centroid in Centers:
        if ((np.array(centroid) < corner_max).all() and (np.array(centroid) > corner_min).all()):
            temp.append(centroid)

    if temp:
        result_centroid.append(tuple(np.mean(temp, axis=0, dtype=int)))
        
result_centroid = list(set(result_centroid))

print(len(result_centroid))

#------------------- VISUALIZATION -------------------#
img_clone_selection_col = img_clone_selection.copy()
img_clone_selection_col = cv.cvtColor(img_clone_selection, cv.COLOR_BGR2RGB)

font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 0, 255)
thickness = 1

for i, c in enumerate(result_centroid):
    number = str(i + 1)
    cv.putText(img_clone_selection_col, number, (c[0] + 10, c[1] - 10), font, font_scale, color, thickness)

cv.polylines(img_clone_selection_col, Contours, isClosed=True, color=(0, 255, 0), thickness=2)

cv.namedWindow('selected MSER', cv.WINDOW_AUTOSIZE)
cv.imshow('selected MSER', img_clone_selection_col)  # afficher l'image avec les labels et contours
cv.imwrite('./OUTPUT/selected_MSER.jpg', img_clone_selection_col)  # sauver l'image

cv.waitKey()
cv.destroyAllWindows()



















