import cv2
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-name', type=str, required=True, 
                    help='img dir for optical flow visualization')
args = parser.parse_args()

def move_to_of(name):
    optical_flow = open("ofd.txt", "r")
    img_list = os.listdir(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}')
    for img in img_list:
        src = cv2.imread(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}/' + img)
        height, width, channels = src.shape
        line = optical_flow.readline()
        if not line:
            break
        u, v, d = line.split()
        
        M = np.float32([[1, 0, u], [0, 1, v]])
        dst = cv2.warpAffine(src, M, (width, height))
        cv2.imwrite(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}/' + 'move_' + img, dst)
    
    optical_flow.close()

if __name__=='__main__':
    move_to_of(args.name)