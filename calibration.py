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
        
        img_i_gray = cv.imread(img_i, cv.IMREAD_GRAYSCALE)
        
        (ret, corners) = cv.findChessboardCorners(img_i_gray, (stp.COL, stp.ROW), None)

        if ret == True:
        
            points_3d_world.append(grid)

            corners_refine = cv.cornerSubPix(img_i_gray, corners, (11, 11), (-1, -1), criteria)
            points_2d_image.append(corners_refine)

            img_color = cv.cvtColor(img_i_gray, cv.COLOR_GRAY2BGR)
            img_color = cv.drawChessboardCorners(img_color, (stp.COL, stp.ROW), corners_refine, ret)
            cv.imwrite(stp.IMG_INTRINSIC_CALIB + str(conut_img) + stp.IMG_EXTENSION, img_color)

        conut_img += 1

    (h, w) = img_color.shape[:2]
    (ret, camera_mtx, dist_coeff, r_vector, t_vector) = cv.calibrateCamera(points_3d_world, points_2d_image, (w, h), None, None)

    print("\nError calibrateCamera : \n", ret)

    print("\n#---------- Camera matrix ----------#\n")
    print(camera_mtx)

    print("\n#----------Distortion coefficient ----------#\n")
    print(dist_coeff)

    print("\n#----------Rotation Vectors ----------#\n")
    print(r_vector)

    print("\n#----------Translation Vectors ----------#\n")
    print(t_vector)

    np.savez(stp.INTRINSIC_CALIB_DATA, mtx=camera_mtx, dist_coeff=dist_coeff, r_vector=r_vector, t_vector=t_vector)

    #------------- COMPUTE FOCAL --------------#
    fx = camera_mtx[0, 0] * stp.SENSOR_X 
    fy = camera_mtx[1, 1] * stp.SENSOR_Y

    print("\n#--------- Focal length ---------#")
    print("fx = ", fx, "mm")
    print("fy = ", fy, "mm")
    print("\n")

    #-----------------------------------------------------------------------------------#
    #----------------------------- EXTRINSIC CALIBRATION -------------------------------#
    #-----------------------------------------------------------------------------------#
    image_names = glob.glob(stp.EXTRINSIC_PATH + '*.bmp')

    with np.load(stp.INTRINSIC_CALIB_DATA + stp.NPZ_EXTENSION) as X:
        (camera_mtx, dist_coeff, r_vector, t_vector) = [X[i] for i in ('mtx', 'dist_coeff', 'r_vector', 't_vector')]

    img_color = cv.imread(image_names[0], cv.IMREAD_COLOR_BGR)
    img_gray = cv.imread(image_names[0], cv.IMREAD_GRAYSCALE)
    
    (h, w) = img_gray.shape[:2]

    if(stp.CAM == "B1"):

        structure_points_3d = np.array([
            [-10.75, -21.0, 197],
            [-10.75, -21.0, 401],
            [-10.75, -21.0, 605],
            [-10.75, -21.0, 809],
            [288, 278, 197],
            [288, 278, 401],
            [288, 278, 605],
            [288, 278, 809]
        ], dtype=np.float32)

        structure_points_2d = np.array([
            [331, 155],
            [600, 155],
            [869, 158],
            [1138, 161],
            [293, 701],
            [581, 709],
            [872, 709],
            [1165, 712]
        ], dtype=np.float32)

    elif(stp.CAM == "B2"):
        
        structure_points_3d = np.array([
            [-10.75, -21.0, 197],
            [-10.75, -21.0, 401],
            [-10.75, -21.0, 605],
            [-10.75, -21.0, 809],
            [288, 278, 197],
            [288, 278, 401],
            [288, 278, 605],
            [288, 278, 809]
        ], dtype=np.float32)

        structure_points_2d = np.array([
            [279.183584, 263.493661],
            [566.611565, 256.617393],
            [854.039545, 255.242140],
            [1131.840751, 255.242140],
            [273.682570, 858.978424],
            [574.863086, 857.603171],
            [870.542587, 845.225889],
            [1156.595314, 838.349622]
        ], dtype=np.float32)

    (success, r_vector, t_vector) = cv.solvePnP(structure_points_3d, structure_points_2d, camera_mtx, dist_coeff)

    (projected_points, _) = cv.projectPoints(structure_points_3d, r_vector, t_vector, camera_mtx, dist_coeff)
    for p in projected_points:
        cv.circle(img_color, tuple(p[0].astype(int)), 5, (0, 0, 255), -1)

    cv.imwrite(stp.IMG_EXTRINSIC_CALIB, img_color)
    cv.imshow("Projection", img_color)
    cv.waitKey(0)
    cv.destroyAllWindows()

    #---------- ROTATION MATRIX ----------#
    R = cv.Rodrigues(r_vector)[0]

    #---------- CAMERA PROJECTION MATRIX ----------#
    Rt = np.hstack((R, t_vector))
    P = np.dot(camera_mtx, Rt)

    print("\n#---------- Camera projection matrix ----------#")
    print(P)

    print("\n#---------- Rotation matrix ----------#")
    print(R)

    print("\n#---------- Translation vector ----------#")
    print(t_vector)
    print("\n")

    np.savez(stp.EXTRINSIC_CALIB_DATA, P=P, R=R, r_vector=r_vector, t_vector=t_vector)