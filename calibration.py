import numpy as np
import cv2 as cv
import glob


#---------- CAMERA : Basler_acA1300-200um ----------#
sensor_x = 0.0048 
sensor_y = 0.0048 

#---------- FILE PATH ----------#
CAM = 'B2'

EXTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Calibration/Intrinsic/"

CALIBRATION_OUTPUT_PATH = "./OUTPUT/calibration/"

CHECKBOARD_FILE = 'checkerboard_calibration.png'
CAM_DATA_FILE = 'calibration_data_cam_basler_acA1300.npz'
CAM_PROJECTION_FILE = 'camera_projection_matrix.npy'

#---------- CHECKBOARD PARAMETERS ----------#
nb_c = 8
nb_r = 6
d = 15 

#------------- IMAGES -------------#
image_names = glob.glob(INTRINSIC_PATH + '*.bmp')

#--------------- INIT -------------#
grid = np.zeros((nb_c * nb_r, 3), np.float32)
grid[:, :2] = np.mgrid[0:nb_c, 0:nb_r].T.reshape(-1, 2) * d 

points_3d_world = []  
points_2d_image = []  

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#--------------------------------------------------#
#------------- INTRINSIC CALIBRATION --------------#
#--------------------------------------------------#

for img_i in image_names:
    
    img_gray = cv.imread(img_i, cv.IMREAD_GRAYSCALE)

    (ret, corners) = cv.findChessboardCorners(img_gray, (nb_c, nb_r), None)

    if ret == True:
    
        points_3d_world.append(grid)

        corners2 = cv.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
        points_2d_image.append(corners2)

        img_color = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
        img = cv.drawChessboardCorners(img_color, (nb_c, nb_r), corners2, ret)
        cv.imwrite(CALIBRATION_OUTPUT_PATH + CHECKBOARD_FILE, img_color)

(h, w) = img.shape[:2]

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

np.savez(CALIBRATION_OUTPUT_PATH + CAM_DATA_FILE, mtx=mtx, dist_coeff=dist_coeff, r_vector=r_vector, t_vector=t_vector)

#------------- COMPUTE FOCAL --------------#
fx = mtx[0, 0] * sensor_x 
fy = mtx[1, 1] * sensor_y 

print("Focal length:")
print("fx = ", fx, "mm")
print("fy = ", fy, "mm")
print("\n")

#------------------------------------------------------#
#------------- EXTRINSIC CALIBRATION ------------------#
#------------------------------------------------------#

image_names = glob.glob(EXTRINSIC_PATH + '*.bmp')

with np.load(CALIBRATION_OUTPUT_PATH + CAM_DATA_FILE) as X:
    (mtx, dist_coeff, r_vector, t_vector) = [X[i] for i in ('mtx', 'dist_coeff', 'r_vector', 't_vector')]

img_gray = cv.imread(image_names[0], cv.IMREAD_GRAYSCALE)

(h, w) = img_gray.shape[:2]

(new_camera_mtx, roi) = cv.getOptimalNewCameraMatrix(mtx, dist_coeff, (w, h), 1, (w, h))
undistorted_img = cv.undistort(img_gray, mtx, dist_coeff, None, new_camera_mtx)

(ret, corners) = cv.findChessboardCorners(undistorted_img, (nb_c, nb_r), None)

if not ret:
    print("#========== CHECKBOARD NOT DETECTED ==========#")
else :
    points_2d_image = cv.cornerSubPix(undistorted_img, corners, (11, 11), (-1, -1), criteria)

    points_3d_world = np.zeros((nb_c * nb_r, 3), np.float32)
    points_3d_world[:, :2] = np.mgrid[0:nb_c, 0:nb_r].T.reshape(-1, 2) * d

    #---------- TRANSLATION & ROTATION ----------#
    (ret, r_vector, t_vector) = cv.solvePnP(points_3d_world, points_2d_image, mtx, dist_coeff)

    #---------- ROTATION MATRIX ----------#
    R = cv.Rodrigues(r_vector)[0]

    #---------- CAMERA PROJECTION MATRIX ----------#
    Rt = np.hstack((R, t_vector))
    P = np.dot(mtx, Rt)

    print("\n#---------- r_vector ----------#")
    print(r_vector)

    print("\n#---------- Camera projection matrix ----------#")
    print(P)

    print("\n#---------- Rotation matrix ----------#")
    print(R)

    print("\n#---------- Translation vector ----------#")
    print(t_vector)
    print("\n")

    np.save(CALIBRATION_OUTPUT_PATH + CAM_PROJECTION_FILE, P)


new_img = cv.imread(image_names[0])

new_line = np.array([0, 0, 0, 1])
new_proj_mtx = np.vstack([P, new_line])

real_pos = np.array([[309.80303030303025], [704.3311688311687], [1]])
pos_img = (int(real_pos[0, 0]), int(real_pos[1, 0]))

# vector_pos_img = np.dot(R, real_pos)
# pos_img = (int(vector_pos_img[0, 0]), int(vector_pos_img[1, 0]))

r = 5
color = (0, 255, 0)
thickness = 1

cv.circle(img=new_img, center=pos_img, radius=r, color=color, thickness=thickness)

cv.namedWindow('circle', cv.WINDOW_AUTOSIZE) 
cv.imshow('circle', new_img) 

cv.waitKey()
cv.destroyAllWindows()