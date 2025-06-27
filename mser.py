import cv2 as cv
import numpy as np
import glob
import sys
import setup as stp
import setup_camera as stp_cam
from intensity_check import intensity_check
from duplicated_check import duplicated_check


#--------------------------------------------------------------------------------------------------#
#----------------------------------------------- MSER ---------------------------------------------#
#--------------------------------------------------------------------------------------------------#
def detect_mser(img, roi_img, cam):
    
    roi_img_clone = roi_img.copy()
    roi_img_clone = cv.cvtColor(roi_img, cv.COLOR_GRAY2RGB)

    #---------------- MSER DETECTION ----------------#
    mser = cv.MSER_create(delta=2, min_area=9, max_area=20, max_variation=0.2)

    (regions, b_box) = mser.detectRegions(roi_img)
    
    ellipse_contours = []
    for r in regions:

        ellipse = cv.fitEllipse(r)
        (center, axis, angle) = ellipse

        center = tuple(int(x) for x in center)
        axis = tuple(int(x) for x in axis)
        angle = int(angle)
        
        ellipse_cnt = cv.ellipse2Poly(center=center, axes=axis, angle=angle, arcStart=0, arcEnd=360, delta=5)
        ellipse_contours.append(ellipse_cnt)

        cv.ellipse(roi_img_clone, ellipse, color=(0, 0, 255), thickness=1)

    hulls = [cv.convexHull(cnt) for cnt in ellipse_contours]

    if(stp.SHOW_IMAGE):
        cv.namedWindow('all MSER', cv.WINDOW_AUTOSIZE) 
        cv.imshow('all MSER', roi_img_clone) 
        cv.waitKey()
        cv.destroyAllWindows()
        
    cv.imwrite(stp.IMG_MSER_ALL, roi_img_clone)

    #----------------- MSER SELECTION ---------------#
    (regions_int, contours_int, Centers_int) = intensity_check(roi_img, regions, hulls, cam.intensity_th)
    (regions, contours, centers, b_box) = duplicated_check(roi_img, regions_int, contours_int, Centers_int)

    centers.sort(key=lambda x : (x[0]), reverse=False)

    result_centroid = []
    for ind in b_box:

        temp = []
        corner_min = np.array((ind[0], ind[1]))
        corner_max = np.array((ind[0] + ind[2], ind[1] + ind[3]))

        for centroid in centers:
            if ((np.array(centroid) < corner_max).all() and (np.array(centroid) > corner_min).all()):
                temp.append(centroid)

        if temp:
            result_centroid.append(tuple(np.mean(temp, axis=0, dtype=int)))
    
    result_centroid = list(set(result_centroid))
    result_centroid.sort(key=lambda x : (x[0]), reverse=False)

    #----------------- TARNSLATION ---------------#
    for i in range(0, len(result_centroid)):
        result_centroid[i] = np.array(result_centroid[i]) + [cam.x0, cam.y0]

    print("#======================================================================#")
    print(f"Number of mire detected : {len(result_centroid)}")
    print("#======================================================================#")

    #------------------- VISUALIZATION -------------------#
    img_clone = img.copy()
    img_clone = cv.cvtColor(img, cv.COLOR_GRAY2RGB) 

    for c in result_centroid:
        img_clone = cv.circle(img_clone, c, radius=4, color=(255, 0, 0), thickness=2)

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)
    thickness = 1

    for i, c in enumerate(result_centroid):
        number = str(i)
        cv.putText(img_clone, number, (c[0] + 10, c[1] - 10), font, font_scale, color, thickness)

    cv.namedWindow('selected MSER', cv.WINDOW_AUTOSIZE)
    cv.imshow('selected MSER', img_clone) 
    cv.waitKey()
    cv.destroyAllWindows()

    cv.imwrite(stp.IMG_MSER_SELECTED, img_clone)

    return(regions, contours, result_centroid)

