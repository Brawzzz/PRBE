import sys
import cv2 as cv
import numpy as np
import setup as stp
import glob
import matplotlib.pyplot as plt
import muDIC as dic


image_stack = dic.image_stack_from_folder(stp.NOISE_PATH, file_type=".bmp")

mesher = dic.Mesher()
mesh = mesher.mesh(image_stack)

inputs = dic.DICInput(mesh, image_stack)

dic_job = dic.DICAnalysis(inputs)
results = dic_job.run()

fields = dic.Fields(results)

viz = dic.Visualizer(fields, images=image_stack)
viz.show(field="True strain", component=(1,1), frame=0)