import cv2 as cv
import numpy as np
import sys
import matplotlib.pyplot as plt
import muDIC as dic
import muDIC.vlab as vlab
from matplotlib import cm
from matplotlib.patches import Rectangle


sys.path.insert(0, r"C:/COURS/SUPMECA/C2/PRBE/utilities/muDIC_patch")

#---------- PATH ----------#
CAM = 'B2'

GROUND_MOTION_PATH = "C:/COURS/SUPMECA/C2/S8/PRBE/Test-5DOF_structure/Undamaged/" + CAM + "/Ground motion/"

image_stack = dic.image_stack_from_folder(GROUND_MOTION_PATH, file_type=".bmp")

#------------ MESH ------------#
mesher = dic.Mesher()
mesh = mesher.mesh(image_stack)

# inputs = dic.DICInput(mesh, image_stack)
# dic_job = dic.DICAnalysis(inputs)
# results = dic_job.run()

# #------------ FIELD COMPUTATION ------------#
# fields = dic.Fields(results)
# true_strain = fields.true_strain # (img_frames, i, j, e, n) 

# #------------ VIZUALISATION ------------#
# viz = dic.Visualizer(fields, images=image_stack)
# viz.show(field="True strain", component=(1,1), frame=85)