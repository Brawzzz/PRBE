import cv2 as cv
import numpy as np
import glob
import setup as stp  
import setup_camera as stp_cam
from mser import detect_mser 


CAM = stp_cam.B2
SEQUENCE = stp.Sequence.NOISE
#----------------------------------------------------------------------------------------#
#---------------------------------------- IMAGES ----------------------------------------#
#----------------------------------------------------------------------------------------#
SEQUENCE_PATH = stp.switch_sequence_path(CAM, SEQUENCE.value) 
image_names = sorted(glob.glob(stp.NOISE_PATH + "*.bmp"))
if len(image_names) < 2:
    print("#======================================================================#")
    raise ValueError("MINIMUM TWO IMAGES ARE NEEDED")
    print("#======================================================================#")

img = cv.imread(image_names[0])
mask = np.zeros_like(img)

if img is None:
    print("#======================================================================#")
    raise IOError(f"ERROR READING FIRST IMAGES : {image_names[0]}")
    print("#======================================================================#")   

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_gray_prev = img_gray.copy()

roi_rect = [CAM.x0, CAM.y0, stp.WINDOW_WIDTH, stp.WINDOW_HEIGHT] 
roi_img = img_gray[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

#----------------------------------------------------------------------------------------#
#----------------------------------------- MSER -----------------------------------------#
#----------------------------------------------------------------------------------------#
(mser_regions, mser_contours, mser_centers) = detect_mser(img_gray, roi_img, CAM)

#----------------------------------------------------------------------------------------#
#-------------------------------------- OPTIC FLOW --------------------------------------#
#----------------------------------------------------------------------------------------#
lk_params = dict(winSize=(5, 5), maxLevel=1, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.02))

mser_centers_prev = np.array(mser_centers, dtype=np.float32).reshape(-1, 1, 2)

vect = []
magnitude = []
for path in image_names[1:]:

    frame = cv.imread(path, cv.IMREAD_COLOR)
    if frame is None:
        print("#======================================================================#")
        print(f"ERROR READING : {path} SKIP")
        print("#======================================================================#")
        continue
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    (mser_centers_next, status, err) = cv.calcOpticalFlowPyrLK(img_gray_prev, frame_gray, mser_centers_prev, None, **lk_params)

    new_valid_point = mser_centers_next[status == 1]
    old_valid_point = mser_centers_prev[status == 1]

    if len(new_valid_point) == 0:
        print("#======================================================================#")
        print("\t\tNO VALID POINTS DETECTED")
        print("#======================================================================#")
        break
    
    #------------------------------------------------------------------------------------#
    #----------------------------------- TRAJ DRAWING -----------------------------------#
    #------------------------------------------------------------------------------------#

    for new_points, old_points in zip(new_valid_point, old_valid_point):

        (a, b) = new_points.ravel()
        (c, d) = old_points.ravel()

        cv.line(mask, (int(a),int(b)), (int(c), int(d)), (0, 255, 0), 1)
        cv.circle(frame, (int(a), int(b)), 6, (0, 0, 255), -1)

        vect.append([a-c, b-d])

    print(vect, len(vect))

    vect = []
    output = cv.add(frame, mask)
    cv.imshow('MSER Tracking + Lucas-Kanade', output)

    key = cv.waitKey(100)
    if key == 27:
        break

    img_gray_prev = frame_gray.copy()
    mser_centers_prev = new_valid_point.reshape(-1, 1, 2)

cv.destroyAllWindows()