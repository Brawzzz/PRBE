import cv2 as cv
import glob
import random
from mser import detect_mser


#---------- PATH ----------#
CAM = 'B1'

NMB_IMG = 101
IMG_INDEX = random.randint(0, NMB_IMG)

EXTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Intrinsic/"

GROUND_MOTION_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Ground_Motion/"
NOISE_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Noise/"
SHOCK_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Shock/"

#------------- IMAGE SELECTION -------------#
image_names = glob.glob(GROUND_MOTION_PATH + '*.bmp')
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

#------------- IMAGE ROI -------------#
if CAM == 'B1':

    x0 = 150
    y0 = 250

    window_width = 1280
    window_height = 500
    
    th_min = 65
    th_max = 255

elif CAM == 'B2':

    x0 = 150
    y0 = 265

    window_width = 1280
    window_height = 600

    th_min = 45
    th_max = 255

roi_rect = [x0, y0, window_width, window_height] 
roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

cv.imshow('roi_img', roi_img)
cv.waitKey(0)
cv.destroyAllWindows()

(mser_regions, mser_contours, mser_centers) = detect_mser(roi_img, th_min, th_max)