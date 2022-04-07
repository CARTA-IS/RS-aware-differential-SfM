import cv2
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-name', type=str, required=True, 
                    help='img dir for optical flow visualization')
parser.add_argument('-size', type=float, required=True, 
                    help='if you want resized img to be rectified is 1. if you want to rectify original img, then input the multiple as they were resized')
args = parser.parse_args()
path = '/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++'
img_ext = '.JPG'
txt_ext = '.txt'

def move_to_of(name, size):
    optical_flow = open(f"{path}/arrow_{name}/output_{name}.txt", "r")
    file_list = os.listdir(f'{path}/resize_{name}')
    img_list = [img for img in file_list if img.endswith(img_ext)]
    img_list.sort()

    for img in img_list:
        src = cv2.imread(f'{path}/resize_{name}/' + img)
        height, width, channels = src.shape
        line = optical_flow.readline()
        
        if not line:
            break

        u, v, d = line.split()
        M = np.float32([[1, 0, float(u)*size], [0, 1, float(v)*size]])
        dst = cv2.warpAffine(src, M, (width, height))

        exist = os.path.exists(f'{path}/rectify_{name}')
        if not exist:
            os.makedirs(f'{path}/rectify_{name}')
        cv2.imwrite(f'{path}/rectify_{name}/' + img, dst)
    
    optical_flow.close()

if __name__=='__main__':
    move_to_of(args.name, args.size)