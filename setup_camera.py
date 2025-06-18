import camera as cam


B1 = cam.Cam('B1', 'B1/')
B1.set_roi(x0=120, y0=565)
B1.set_intensity_th(intensity_th=8)

B2 = cam.Cam('B2', 'B2/')
B2.set_roi(x0=0, y0=400)
B2.set_intensity_th(intensity_th=8)

CAMS = [B1, B2]
CAM_INDEX = 1

CAM = CAMS[CAM_INDEX]
CAM_PATH = CAM.path