import numpy as np
import scipy
import cv2

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(150, 150, 150)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

def obstacle_thresh(img, rgb_thresh=(150, 150, 150)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    below_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] < rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[below_thresh] = 1
    # Return the binary image
    return color_select

def rock_thresh(img, threshold_low=(100, 100, 20), threshold_high=(210, 210, 55)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:, :, 0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > threshold_low[0]) & (img[:,:,0] < threshold_high[0])  \
                   & (img[:,:,1] > threshold_low[1]) & (img[:,:,1] < threshold_high[1]) \
                   & (img[:,:,2] > threshold_low[2]) & (img[:,:,2] < threshold_high[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    return color_select
#def rock_thresh(img, threshold_low=(85,85,30)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:, :, 0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > threshold_low[0])  \
                   & (img[:,:,1] > threshold_low[1])\
                   & (img[:,:,2] < threshold_low[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    return color_select
# Define a function to convert to rover-centric coordinates
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the
    # center bottom of the image.
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle)
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to apply a rotation to pixel positions
def rotate_pix(xpix, ypix, yaw):
    # TODO:
    # Convert yaw to radians
    # Apply a rotation
    yaw_rad = yaw * np.pi / 180
    x_rotated = xpix * np.cos(yaw_rad) - ypix * np.sin(yaw_rad)
    y_rotated = xpix * np.sin(yaw_rad) + ypix * np.cos(yaw_rad)
    # Return the result
    return x_rotated, y_rotated

# Define a function to perform a translation
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale):
    # TODO:
    # Apply a scaling and a translation
    x_world = np.int_(xpos + (xpix_rot / scale))
    y_world = np.int_(ypos + (ypix_rot / scale))
    # Return the result
    return x_world, y_world

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):

    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    # mask = cv2.warpPerspective(np.ones_like(img[:, :, 0]), M, (img.shape[1], img.shape[0]))
    # Removed mask because it occasionally creates seemingly arbitrary errors 
    # return warped, mask (whenever mask is used)
    # Mask can be initialized by returning "mask" in the "rock_thresh" section
    return warped 


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover,debug):
    # Perform perception steps to update Rover()

    # 1) Define source and destination points for perspective transform
    
    dst_size = 5
    # Equates to "box size"
    bottom_offset = 6
    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    destination = np.float32([[Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - bottom_offset],
                  [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - bottom_offset],
                  [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],
                  [Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],])

    # 2) Apply perspective transform 
    if debug:
        warped = perspect_transform(Rover.img, source, destination)
        threshed_ground = color_thresh(warped)
        threshed_obstacle = obstacle_thresh(warped)
        threshed_rock = rock_thresh(warped)
        cv2.imwrite("debuger/ "+ str(Rover.total_time) + "original.jpg",Rover.img)
        cv2.imwrite("debuger/ "+str(Rover.total_time) + "threshed.jpg",threshed_ground)
        cv2.imwrite("debuger/ "+str(Rover.total_time) + "warped.jpg",warped)
        cv2.imwrite("debuger/ "+str(Rover.total_time) + "obstacles.jpg",threshed_obstacle)
        cv2.imwrite("debuger/ "+str(Rover.total_time) + "rock.jpg",threshed_rock)

    else:
        warped = perspect_transform(Rover.img, source, destination)
        threshed_ground = color_thresh(warped)
        threshed_obstacle = obstacle_thresh(warped)
        threshed_rock = rock_thresh(warped)

    # Note: add mask back to this point whenever used
    
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    #circle = cv2.circle(blank.copy(),((warped.shape[1]//2)-50,(warped.shape[1]//2 +65)),130,(255,255,255),-1)


    #masking
    blank = np.zeros_like(warped)
    circle = cv2.circle(blank.copy(),((warped.shape[1]//2)-50,(warped.shape[1]//2 +65)),130,(255,255,255),-1)
    circle = color_thresh(circle,(254,254,254))
    threshed_ground = cv2.bitwise_and(threshed_ground,circle)
    threshed_ground =scipy.ndimage.binary_erosion(threshed_ground, structure=np.ones((5,5))).astype(threshed_ground.dtype)

    # 4) Update Rover.vision_image (this will be displayed on left side of screen) 
       # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
           #      Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
           #      Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image
    Rover.vision_image[:,:,2] = threshed_ground * 255
    Rover.vision_image[:,:,0] = threshed_obstacle * 255
    Rover.vision_image[:,:,1] = threshed_rock * 255
    
    # 5) Convert map image pixel values to rover-centric coords 
    ground_xpix, ground_ypix = rover_coords(threshed_ground)
    obstacle_xpix, obstacle_ypix = rover_coords(threshed_obstacle)
    rock_xpix, rock_ypix = rover_coords(threshed_rock)
    rover_xpos, rover_ypos = Rover.pos
    rover_yaw  = Rover.yaw

    # 6) Convert rover-centric pixel values to world coordinates 
    scale = 10
    ground_x_world, ground_y_world = pix_to_world(ground_xpix, ground_ypix, rover_xpos, rover_ypos, Rover.yaw, Rover.worldmap.shape[0], scale)
    obstacle_x_world, obstacle_y_world = pix_to_world(obstacle_xpix, obstacle_ypix, rover_xpos, rover_ypos, Rover.yaw, Rover.worldmap.shape[0], scale)
    rock_x_world, rock_y_world = pix_to_world(rock_xpix, rock_ypix, rover_xpos, rover_ypos, Rover.yaw, Rover.worldmap.shape[0], scale*2)

    # 7) Update Rover worldmap (to be displayed on right side of screen)
      # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
          #      Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
          #      Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    if (Rover.roll < 1 or Rover.roll > 359):
        if (Rover.pitch < 1 or Rover.pitch > 359):
            Rover.worldmap[ground_y_world, ground_x_world, 2] = 50 
            Rover.worldmap[rock_y_world, rock_x_world, 1] = 50
            Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] = 25

    # 8) Convert rover-centric pixel positions to polar coordinates
      # Update Rover pixel distances and angles
      # Rover.nav_dists = rover_centric_pixel_distances
      # Rover.nav_angles = rover_centric_angles
    dist, angles = to_polar_coords(ground_xpix, ground_ypix)
    rock_dist, rock_angles = to_polar_coords(rock_xpix, rock_ypix)
    obstacle_dist, obstacle_angles = to_polar_coords(obstacle_xpix, obstacle_ypix)

    # Update the Rover's distances and angles
    Rover.nav_dists = dist
    Rover.nav_angles = angles
    Rover.rock_dist = rock_dist
    Rover.rock_angles = rock_angles
    Rover.obstacle_dist = obstacle_dist
    Rover.obstacle_angles = obstacle_angles
    return Rover