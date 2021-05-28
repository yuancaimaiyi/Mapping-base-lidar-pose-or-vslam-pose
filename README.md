# Mapping-base-lidar-pose-or-vslam-pose
I modified the colmap,when  it reconstructs from known pose ,only let it optimize rotation ,fixing position! 
## first step
### (1) base/cost_functions.h replace your code
### (2) controllers/bundle_adjustment.cc replace your code
### (3) optim/bundle_adjustment.cc replace your code 
## second step
### example folder

..........model

................images.txt   // your piror pose  

................cameras.txt   

................points3D.txt      //empty file  

..........trans.py  // trans colmap tvec to camera center  and trans camera center to colmap tvec(-R.T*tvec=C   and tvec=-R*C)  

..........run  3D_from_prior_pose.sh 

