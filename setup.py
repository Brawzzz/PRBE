import os 
from enum import Enum
import setup_camera as stp_cam

#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------- ENUM -------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#
class Sequence(Enum):
    
    GROUND_MOTION = "Ground_Motion"
    NOISE = "Noise"
    SHOCK = "Shock"

#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------- PARAMS -----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#
SHOW_IMAGE = True

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 200

CAMS = stp_cam.CAMS 
CAM = stp_cam.CAM
CAM_PATH = stp_cam.CAM_PATH

#---------------------------- CAMERA : Basler_acA1300-200um ---------------------------#
SENSOR_X = 0.0048 
SENSOR_Y = 0.0048 

COL = 8
ROW = 6
D = 25 

#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------- PATH -------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#
IMG_EXTENSION = ".png"
NPZ_EXTENSION = ".npz"
NPY_EXTENSION = ".npy"

#------------------------------------- CALIBRATION ------------------------------------#
UNDAMAGED_PATH = "./5DOF_structure/Undamaged/"

EXTRINSIC_PATH = UNDAMAGED_PATH + CAM_PATH + "Calibration/Extrinsic/"
INTRINSIC_PATH = UNDAMAGED_PATH + CAM_PATH + "Calibration/Intrinsic/"

CALIBRATION_OUTPUT_PATH = "./output/calibration/"

INTRINSIC_CALIB_PATH = "intrinsic/"
EXTRINSIC_CALIB_PATH = "extrinsic/"
INTRINSIC_CALIB = "intrinsic_calib"
EXTRINSIC_CALIB = "extrinsic_calib"

INTRINSIC_CALIB_DATA_FILE = 'intrinsic_calib_data'
EXTRINSIC_CALIB_DATA_FILE = 'extrinsic_calib_data'

INTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + CAM_PATH + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB_DATA_FILE + "_" + CAM.name
EXTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + CAM_PATH + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB_DATA_FILE + "_" + CAM.name

IMG_INTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + CAM_PATH + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB + "_"  
IMG_EXTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + CAM_PATH + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB + IMG_EXTENSION

#-------------------------------------- SEQUENCES ------------------------------------#
GROUND_MOTION_PATH = UNDAMAGED_PATH + CAM_PATH + Sequence.GROUND_MOTION.value + "/"
NOISE_PATH = UNDAMAGED_PATH + CAM_PATH + Sequence.NOISE.value + "/"
SHOCK_PATH = UNDAMAGED_PATH + CAM_PATH + Sequence.SHOCK.value + "/"

#--------------------------------------- MSER  ---------------------------------------#
MSER_OUTPUT_FILE = "./output/mser/"

MSER_ALL_FILE = "MSER_all"
MSER_SELECTED_INTENSITY_FILE = "MSER_selected_intensity"
MSER_DUPLICATED_SUPRESSION_FILE = "MSER_duplicated_supression"
MSER_SELECTED_FILE = "MSER_selected"

IMG_MSER_ALL = MSER_OUTPUT_FILE + CAM_PATH + MSER_ALL_FILE + IMG_EXTENSION
IMG_MSER_SELECTED_INTENSITY = MSER_OUTPUT_FILE + CAM_PATH + MSER_SELECTED_INTENSITY_FILE + IMG_EXTENSION
IMG_MSER_DUPLICATED_SUPRESSION = MSER_OUTPUT_FILE + CAM_PATH + MSER_DUPLICATED_SUPRESSION_FILE + IMG_EXTENSION
IMG_MSER_SELECTED = MSER_OUTPUT_FILE + CAM_PATH + MSER_SELECTED_FILE + IMG_EXTENSION

#-------------------------------- TEMPLATE MATCHING-----------------------------------#
TEMPLATE_MATCHING_PATH = "./output/template_matching/"

TEMPLATE_FILE_NAME = 'mire_template_' + CAM.name
TEMPLATE_MATCHING_OUTPUT_NAME = "template_matching_" + CAM.name

TEMPLATE_PATH = TEMPLATE_MATCHING_PATH + CAM_PATH + TEMPLATE_FILE_NAME + IMG_EXTENSION
TEMPLATE_MATCHING_OUTPUT = TEMPLATE_MATCHING_PATH + CAM_PATH + TEMPLATE_MATCHING_OUTPUT_NAME + IMG_EXTENSION

