import numpy as np
from math import atan2, asin, pi, cos, sin
import math
import sys
import  argparse
import os
import cv2
from scipy.spatial.transform import Rotation as RR
### write by licheng 
class Euler:
    def __init__(self):
        self.Yaw = 0
        self.Pitch = 0
        self.Roll = 0
class Rot(object):
    def quatern2Euler(qua):
        euler = Euler()
        L = (qua[0]**2 + qua[1]**2 + qua[2]**2 + qua[3]**2)**0.5
        w = qua[0] / L
        x = qua[1] / L
        y = qua[2] / L
        z = qua[3] / L
        euler.Roll = atan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
        if euler.Roll < 0:
            euler.Roll += 2 * pi
        # print("*")
        # print(w * y - z * x)
        temp = w * y - z * x
        if temp >= 0.5:
            temp = 0.5
        elif temp <= -0.5:
            temp = -0.5
        else:
            pass
        euler.Pitch = asin(2 * temp)
        euler.Yaw = atan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))
        if euler.Yaw < 0:
            euler.Yaw += 2 * pi
        return euler

    def Euler2quatern(euler):
        roll = euler.Roll / 2
        pitch = euler.Pitch / 2
        yaw = euler.Yaw / 2
        w = cos(roll) * cos(pitch) * cos(yaw) + \
            sin(roll) * sin(pitch) * sin(yaw)
        x = sin(roll) * cos(pitch) * cos(yaw) - \
            cos(roll) * sin(pitch) * sin(yaw)
        y = cos(roll) * sin(pitch) * cos(yaw) + \
            sin(roll) * cos(pitch) * sin(yaw)
        z = cos(roll) * cos(pitch) * sin(yaw) + \
            sin(roll) * sin(pitch) * cos(yaw)
        qua = [w, x, y, z]
        return qua

    def Euler2rotMat(euler):
        qua = Rot.Euler2quatern(euler)
        R = Rot.quatern2rotMat(qua)
        return R

    def rotMat2Euler(R):
        qua = Rot.rotMat2quatern(R)
        euler = Rot.quatern2Euler(qua)
        return(euler)
def eulerAnglesToRotationMatrix(theta):
    R_x = np.array([[1, 0, 0],
                    [0, math.cos(theta[0]), -math.sin(theta[0])],
                    [0, math.sin(theta[0]), math.cos(theta[0])]
                    ])

    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0, 1, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0, 0, 1]
                    ])

    R = np.dot(R_z, np.dot(R_y, R_x))
    return R
def change_tvec_to_C(image_txt,output_path):
    newFile=open(os.path.join(output_path,"images.txt"),"w+")
    i=0
    with open(image_txt,"r+") as file:
        for line in file.readlines():
            if i<4:
                newFile.writelines(line)
                i+=1
                continue
            value=line.strip().split()
            #start trans
            if len(value)==10:
                #eu=Rot.quatern2Euler([float(value[1]),float(value[2]),float(value[3]),float(value[4])]) 
                r = RR.from_quat([float(value[2]),float(value[3]),float(value[4]),float(value[1])])
                #R=eulerAnglesToRotationMatrix([eu.Roll,eu.Pitch,eu.Yaw])
                R=r.as_matrix()
                tvec=np.array([float(value[5]),float(value[6]),float(value[7])]).reshape(3,1)
                c=np.dot(R.T,-tvec)
                newFile.writelines("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(value[0],\
                value[1],value[2],value[3],value[4],c[0,0],c[1,0],c[2,0],value[8],value[9]))
                newFile.writelines("\n")
            else:
                newFile.writelines(line)
    newFile.close()
def change_C_to_tvec(image_txt,output_path):
    # camera center to cv's tvec
    newFile=open(os.path.join(output_path,"images.txt"),"w+")
    i=0
    with open(image_txt,"r+") as file:
        for line in file.readlines():
            if i<4:
                newFile.writelines(line)
                i+=1
                continue
            value=line.strip().split()
            #start trans
            if len(value)==10:
                #eu=Rot.quatern2Euler([float(value[1]),float(value[2]),float(value[3]),float(value[4])])
                r = RR.from_quat([float(value[2]),float(value[3]),float(value[4]),float(value[1])])
                #R=eulerAnglesToRotationMatrix([eu.Roll,eu.Pitch,eu.Yaw])
                R=r.as_matrix()
                C=np.array([float(value[5]),float(value[6]),float(value[7])]).reshape(3,1)
                tvec=np.dot(R,-C)
                newFile.writelines("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(value[0],\
                value[1],value[2], value[3],value[4],tvec[0,0],tvec[1,0],tvec[2,0],value[8],value[9]))
                newFile.writelines("\n")
            else:
                newFile.writelines(line)
    newFile.close()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path",required=True)
    parser.add_argument("--flag",required=True)
    args = parser.parse_args()
    if args.flag=="1": # t to C
        change_tvec_to_C(args.input_path,args.output_path)
    else: # C to t
        change_C_to_tvec(args.input_path,args.output_path)
