import cv2
import os
import sys
import numpy as np
import argparse
import fractions

parser = argparse.ArgumentParser()
parser.add_argument('-name', type=str, default="name", 
                    help='resized img dir name for optical flow visualization')
parser.add_argument('-dir', type=str, default="dir", 
                    help='original img dir for optical flow visualization')
parser.add_argument('-numerator', type=int, required=True, 
                    help='if you want resized img to be rectified is 1. if you want to rectify original img, then input the multiple as they were resized')
parser.add_argument('-denominator', type=int, required=True, 
                    help='if you want resized img to be rectified is 1. if you want to rectify original img, then input the multiple as they were resized')
# parser.add_argument('-size', type=float, required=True, 
#                     help='if you want resized img to be rectified is 1. if you want to rectify original img, then input the multiple as they were resized')
args = parser.parse_args()
path = '/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++'
img_ext = '.JPG'
txt_ext = '.txt'

def move_to_of(name, dir, numerator, denominator):
    is_original = False
    size = fractions.Fraction(numerator, denominator)
    
    if size == 1 and name != 'name' and dir == 'dir':
        file_list = os.listdir(f'{path}/resize_{name}')
        img_list = [img for img in file_list if img.endswith(img_ext)]
        img_list.sort()
        print('Rectify resized images')
    elif size != 1 and name != 'name' and dir != 'dir':
        file_list = os.listdir(f'{dir}')
        img_list = [img for img in file_list if img.endswith(img_ext)]
        img_list.sort()
        is_original = True
        print('Rectify original images')
    else:
        print('Check if arguments are correctly inserted')
        sys.exit()
        
    optical_flow = open(f'{path}/arrow_{name}/output_{name}.txt', "r")

    for img in img_list:
        if is_original:
            src = cv2.imread(f'{dir}' + img)
        else:
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
    move_to_of(args.name, args.dir, args.numerator, args.denominator)