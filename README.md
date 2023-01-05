# Project Description
For at least three decades, scientists have advocated the return of geological samples from Mars. One early concept was the Sample Collection for Investigation of Mars (SCIM) proposal, which involved sending a spacecraft in a grazing pass through Mars's upper atmosphere to collect dust and air samples without landing or orbiting. As of late 1999, the MSR mission was anticipated to be launched from Earth in 2003 and 2005. Each was to deliver a rover and a Mars ascent vehicle, and a French supplied Mars orbiter with Earth return capability was to be included in 2005. Sample containers orbited by both MAVs were to reach Earth in 2008. This mission concept, considered by NASA's Mars Exploration Program to return samples by 2008, was cancelled
following a program review. In this project, we’ll do computer vision for robotics. We are going to build a Sample & Return Rover in simulation. Mainly, we’ll control the robot from images streamed from a camera mounted on the robot. The project aims to do autonomous mapping and navigation given an initial map of the environment. Realistically speaking, the hard work is done now that you have the mapping component! You will have the option to choose whether to send orders like the throttle, brake, and steering with each new image the rover's camera produces.

## Phase 1-Basic Functionality
The inset image at the bottom right when you're running in autonomous mode is packed with information. In this image, your map of navigable terrain, obstacles and rock sample locations is overplotted with the ground truth map. In addition, some overall statistics are presented ncluding total time, percent of the world you have mapped, the fidelity (accuracy) of your map, and the number of rocks you have located (mapped) and how many you have collected. The requirement for a passing submission of the first phase is to map at least 40% of the environment at 60% fidelity and locate at least one of the rock samples (note: you're not required to collect any rocks, just map the location of at least 1). Each time you launch the simulator in autonomous mode there will be 6 rock samples scattered randomly about the environment and your rover will start at random orientation in the middle of the map.

Phase 1 source code: https://drive.google.com/drive/folders/1QucHjE7lxpwGZftF7M_QE8kovCf5aZBv?usp=sharing 


## Phase 2-Collect and Return
In this stage, build upon your previous implementation to map at least 95% of the environment at 85% fidelity. All while colliding with the least number of obstacles. (The maximum number of collisions allowed will be announced at the beginning of phase 2) Also, there is a robotic arm located on the vehicle. In this phase, you should also locate and use the robotics arm to pick up at least five rocks out of the six, and then return them back to the start position.

# Dependencies to download
![image](https://user-images.githubusercontent.com/66957026/210679923-04a1a078-b041-401e-9430-46c011c5dd1d.png)


# How to Use
open repo:
![image](https://user-images.githubusercontent.com/93041833/206929367-7125ca55-00a8-49d2-8b1d-9f7b72c53ffb.png)

open the file named code
![image](https://user-images.githubusercontent.com/93041833/206929394-8fc2078f-c8bf-49ce-94f1-5f7d9b7de460.png)

right click then open in terminal
![image](https://user-images.githubusercontent.com/93041833/206929513-3090a169-6cfc-438c-be71-31ca3e2d1903.png)

then type "y" to activate debugger mode
![image](https://user-images.githubusercontent.com/93041833/206929592-77b3ecf2-9a52-444a-af1d-79d7aed62683.png)

when activating debugger mode it will automatically take images instantly when rover is moving and put them simultaneously in the dubugger folder insid code folder:
![image](https://user-images.githubusercontent.com/93041833/206930014-6651008d-8193-4b7a-a96b-47fd4c503355.png)

the rover will keep moving automatically in autonmous mode and locating rocks:
![image](https://user-images.githubusercontent.com/93041833/206930205-a1461aeb-8844-4e21-bd10-8d65fb1f7456.png)

# Test Results 
results are different for different simulator resolutions


<img width="489" alt="Screen Shot 2023-01-05 at 3 23 38 AM" src="https://user-images.githubusercontent.com/66957026/210680573-d09903f2-10b9-48f0-939a-8c0095674e17.png">

<img width="605" alt="Screen Shot 2023-01-05 at 2 34 40 AM" src="https://user-images.githubusercontent.com/66957026/210680624-352aad53-3f86-4d39-8528-c2c8f8743f21.png">

<img width="601" alt="Screen Shot 2023-01-05 at 2 34 20 AM" src="https://user-images.githubusercontent.com/66957026/210680646-f9a47141-6a0b-4e2a-a411-4d124a46090d.png">

<img width="606" alt="Screen Shot 2023-01-05 at 12 52 52 AM" src="https://user-images.githubusercontent.com/66957026/210680656-3a60d8b4-21c3-4b40-b786-abf26d81152a.png">


video of run: https://drive.google.com/drive/folders/1DqhUCZuHyJ-yrPvJBji1jTuYNpYoEg-Z?usp=share_link
