import cv2
import os
import sys

img_list = os.listdir('/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/real')
for img in img_list:
    src = cv2.imread('/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/real/' + img)
    height, width, channels = src.shape
    dst = cv2.resize(src, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite('/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/resize_real/' + 'resize_' + img, dst)

