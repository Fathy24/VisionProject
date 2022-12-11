#Libraries:
#%matplotlib inline

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



#Quick look at the data:
path = "../test_dataset/IMG/*"
img_list = glob.glob(path)
#grab a random image and display it 
idx = np.random.randint(0, len(img_list)-1)
image = mpimg.imread(img_list[idx])
plt.imshow(image)


#Calibration data:
#in the simulator you can toggle on a grid on the ground for calibration
#you can also toggle on the rock samples using the 0 key
#here is an example of the grid and one of the rocks
example_grid= "../calibration_images/example_grid1.jpg"
example_rock = "../calibration_images/example_rock1.jpg"
grid_img = mpimg.imread(example_grid)
rock_img = mpimg.imread(example_rock)

fig = plt.figure(figsize=(12,3))
plt.subplot(121)
plt.imshow(grid_img)
plt.subplot(122)
plt.imshow(rock_img)


#perspecive transform:
#define a function to perform perspective transform
#I've used the example grid image above to choose source points for the grid cell infront of the rover(each gird cell is 1 m^2 in the sim)
#define a function to perform perspective transform
def perspect_transform(img,src,dst):
  M= cv2.getPerspectiveTransform(src,dst)
  warped = cv2.warpedPerspective(img, M, (img.shape[1], img.shape[0]))
  return warped
dst = 3
bottom_offset = 5
#the numbers change according to the the grid output image in the prev function
source= np.float32([[14,140],
                    [300,140],
                    [200,95],
                    [120,95]])
destination= np.float32([[image.shape[1]/2-dst, image.shape[0]-bottom_offset],
                         [image.shape[1]/2+dst, image.shape[0]-bottom_offset],
                         [image.shape[1]/2+dst, image.shape[0]- 2*dst -bottom_offset],
                         [image.shape[1]/2-dst, image.shape[0]- 2*dst -bottom_offset]])
warped = perspect_transform(rock_img, source, destination)
plt.imshow(warped)

#idnetify pixels above the threshold
# Threshold of RGB> 160 does a nice job of identifying ground pixels only



def color_thresh(img,rgb_thresh=(160,160,160)):
    #Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    #Require that each pixel be above all three threshold values in RGB 
    #above_thresh will now contain a boolean array with "True"
    #where threshold was nest 
    above_thresh= (img[:,:,0] > rgb_thresh[0] ) \
                & (img[:,:,1] > rgb_thresh[1] )\
                & (img[:,:,0] > rgb_thresh[2] )

    color_select[above_thresh]=1            
    #Return the binary image 
    return color_select

threshed = color_thresh(warped)
plt.imshow(threshed, cmap='gray')
#scipy = misc.imsave('../output/warped_thresed,threshed*255)(path)


def rover_coords(binary_img):
    #idenify nonzero pixels
    ypos,xpos=binary_img.nonzero()

    x_pixel=-(ypos - binary_img.shape[0].astype(np.float32))
    y_pixel=-(xpos - binary_img.shape[0].astype(np.float32))

    return x_pixel,y_pixel

#Define a function to convert to radial coords in rover space 
def to_polar_coords(x_pixel,y_pixel):
    #Convert (x_pixel,y_pixel) to (distance,angle)
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist=np.sqrt(x_pixel**2+y_pixel**2)
    angles=np.arctan2(y_pixel,x_pixel)
    return dist , angles
    #Define a function to apply a rotation to pixel positions 

def rotate_pix(xpix,ypix, yaw):
    yaw_rad = yaw * np.pi/180
    xpix_rotated =(xpix * np.cos(yaw_rad)- (ypix*np.sin(yaw_rad)))
    ypix_rotated =(xpix * np.sin(yaw_rad)+ (ypix*np.sin(yaw_rad)))

    return xpix_rotated,ypix_rotated


#Define a functionto perform a translation
def translate_pix(xpix_rot,ypix_rot,xpos,ypos,scale):
    #apply a scaling and an translation
    xpix_translated=(xpix_rot)+xpos
    ypix_translated=(ypix_rot)+ypos
    #return the result 
    return xpix_translated,ypix_translated

#def pix_to_world (xpis,ypix,xpos,ypos,yaw,world_size,scale):
    #Apply rotation

#    return x_pix_world,y_pix_world

#Garb another random image 
idx=np.random.randint(0,len(img_list)-1)
image=mpimg.imread(img_list[idx])
warped=perspect_transform(image,source,destination)
threshed=color_thresh(warped)


#Calculate pixel values in rover-centric coords and distance/angle to all pixels
xpix,ypix =rover_coords(threshed)
dist,angles=to_polar_coords(xpix,ypix)
mean_dir = np.mean(angles)


#do some plotting
fig = plt.figure(figsize=(12,9))
plt.subplot(221)
plt.imshow(image)
plt.subplot(222)
plt.imshow(warped)
plt.subplot(223)
plt.imshow(threshed, cmap='gray')
plt.subplot(224)
plt.plot(xpix,ypix,'.')
plt.ylim(-160,160)
plt.xlim(0,160)
arrow_length = 100
x_arrow=arrow_length * np.cos(mean_dir)
y_arrow=arrow_length * np.sin(mean_dir)
plt.arrow(0,0,x_arrow,y_arrow,color='red',zorder=2,head_width=10,width=2)

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