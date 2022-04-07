import cv2
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-dir', type=str, required=True, 
                    help='img dir for optical flow visualization')
parser.add_argument('-size', type=float, default=0.3, 
                    help='img dir for optical flow visualization')
args = parser.parse_args()
path = '/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++'

def one_third(dir, size):
    # img_list = os.listdir(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}')
    img_list = os.listdir(f'{dir}')
    name_index = dir.rfind('/')
    name = dir[name_index+1:]
    for img in img_list:
        src = cv2.imread(f'{dir}/' + img)
        height, width, channels = src.shape
        dst = cv2.resize(src, (0, 0), fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
        exist = os.path.exists(f'{path}/resize_{name}')
        if not exist:
            os.makedirs(f'{path}/resize_{name}')
        cv2.imwrite(f'{path}/resize_{name}/' + img, dst)

def three_fold():
    return

if __name__=='__main__':
    one_third(args.dir, args.size)