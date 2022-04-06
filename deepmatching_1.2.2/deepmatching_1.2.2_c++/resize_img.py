import cv2
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-dir', type=str, required=True, 
                    help='img dir for optical flow visualization')
args = parser.parse_args()

def one_third(dir):
    # img_list = os.listdir(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}')
    img_list = os.listdir(f'{dir}')

    for img in img_list:
        src = cv2.imread(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}/' + img)
        height, width, channels = src.shape
        dst = cv2.resize(src, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/resize_{dir}/' + img, dst)

def three_fold():
    return

if __name__=='__main__':
    one_third()