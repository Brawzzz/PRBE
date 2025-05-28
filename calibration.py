import numpy as np
import cv2 as cv
import glob
import setup as stp


SETUP = stp.setup_files(stp.CAM_PATH)

if(SETUP == True):

    #------------- IMAGES -------------#
    image_names = glob.glob(stp.INTRINSIC_PATH + '*.bmp')

    #--------------- INIT -------------#
    grid = np.zeros((stp.COL * stp.ROW, 3), np.float32)
    grid[:, :2] = np.mgrid[0:stp.COL, 0:stp.ROW].T.reshape(-1, 2) * stp.D 

    points_3d_world = []  
    points_2d_image = []  

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #----------------------------------------------------------------------------#
    #-------------------------- INTRINSIC CALIBRATION ---------------------------#
    #----------------------------------------------------------------------------#
    conut_img = 0
    for img_i in image_names:
        
        img_gray = cv.imread(img_i, cv.IMREAD_GRAYSCALE)
        
        (ret, corners) = cv.findChessboardCorners(img_gray, (stp.COL, stp.ROW), None)

        if ret == True:
        
            points_3d_world.append(grid)

            corners_refine = cv.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
            points_2d_image.append(corners_refine)

            img_color = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
            img_color = cv.drawChessboardCorners(img_color, (stp.COL, stp.ROW), corners_refine, ret)
            cv.imwrite(stp.CALIBRATION_OUTPUT_PATH + stp.CAM_PATH + stp.CORNERS + stp.CHECKBOARD_FILE + "_" + str(conut_img) + stp.IMG_EXTENSION, img_color)

        conut_img += 1

    (h, w) = img_color.shape[:2]
    (ret, mtx, dist_coeff, r_vector, t_vector) = cv.calibrateCamera(points_3d_world, points_2d_image, (w, h), None, None)

    print("Error calibrateCamera : \n", ret)

    print("#---------- Camera matrix ----------#\n")
    print(mtx)

    print("\n#----------Distortion coefficient ----------#\n")
    print(dist_coeff)

    print("\n#----------Rotation Vectors ----------#\n")
    print(r_vector)

    print("\n#----------Translation Vectors ----------#\n")
    print(t_vector)

    np.savez(stp.CALIBRATION_OUTPUT_PATH + stp.CAM_PATH + stp.CAM_DATA_FILE + "_" + stp.CAM, mtx=mtx, dist_coeff=dist_coeff, r_vector=r_vector, t_vector=t_vector)

    #------------- COMPUTE FOCAL --------------#
    fx = mtx[0, 0] * stp.SENSOR_X 
    fy = mtx[1, 1] * stp.SENSOR_Y

    print("Focal length:")
    print("fx = ", fx, "mm")
    print("fy = ", fy, "mm")
    print("\n")

    #-----------------------------------------------------------------------------------#
    #----------------------------- EXTRINSIC CALIBRATION -------------------------------#
    #-----------------------------------------------------------------------------------#
    image_names = glob.glob(stp.EXTRINSIC_PATH + '*.bmp')

    with np.load(stp.CALIBRATION_OUTPUT_PATH + stp.CAM_PATH + stp.CAM_DATA_FILE + "_" + stp.CAM + stp.NPZ_EXTENSION) as X:
        (mtx, dist_coeff, r_vector, t_vector) = [X[i] for i in ('mtx', 'dist_coeff', 'r_vector', 't_vector')]

    img_gray = cv.imread(image_names[0], cv.IMREAD_GRAYSCALE)

    (h, w) = img_gray.shape[:2]

    (new_camera_mtx, roi) = cv.getOptimalNewCameraMatrix(mtx, dist_coeff, (w, h), 1, (w, h))
    undistorted_img = cv.undistort(img_gray, mtx, dist_coeff, None, new_camera_mtx)

    (ret, corners) = cv.findChessboardCorners(undistorted_img, (stp.COL, stp.ROW), None)

    if not ret:
        print("#========== CHECKBOARD NOT DETECTED ==========#")
    else :
        points_2d_image = cv.cornerSubPix(undistorted_img, corners, (11, 11), (-1, -1), criteria)

        points_3d_world = np.zeros((stp.COL * stp.ROW, 3), np.float32)
        points_3d_world[:, :2] = np.mgrid[0:stp.COL, 0:stp.ROW].T.reshape(-1, 2) * stp.D

        #---------- TRANSLATION & ROTATION ----------#
        (ret, r_vector, t_vector) = cv.solvePnP(points_3d_world, points_2d_image, mtx, dist_coeff)

        #---------- ROTATION MATRIX ----------#
        R = cv.Rodrigues(r_vector)[0]

        #---------- CAMERA PROJECTION MATRIX ----------#
        Rt = np.hstack((R, t_vector))
        P = np.dot(mtx, Rt)

        print("\n#---------- Camera projection matrix ----------#")
        print(P)

        print("\n#---------- Rotation matrix ----------#")
        print(R)

        print("\n#---------- Translation vector ----------#")
        print(t_vector)
        print("\n")

        np.savez(stp.CALIBRATION_OUTPUT_PATH + stp.CAM_PATH + stp.CAM_PROJECTION_FILE + "_" + stp.CAM, P)