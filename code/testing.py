import cv2 # openCV for perspective transform 
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.misc #for saving images as needed
import glob #for reading in a list of images as folder
#import imageio
#imageio.plugins.ffmpeg.download()
from email.mime import image
#from turtle import width
#import tkinter as TK




#Calibration data:
#in the simulator you can toggle on a grid on the ground for calibration
#you can also toggle on the rock samples using the 0 key
#here is an example of the grid and one of the rocks
example_grid= "../calibration_images/example_grid1.jpg"
example_rock = "../calibration_images/example_rock1.jpg"
grid_img = mpimg.imread(example_grid)
rock_img = mpimg.imread(example_rock)

def color_thresh_obstacles(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] < rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

K = color_thresh_obstacles(rock_img)
plt.imshow(K)
plt.show()