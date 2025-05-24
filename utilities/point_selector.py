import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import cv2
import numpy as np

""" 
    This script is used to select the control points on the image by right-clicking on the image.
    The selected points are saved as a txt file. (selected_points.txt)
"""

def onclick(event, points, point_index):

    if event.button == 3:

        points.append((event.xdata, event.ydata))
        point_index = len(points) - 1
        plt.plot(event.xdata, event.ydata, 'ro') 
        plt.text(event.xdata, event.ydata, str(point_index), color='r', fontsize=14) 
        plt.draw()

        print(f"Point {point_index}: ({event.xdata}, {event.ydata})")

if __name__ == '__main__':

    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(title = "Select the image") 
    image = cv2.imread(file_path)

    points = []
    point_index = 1
    
    fig = plt.figure()
    fig.suptitle('Select the control points by right-clicking on the image')
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, points, point_index))
    plt.imshow(image)
    plt.show()

    print("Selected points: ", points)
    np.savetxt('./utilities/selected_points.txt', points, fmt='%f', delimiter=',')