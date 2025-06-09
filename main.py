import cv2 as cv
import numpy as np
import glob
import sys
import mser
import setup as stp

print("\n")

SETUP = stp.setup_files(stp.CAM_PATH)

if(SETUP == True):

    IMG_INDEX = 20
    SEQUENCE = stp.Sequence.NOISE

    all_mser_centers = []

    for cam in stp.Cam:

        cam_path = cam.value + "/"

        #-------------------------- SEQUENCE --------------------------#
        SEQUENCE_PATH = stp.change_sequence_path(cam.value, SEQUENCE.value) 
        print(f"#=============== Selected cam : {cam.value} ===============#")
        print(f"#========== Sequence path : {SEQUENCE_PATH} ==========#")

        #-------------------------- IMAGE SELECTION --------------------------#
        image_names = glob.glob(SEQUENCE_PATH + '*.bmp')
        img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_GRAYSCALE)

        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        print("\n#============================#")
        index = image_names[IMG_INDEX].find('\\')
        if index != -1:
            print(f"Selected image : {image_names[IMG_INDEX][(index+1):]}")
            print(f"Image index : {IMG_INDEX}")
        else:
            tronquee = image_names[IMG_INDEX]
        print("#============================#\n")

        #------------------------- PARAMS -------------------------#
        if cam.value == 'B1':

            x0 = 100
            y0 = 250   

            window_width = 1300
            window_height = 500

            intensity_th = 10

        elif cam.value == 'B2':

            x0 = 0
            y0 = 250

            window_width = 1300
            window_height = 625

            intensity_th = 8

        #-------------------------- IMAGE ROI --------------------------#
        roi_rect = [x0, y0, window_width, window_height] 
        roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]
        img_blur = cv.GaussianBlur(roi_img, (3,3), 0)

        cv.imshow('roi_img', roi_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        stp.IMG_MSER_ALL = stp.mser_all(cam_path)
        stp.IMG_MSER_SELECTED_INTENSITY = stp.mser_selected_intensity(cam_path)
        stp.IMG_MSER_DUPLICATED_SUPRESSION = stp.mser_duplicated_supression(cam_path)
        stp.IMG_MSER_SELECTED = stp.mser_selected(cam_path)

        (mser_regions, mser_contours, mser_centers) = mser.detect_mser(roi_img, intensity_th)

        print("\n")
        print("#=============== MSER CENTERS ===============#")

        all_mser_centers.append(mser_centers)

    # matching_centers = mser.find_matching_centers(all_mser_centers)

    SEQUENCE_PATH = stp.change_sequence_path(stp.Cam.B1.value, SEQUENCE.value)
    image_names = glob.glob(SEQUENCE_PATH + '*.bmp')
    img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_COLOR)
    roi_rect = [100, 250, window_width, window_height] 
    roi_img_b1 = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

    SEQUENCE_PATH = stp.change_sequence_path(stp.Cam.B2.value, SEQUENCE.value)
    image_names = glob.glob(SEQUENCE_PATH + '*.bmp')
    img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_COLOR)
    roi_rect = [0, 250, window_width, window_height] 
    roi_img_b2 = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

    l1 = all_mser_centers[0]
    l2 = all_mser_centers[1]

    print(l1[8], l2[5])

    cv.circle(roi_img_b1, l1[0], 5, (0, 0, 255), -1)
    cv.circle(roi_img_b2, l2[5], 5, (0, 0, 255), -1)

    cv.imshow('img_B1', roi_img_b1)
    cv.imshow('img_B2', roi_img_b2)

    cv.waitKey(0)
    cv.destroyAllWindows()

    #-------------------------- 3D POINTS RECONSTRUCTION --------------------------#
    # stp.EXTRINSIC_CALIB_DATA = stp.change_calib_data_path(stp.Cam.B1.value, type="int")
    # data = np.load(stp.INTRINSIC_CALIB_DATA + stp.NPZ_EXTENSION)
    # camera_mtx_b1 = 'mtx'
    # dist_coeff_b1 = 'dist_coeff'

    # stp.EXTRINSIC_CALIB_DATA = stp.change_calib_data_path(stp.Cam.B2.value, type="int")
    # data = np.load(stp.INTRINSIC_CALIB_DATA + stp.NPZ_EXTENSION)
    # camera_mtx_b2 = 'mtx'
    # dist_coeff_b2 = 'dist_coeff'

    # stp.EXTRINSIC_CALIB_DATA = stp.change_calib_data_path(stp.Cam.B1.value, type="ext")
    # data = np.load(stp.EXTRINSIC_CALIB_DATA + stp.NPZ_EXTENSION)
    # projection_matrix_b1 = data['P']
    # rotation_matrix_b1 = data['R']
    # r_vector_b1 = data['r_vector']
    # t_vector_b1 = data['t_vector']
    
    # stp.EXTRINSIC_CALIB_DATA = stp.change_calib_data_path(stp.Cam.B2.value, type="ext")
    # data = np.load(stp.EXTRINSIC_CALIB_DATA + stp.NPZ_EXTENSION)
    # projection_matrix_b2 = data['P']
    # rotation_matrix_b2 = data['R']
    # r_vector_b2 = data['r_vector']
    # t_vector_b2 = data['t_vector']

    # centers_2d_image_b1 = np.array([p[0] for p in matching_centers]).T 
    # centers_2d_image_b2 = np.array([p[1] for p in matching_centers]).T 

    # points_4d = cv.triangulatePoints(projection_matrix_b1, projection_matrix_b2, centers_2d_image_b1, centers_2d_image_b2)
    
    # w = np.abs((points_4d[:3] / points_4d[3])) > 1e-8
    # points_3d_world = (points_4d[:3] / w)
    # points_3d_world_valid = points_3d_world[2, :] > 0 
    # points_3d_world = points_3d_world[:, points_3d_world_valid].T

    # print("\nPoints 3D:")
    # print(points_3d_world)

    # img = cv.cvtColor(roi_img, cv.COLOR_GRAY2RGB)

    # (projected_points, _) = cv.projectPoints(points_3d_world, r_vector_b2, t_vector_b2, camera_mtx_b2, dist_coeff_b2)
    # print("\nPoints 2D:")
    # print(projected_points)

    # for p in projected_points:
    #     cv.circle(img, tuple(p[0].astype(int)), 5, (0, 0, 255), -1)

    # cv.imshow('img', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()   
        