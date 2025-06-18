import cv2 as cv
import numpy as np
import glob
import setup as stp
import matplotlib.pyplot as plt 
import calibration


stp.B1.set_roi(x0=120, y0=565)
stp.B2.set_roi(x0=0, y0=400)

stp.B1.set_intensity_th(intensity_th=10)
stp.B2.set_intensity_th(intensity_th=8)

(camera_mtx, dist_coef) = calibration.calib_int(stp.B1)
(proj_mtx, rotation_mtx) = calibration.calib_ext(stp.B1)
stp.B1.set_calib(camera_mtx, dist_coef, proj_mtx, rotation_mtx)

(camera_mtx, dist_coef) = calibration.calib_int(stp.B2)
(proj_mtx, rotation_mtx) = calibration.calib_ext(stp.B2)
stp.B2.set_calib(camera_mtx, dist_coef, proj_mtx, rotation_mtx)

cam = stp.B1

#--------------------------------------------------------------------------------------------------#
#----------------------------------------------- FUNCTION -----------------------------------------#
#--------------------------------------------------------------------------------------------------#
def distance(p1, p2):
    return np.linalg.norm(np.array(p2) - np.array(p1))

def points_filter(points, d_min):
    filtered_points = []
    for pt in points:
        if all(distance(pt, other) > d_min for other in filtered_points):
            filtered_points.append(pt)
    return filtered_points

#--------------------------------------------------------------------------------------------------#
#---------------------------------------------- LOCAL MAIN ----------------------------------------#
#--------------------------------------------------------------------------------------------------#
ROI = False
SETUP = stp.setup_files(cam)

print("#======================================================================#")


if(SETUP):

    stp.EXTRINSIC_PATH = stp.switch_calib_path(cam, type="ext")
    image_names = glob.glob(stp.EXTRINSIC_PATH + '*.bmp')

    img = cv.imread(image_names[0], cv.IMREAD_GRAYSCALE)
    img_col = cv.imread(image_names[0], cv.IMREAD_COLOR)

    # roi_rect = [cam.x0, cam.y0, stp.WINDOW_WIDTH, stp.WINDOW_HEIGHT] 

    # img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]
    # img_col = img_col[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]


    if(ROI):
        (x, y, w, h) = cv.selectROI("select ROI", img)
        img_myre = img[y:y+h, x:x+w]
        cv.imwrite(stp.TEMPLATE_PATH, img_myre)

    else:

        template = cv.imread(stp.TEMPLATE_PATH, cv.IMREAD_GRAYSCALE)
        (w, h) = (template.shape[1], template.shape[0])

        methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR, cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]

        min_val = 100000
        min_loc = []

        result = cv.matchTemplate(img, template, cv.TM_SQDIFF)
        # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        for i in range(0, result.shape[0]):
            for j in range(0, result.shape[1]):

                val = result[i][j]
                if(val < min_val):
                    loc = (j, i)
                    min_loc.append(loc)

        min_loc = points_filter(min_loc, d_min=10)
        
        for i in range(0, len(min_loc)) :

            top_left = min_loc[i]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_col, top_left, bottom_right, (0, 255, 0), 2)

        cv.imshow('Matching Result', img_col)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite(stp.TEMPLATE_MATCHING_OUTPUT, img_col)

        plt.figure(figsize=(10, 6))
        plt.imshow(result, cmap='inferno', interpolation='lanczos')
        plt.colorbar(label='Score de correspondance')
        plt.title("Heatmap - Résultat de matchTemplate")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