#--------------------------------------------------------------------------------------------------#
#-------------------------------------------- MATCHING --------------------------------------------#
#--------------------------------------------------------------------------------------------------#
def find_matching_centers(mser_centers, mtx_b1_b2):

    mser_centers_b1_pixels = mser_centers[0]
    mser_centers_b2_pixels = mser_centers[1]

    optic_center_cam_b1 = stp_cam.B1.extrinsic_mtx[:3, 3]
    optic_center_cam_b2 = stp_cam.B2.extrinsic_mtx[:3, 3]

    ray_vectors_b1 = []
    ray_vectors_b2 = []

    for c1_pixels in mser_centers_b1_pixels :

        c1_pixels_homogeneous = np.array([c1_pixels[0], c1_pixels[1], 1])
        c1_cam_b1 = np.linalg.inv(stp_cam.B1.mtx) @ c1_pixels_homogeneous
        c1_cam_b1_w = np.linalg.inv(stp_cam.B1.rotation_mtx) @ c1_cam_b1

        ray_vector_c1 = c1_cam_b1_w - optic_center_cam_b1
        ray_vectors_b1.append((ray_vector_c1, c1_pixels))
    
    for c2_pixels in mser_centers_b2_pixels :

        c2_pixels_homogeneous = np.array([c2_pixels[0], c2_pixels[1], 1])
        c2_cam_b2 = np.linalg.inv(stp_cam.B2.mtx) @ c2_pixels_homogeneous
        c2_cam_b2_w = np.linalg.inv(stp_cam.B2.rotation_mtx) @ c2_cam_b2

        ray_vector_c2 = c2_cam_b2_w - optic_center_cam_b2
        ray_vectors_b2.append((ray_vector_c2, c2_pixels))

    d_min = sys.float_info.max

    matching_points = []
    for ray_b1 in ray_vectors_b1:
        
        c1_pixels = ray_b1[1]
        ray_b1 = ray_b1[0]
        
        for ray_b2 in ray_vectors_b2:

            c2_pixels = ray_b2[1]
            ray_b2 = ray_b2[0]

            r = optic_center_cam_b1 - optic_center_cam_b2
            cross = np.cross(ray_b1, ray_b2)

            d = abs(np.dot(r, cross))/ np.linalg.norm(cross)

            if(d <= d_min):
                d_min = d

                c1_pixels_valid = c1_pixels
                c2_pixels_valid = c2_pixels

        matching_points.append((c1_pixels_valid, c2_pixels_valid))

    return(matching_points)

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- STEREO 3D POINTS ---------------------------------------#
#--------------------------------------------------------------------------------------------------#
def stereo_points(IMG_INDEX, SEQUENCE, rotation_mtx):

    all_mser_centers = []

    for cam in stp.CAMS:

        #-------------------------- SEQUENCE --------------------------#
        SEQUENCE_PATH = stp.switch_sequence_path(cam, SEQUENCE.value) 
        print("#======================================================================#")
        print(f"\t\t\tSelected cam : {cam.name}")
        print(f"\tSequence path : {SEQUENCE_PATH}")
        print("#======================================================================#")

        #-------------------------- IMAGE SELECTION --------------------------#
        image_names = sorted(glob.glob(SEQUENCE_PATH + '*.bmp'))
        img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_GRAYSCALE)
        
        if(stp.SHOW_IMAGE):
            cv.imshow('img', img)
            cv.waitKey(0)
            cv.destroyAllWindows()

        print("\n#======================================================================#")
        index = image_names[IMG_INDEX].find('\\')
        if index != -1:
            print(f"Selected image : {image_names[IMG_INDEX][(index+1):]}")
            print(f"\t\t\tImage index : {IMG_INDEX}")
        else:
            tronquee = image_names[IMG_INDEX]
        print("#======================================================================#\n")

        #-------------------------- UNDISTORD IMAGE --------------------------#
        img = cv.undistort(img, cam.mtx, cam.dist_coeff)

        #-------------------------- IMAGE ROI --------------------------#
        roi_rect = [cam.x0, cam.y0, stp.WINDOW_WIDTH, stp.WINDOW_HEIGHT] 
        roi_img = img[int(roi_rect[1]):int(roi_rect[1] + roi_rect[3]), int(roi_rect[0]):int(roi_rect[0] + roi_rect[2])]

        if(stp.SHOW_IMAGE):
            cv.imshow('roi_img', roi_img)
            cv.waitKey(0)
            cv.destroyAllWindows()

        stp.IMG_MSER_ALL = stp.mser_all(cam)
        stp.IMG_MSER_SELECTED_INTENSITY = stp.mser_selected_intensity(cam)
        stp.IMG_MSER_DUPLICATED_SUPRESSION = stp.mser_duplicated_supression(cam)
        stp.IMG_MSER_SELECTED = stp.mser_selected(cam)

        (mser_regions, mser_contours, mser_centers) = detect_mser(img, roi_img, cam)

        print("\n")
        print("#======================================================================#")
        print("\t\t\tMATCHING MSER CENTERS\n")

        all_mser_centers.append(mser_centers)

    matching_centers = find_matching_centers(all_mser_centers, rotation_mtx)

    k = 0
    for cam in stp.CAMS:

        #-------------------------- SEQUENCE --------------------------#
        SEQUENCE_PATH = stp.switch_sequence_path(cam, SEQUENCE.value) 
        print("#======================================================================#")
        print(f"\t\t\tSelected cam : {cam.name}")
        print(f"\tSequence path : {SEQUENCE_PATH}")
        print("#======================================================================#")

        #-------------------------- IMAGE SELECTION --------------------------#
        image_names = sorted(glob.glob(SEQUENCE_PATH + '*.bmp'))
        img = cv.imread(image_names[IMG_INDEX], cv.IMREAD_COLOR)
        
        #-------------------------- UNDISTORD IMAGE --------------------------#
        img = cv.undistort(img, cam.mtx, cam.dist_coeff)

        #-------------------------- RENDER IMAGE --------------------------#
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 255)
        thickness = 1
        for i in range(0, len(matching_centers)):
            number = str(i)
            c = matching_centers[i][k]
            cv.circle(img, c, radius=4, color=(255, 0, 0), thickness=2)
            cv.putText(img, number, (c[0] + 10, c[1] - 10), font, font_scale, color, thickness)

        cv.imshow('roi_img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite(stp.MSER_OUTPUT_FILE + cam.path + "sorted_" + cam.name + stp.IMG_EXTENSION, img)

        k += 1

    print("#======================================================================#")
    
    return matching_centers

    

















