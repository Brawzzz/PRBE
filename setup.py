import sys
import os 
import pathlib

#--------------------------------------------------------------------------------------#
#---------------------------------------- PATH ----------------------------------------#
#--------------------------------------------------------------------------------------#
CAM = 'B2'
CAM_PATH = CAM + '/'

#---------- CAMERA : Basler_acA1300-200um ----------#
SENSOR_X = 0.0048 
SENSOR_Y = 0.0048 

EXTRINSIC_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Calibration/Intrinsic/"

COL = 8
ROW = 6
D = 25 

GROUND_MOTION_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Ground_Motion/"
NOISE_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Noise/"
SHOCK_PATH = "./5DOF_structure/Undamaged/" + CAM + "/Shock/"

CALIBRATION_OUTPUT_PATH = "./output/calibration/"
MSER_OUTPUT_FILE = "./output/mser/"
CORNERS = "/corners/"

CHECKBOARD_FILE = 'checkerboard_calibration'
CAM_DATA_FILE = 'calibration_data_cam_basler_acA1300'
CAM_PROJECTION_FILE = 'camera_projection_matrix'

ALL_MSER_FILE = "all_MSER"
CIRCULAR_MSER_FILE = "circular_MSER"
DUPLICATED_MSER_SUPRESSION_FILE = "duplicated_MSER_supression"
SELECTED_MSER_INTENSITY_FILE = "selected_MSER_intensity"
SELECTED_MSER_FILE = "selected_MSER"

IMG_EXTENSION = ".png"
NPZ_EXTENSION = ".npz"
NPY_EXTENSION = ".npy"


def setup_files(cam_path):

    setup = False
    try:
        calibration_path = os.path.join(CALIBRATION_OUTPUT_PATH, cam_path)
        corners_path = os.path.join(calibration_path, CORNERS.strip("/"))

        if not os.path.exists(calibration_path):
            print(f"========== CREATING : {calibration_path} ==========")
            os.makedirs(calibration_path, exist_ok=True)
            print("========== DONE ==========")

        if not os.path.exists(corners_path):
            os.makedirs(corners_path, exist_ok=True)

        print("========== FILE PATH OK ==========")
        setup = True

    except Exception as e:
        print("========== ERROR WHILE CREATING FILE ==========")
        print(f"{e}")
        setup = False

    return setup

setup = setup_files(CAM_PATH)