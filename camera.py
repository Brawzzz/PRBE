import os 
import numpy as np

#--------------------------------------------------------------------------------------#
#---------------------------------------- CLASS ---------------------------------------#
#--------------------------------------------------------------------------------------#
class Cam:

    def __init__(self, name, path):

        self.name = name
        self.path = path

        self.mtx = None
        self.extrinsic_mtx = None
        self.dist_coeff = None
        self.proj_mtx = None
        self.rotation_mtx = None

        self.x0 = None
        self.y0 = None
        self.intensity_th = None

    def calib(self, intrinsic_data_file, extrinsic_data_file):
        
        try:
            if(os.path.exists(intrinsic_data_file)):
                with np.load(intrinsic_data_file) as X:
                    (camera_mtx, dist_coeff) = [X[i] for i in ('mtx', 'dist_coeff')]
                    self.mtx = camera_mtx
                    self.dist_coeff = dist_coeff    

            if(os.path.exists(extrinsic_data_file)):
                with np.load(extrinsic_data_file) as X:
                    (P, R, Rt) = [X[i] for i in ('P', 'R', 'Rt')]
                    self.proj_mtx = P
                    self.rotation_mtx = R
                    self.extrinsic_mtx = Rt

        except Exception as e:

            print("#======================================================================#")
            print(f"\t\tERROR WHITH CALIBRATION FILE")
            print(f"{e}")
            print("#======================================================================#")

    def set_calib(self, mtx, extrinsic_mtx, dist_coeff, proj_mtx, rotation_mtx):
        self.mtx = mtx
        self.extrinsic_mtx = extrinsic_mtx
        self.dist_coeff = dist_coeff
        self.proj_mtx = proj_mtx
        self.rotation_mtx = rotation_mtx
    
    def set_roi(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
    
    def set_intensity_th(self, intensity_th):
        self.intensity_th = intensity_th

    def print_cam(self):

        print("#======================================================================#")
        print(f"Cam.name : {self.name}")
        print(f"Cam.path : {self.path}")
        print(f"Cam.mtx : \n {self.mtx}")
        print(f"Cam.rotation_mtx : \n {self.rotation_mtx}")
        print(f"Cam.proj_mtx : \n {self.proj_mtx}")
        print("#======================================================================#")
