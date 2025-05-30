import sys
import os 
import pathlib

#--------------------------------------------------------------------------------------#
#---------------------------------------- PATH ----------------------------------------#
#--------------------------------------------------------------------------------------#
CAM = 'B1'
CAM_PATH = CAM + '/'

#-------------------- CAMERA : Basler_acA1300-200um --------------------#
SENSOR_X = 0.0048 
SENSOR_Y = 0.0048 

COL = 8
ROW = 6
D = 25 

#-------------------- IMAGES --------------------#
IMG_EXTENSION = ".png"
NPZ_EXTENSION = ".npz"
NPY_EXTENSION = ".npy"

#-------------------- CALIBRATION --------------------#
EXTRINSIC_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Calibration/Intrinsic/"

CALIBRATION_OUTPUT_PATH = "./output/calibration/"

INTRINSIC_CALIB_PATH = "intrinsic/"
EXTRINSIC_CALIB_PATH = "extrinsic/"
INTRINSIC_CALIB = "intrinsic_calib"
EXTRINSIC_CALIB = "extrinsic_calib"

INTRINSIC_CALIB_DATA_FILE = 'intrinsic_calib_data'
EXTRINSIC_CALIB_DATA_FILE = 'extrinsic_calib_data'

INTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + CAM_PATH + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB_DATA_FILE + "_" + CAM
EXTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + CAM_PATH + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB_DATA_FILE + "_" + CAM

IMG_INTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + CAM_PATH + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB + "_"  
IMG_EXTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + CAM_PATH + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB + IMG_EXTENSION

#-------------------- SEQUENCES --------------------#
GROUND_MOTION_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Ground_Motion/"
NOISE_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Noise/"
SHOCK_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Shock/"

#-------------------- MSER --------------------#
MSER_OUTPUT_FILE = "./output/mser/"

ALL_MSER_FILE = "all_MSER"
CIRCULAR_MSER_FILE = "circular_MSER"
DUPLICATED_MSER_SUPRESSION_FILE = "duplicated_MSER_supression"
SELECTED_MSER_INTENSITY_FILE = "selected_MSER_intensity"
SELECTED_MSER_FILE = "selected_MSER"

#------------------------------------------------------------------------------------------#
#---------------------------------------- FUNCTION ----------------------------------------#
#------------------------------------------------------------------------------------------#
def setup_files(cam_path):

    setup = False
    try:
        calibration_path = os.path.join(CALIBRATION_OUTPUT_PATH, cam_path)
        corners_path = os.path.join(calibration_path, EXTRINSIC_CALIB_PATH.strip("/"))
        checkboard_path = os.path.join(calibration_path, INTRINSIC_CALIB_PATH.strip("/"))

        if not os.path.exists(calibration_path):
            print(f"#==================== CREATING : {calibration_path} ====================#")
            os.makedirs(calibration_path, exist_ok=True)
            print("#==================== DONE ====================#")
        
        if not os.path.exists(corners_path):
            os.makedirs(corners_path, exist_ok=True)

        if not os.path.exists(checkboard_path):
            os.makedirs(checkboard_path, exist_ok=True)

        else:
            print("#==================== ALL REPOSITORIES ALREADY EXIST ====================#")
        
        setup = True

    except Exception as e:
        print("#==================== ERROR WHILE CREATING FILE ====================#")
        print(f"{e}")
        setup = False

    return setup