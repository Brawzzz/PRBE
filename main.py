import cv2 as cv
import numpy as np
import glob
import mser
import setup as stp
import setup_camera as stp_cam


#------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------- CALIBRATION ----------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#
INTRINSIC_CALIB_DATA_1 = stp.switch_calib_data_path(stp_cam.B1, type="int")
EXTRINSIC_CALIB_DATA_1 = stp.switch_calib_data_path(stp_cam.B1, type="ext")
INTRINSIC_CALIB_DATA_1 = INTRINSIC_CALIB_DATA_1 + stp.NPZ_EXTENSION
EXTRINSIC_CALIB_DATA_1 = EXTRINSIC_CALIB_DATA_1 + stp.NPZ_EXTENSION
stp_cam.B1.calib(INTRINSIC_CALIB_DATA_1, EXTRINSIC_CALIB_DATA_1)

print("#======================================================================#")
print('\tEXTRINSIC_CALIB_DATA_1')
print(stp_cam.B1.extrinsic_mtx)
print("\n")
print("#======================================================================#")


INTRINSIC_CALIB_DATA_2 = stp.switch_calib_data_path(stp_cam.B2, type="int")
EXTRINSIC_CALIB_DATA_2 = stp.switch_calib_data_path(stp_cam.B2, type="ext")
INTRINSIC_CALIB_DATA_2 = INTRINSIC_CALIB_DATA_2 + stp.NPZ_EXTENSION
EXTRINSIC_CALIB_DATA_2 = EXTRINSIC_CALIB_DATA_2 + stp.NPZ_EXTENSION
stp_cam.B2.calib(INTRINSIC_CALIB_DATA_2, EXTRINSIC_CALIB_DATA_2)

print("#======================================================================#")
print('\tEXTRINSIC_CALIB_DATA_2')
print(stp_cam.B2.extrinsic_mtx)
print("\n")
print("#======================================================================#")

MATRIX_B1_B2 = np.linalg.inv(stp_cam.B1.extrinsic_mtx) @ stp_cam.B2.extrinsic_mtx
MATRIX_B2_B1 = np.linalg.inv(stp_cam.B2.extrinsic_mtx) @ stp_cam.B1.extrinsic_mtx

print("#======================================================================#")
print('\tMATRIX_B1_B2')
print(MATRIX_B1_B2)
print("\n")
print('\tMATRIX_B2_B1')
print(MATRIX_B2_B1)
print("#======================================================================#")

print("\n#======================================================================#")
SETUP_B1 = stp.setup_files(stp_cam.B1)
SETUP_B2 = stp.setup_files(stp_cam.B2)

if(SETUP_B1 and SETUP_B2):

    IMG_INDEX = 0
    SEQUENCE = stp.Sequence.NOISE


    stereo_points = mser.stereo_points(IMG_INDEX, SEQUENCE, MATRIX_B1_B2)

    #--------------------------------------------------------------------------------------------------#
    #----------------------------------------------- PROCESS ------------------------------------------#
    #--------------------------------------------------------------------------------------------------#