#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------- FUNCTION ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
def setup_files(cam):

    setup = False
    try:
        calibration_path = os.path.join(CALIBRATION_OUTPUT_PATH, cam.path)
        corners_path = os.path.join(calibration_path, EXTRINSIC_CALIB_PATH.strip("/"))
        checkboard_path = os.path.join(calibration_path, INTRINSIC_CALIB_PATH.strip("/"))
        
        if not os.path.exists(calibration_path):
            print("#======================================================================#")
            print(f"CREATING : {calibration_path}")
            os.makedirs(calibration_path, exist_ok=True)
            print("\t\t\tDONE")
            print("#======================================================================#")
        
        if not os.path.exists(corners_path):
            os.makedirs(corners_path, exist_ok=True)

        if not os.path.exists(checkboard_path):
            os.makedirs(checkboard_path, exist_ok=True)

        for cam_i in CAMS:

            mser_path = os.path.join(MSER_OUTPUT_FILE, cam_i.path)
            template_matching_path = os.path.join(TEMPLATE_MATCHING_PATH, cam_i.path)

            if not os.path.exists(mser_path):
                print("#======================================================================#")
                print(f"CREATING : {mser_path}")
                os.makedirs(mser_path, exist_ok=True)
                print("\t\t\tDONE")
                print("#======================================================================#")

            if not os.path.exists(template_matching_path):
                print("#======================================================================#")
                print(f"CREATING : {template_matching_path}")
                os.makedirs(template_matching_path, exist_ok=True)
                print("\t\t\tDONE")
                print("#======================================================================#")
            
        else:
            print("#======================================================================#")
            print(f"\t\t\t\tSETUP OK")
        
        setup = True

    except Exception as e:

        print("#======================================================================#")
        print(f"\t\tERROR WHILE CREATING FILE")
        print(f"{e}")
        print("#======================================================================#")

        setup = False

    return setup

def switch_sequence_path(cam, seq):

    new_path = ""
    if(seq == Sequence.GROUND_MOTION.value):
        new_path = UNDAMAGED_PATH + cam.path + Sequence.GROUND_MOTION.value + "/"
    elif(seq == Sequence.NOISE.value):
        new_path = UNDAMAGED_PATH + cam.path + Sequence.NOISE.value + "/"
    elif(seq == Sequence.SHOCK.value):
        new_path = UNDAMAGED_PATH + cam.path + Sequence.SHOCK.value + "/"
    
    print("#======================================================================#")
    print(f"\t\t\tSequence path change")
    print("#======================================================================#")
    return(new_path)

def switch_calib_path(cam, type="ext"):
    if(type == "ext"):
        EXTRINSIC_PATH = UNDAMAGED_PATH + cam.path + "Calibration/Extrinsic/"
        return(EXTRINSIC_PATH)
    
    elif(type == "int"):
        INTRINSIC_PATH = UNDAMAGED_PATH + cam.path + "Calibration/Intrinsic/"
        return(INTRINSIC_PATH)

def switch_calib_data_path(cam, type="ext"):

    if(type == "ext"):
        EXTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + cam.path + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB_DATA_FILE + "_" + cam.name
        return(EXTRINSIC_CALIB_DATA)
    
    elif(type == "int"):
        INTRINSIC_CALIB_DATA = CALIBRATION_OUTPUT_PATH + cam.path + INTRINSIC_CALIB_PATH + INTRINSIC_CALIB_DATA_FILE + "_" + cam.name
        return(INTRINSIC_CALIB_DATA)

def switch_calib_img_path(cam, type="ext"):
    
    if(type == "ext"):
        IMG_EXTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + cam.path + EXTRINSIC_CALIB_PATH + EXTRINSIC_CALIB + IMG_EXTENSION
        return(IMG_EXTRINSIC_CALIB)
    
    elif(type == "int"):
        IMG_INTRINSIC_CALIB = CALIBRATION_OUTPUT_PATH + cam.path + EXTRINSIC_CALIB_PATH + INTRINSIC_CALIB + "_"
        return(IMG_INTRINSIC_CALIB)
    
#------------------------------------------------ MSER ------------------------------------#
def mser_all(cam):
    IMG_MSER_ALL = MSER_OUTPUT_FILE + cam.path + MSER_ALL_FILE + IMG_EXTENSION
    return(IMG_MSER_ALL)

def mser_selected_intensity(cam):
    IMG_MSER_SELECTED_INTENSITY = MSER_OUTPUT_FILE + cam.path + MSER_SELECTED_INTENSITY_FILE + IMG_EXTENSION
    return(IMG_MSER_SELECTED_INTENSITY)

def mser_duplicated_supression(cam):
    IMG_MSER_DUPLICATED_SUPRESSION = MSER_OUTPUT_FILE + cam.path + MSER_DUPLICATED_SUPRESSION_FILE + IMG_EXTENSION
    return(IMG_MSER_DUPLICATED_SUPRESSION)

def mser_selected(cam):
    IMG_MSER_SELECTED = MSER_OUTPUT_FILE + cam.path + MSER_SELECTED_FILE + IMG_EXTENSION
    return(IMG_MSER_SELECTED)

#------------------------------------------------------------------------------------------#
def switch_template_file_name(cam): 
    TEMPLATE_FILE_NAME = 'myre_template_' + cam.name
    return(TEMPLATE_FILE_NAME)

def switch_template_matching_output_name(cam): 
    TEMPLATE_MATCHING_OUTPUT_NAME = "template_matching_" + cam.name
    return(TEMPLATE_MATCHING_OUTPUT_NAME)

