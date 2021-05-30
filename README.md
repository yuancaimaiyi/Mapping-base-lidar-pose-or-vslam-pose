# Mapping-base-lidar-pose-or-vslam-pose
I simply modified the colmap,when it reconstructs from known pose ,only let it optimize rotation ,fixing position!  
Why do I do this, because when reconstructing from a known pose, if you use the rtk position, there is no need to optimize the position during BA fine-tuning. You can fine-tune the rotation, but this is a very loose coupling, if you want to use rtk to constrain BA, you can look at openmvg **sfm_data_BA_ceres.cpp**. You can implement it in colmap immediately！！！！！！！
reference : https://colmap.github.io/faq.html?highlight=known%20pose#reconstruct-sparse-dense-model-from-known-camera-poses  


## first step
### (1) base/cost_functions.h replace your colmap code
### (2) controllers/bundle_adjustment.cc replace your colmap code
### (3) optim/bundle_adjustment.cc replace your colmap code 
## second step
### example folder

..........model

................images.txt   // your piror pose  

................cameras.txt   

................points3D.txt      //empty file  

..........trans.py  // trans colmap tvec to camera center  and trans camera center to colmap tvec(-R.T*tvec=C   and tvec=-R*C)  

..........run  3D_from_prior_pose.sh 

