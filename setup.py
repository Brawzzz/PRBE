import sys
import os 
import pathlib
from enum import Enum

class Cam(Enum):
    B1 = 'B1'
    B2 = 'B2'

class Sequence(Enum):
    GROUND_MOTION = "Ground_Motion"
    NOISE = "Noise"
    SHOCK = "Shock"

SHOW_IMAGE = False

#--------------------------------------------------------------------------------------#
#---------------------------------------- PATH ----------------------------------------#
#--------------------------------------------------------------------------------------#
CAM = Cam.B1.value
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
UNDAMAGED_PATH = "./5DOF_structure/Undamaged/"

EXTRINSIC_PATH = UNDAMAGED_PATH + CAM + "/Calibration/Extrinsic/"
INTRINSIC_PATH = UNDAMAGED_PATH + CAM + "/Calibration/Intrinsic/"

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
GROUND_MOTION_PATH = UNDAMAGED_PATH + CAM + "/" + Sequence.GROUND_MOTION.value + "/"
NOISE_PATH = UNDAMAGED_PATH + CAM + "/" + Sequence.NOISE.value +"/"
SHOCK_PATH = UNDAMAGED_PATH + CAM + "/" + Sequence.SHOCK.value + "/"

#-------------------- MSER --------------------#
MSER_OUTPUT_FILE = "./output/mser/"

MSER_ALL_FILE = "MSER_all"
MSER_SELECTED_INTENSITY_FILE = "MSER_selected_intensity"
MSER_DUPLICATED_SUPRESSION_FILE = "MSER_duplicated_supression"
MSER_SELECTED_FILE = "MSER_selected"

IMG_MSER_ALL = MSER_OUTPUT_FILE + CAM_PATH + MSER_ALL_FILE + IMG_EXTENSION
IMG_MSER_SELECTED_INTENSITY = MSER_OUTPUT_FILE + CAM_PATH + MSER_SELECTED_INTENSITY_FILE + IMG_EXTENSION
IMG_MSER_DUPLICATED_SUPRESSION = MSER_OUTPUT_FILE + CAM_PATH + MSER_DUPLICATED_SUPRESSION_FILE + IMG_EXTENSION
IMG_MSER_SELECTED = MSER_OUTPUT_FILE + CAM_PATH + MSER_SELECTED_FILE + IMG_EXTENSION

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

        for cam in Cam:

            cam_path_mser = cam.value + "/"
            mser_path = os.path.join(MSER_OUTPUT_FILE, cam_path_mser)

            if not os.path.exists(mser_path):
                print(f"#==================== CREATING : {mser_path} ====================#")
                os.makedirs(mser_path, exist_ok=True)
                print("#==================== DONE ====================#")

        else:
            print("#==================== ALL REPOSITORIES ALREADY EXIST ====================#")
        
        setup = True

    except Exception as e:
        print("#==================== ERROR WHILE CREATING FILE ====================#")
        print(f"{e}")
        setup = False

    return setup

def change_sequence_path(cam, seq):

    new_path = ""
    if(seq == Sequence.GROUND_MOTION.value):
        new_path = UNDAMAGED_PATH + cam + "/" + Sequence.GROUND_MOTION.value +"/"
    elif(seq == Sequence.NOISE.value):
        new_path = UNDAMAGED_PATH + cam + "/" + Sequence.NOISE.value + "/"
    elif(seq == Sequence.SHOCK.value):
        new_path = UNDAMAGED_PATH + cam + "/" + Sequence.SHOCK.value + "/"
    
    print("#=========== Sequence path change ==========#")
    return(new_path)


def change_calib_data_path(cam, type="ext"):

    if(type == "ext"):
        EXTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + cam + "/" + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB_DATA_FILE + "_" + cam
        return(EXTRINSIC_CALIB_DATA)
    
    elif(type == "int"):
        INTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + cam + "/" + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB_DATA_FILE + "_" + cam
        return(INTRINSIC_CALIB_DATA)


def mser_all(cam_path):
    IMG_MSER_ALL = MSER_OUTPUT_FILE + cam_path + MSER_ALL_FILE + IMG_EXTENSION
    return(IMG_MSER_ALL)

def mser_selected_intensity(cam_path):
    IMG_MSER_SELECTED_INTENSITY = MSER_OUTPUT_FILE + cam_path + MSER_SELECTED_INTENSITY_FILE + IMG_EXTENSION
    return(IMG_MSER_SELECTED_INTENSITY)

def mser_duplicated_supression(cam_path):
    IMG_MSER_DUPLICATED_SUPRESSION = MSER_OUTPUT_FILE + cam_path + MSER_DUPLICATED_SUPRESSION_FILE + IMG_EXTENSION
    return(IMG_MSER_DUPLICATED_SUPRESSION)

def mser_selected(cam_path):
    IMG_MSER_SELECTED = MSER_OUTPUT_FILE + cam_path + MSER_SELECTED_FILE + IMG_EXTENSION
    return(IMG_MSER_SELECTED)