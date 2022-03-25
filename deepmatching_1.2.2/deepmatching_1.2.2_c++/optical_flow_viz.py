import os
import cv2
import sys
import argparse

# bring output.txt to make (u,v)
parser = argparse.ArgumentParser()
parser.add_argument('-img', type=str, 
                    help='an image for optical flow visualization')
args = parser.parse_args()

# for one image
"""
with open("output.txt", "r") as fp:
    num_lines = sum(1 for line in fp)
    print("Total lines:", num_lines)

f = open("output.txt", "r")
u = 0
v = 0
for i in range(num_lines):
    line = f.readline()
    if not line:
        break
    temp = []
    count = 0
    for pixel in line.split():
        temp.append(int(pixel))
        count += 1
        if count >= 4:
            break
    u += temp[2] - temp[0]
    v += temp[3] - temp[1]

u /= num_lines
v /= num_lines

print(u, v)

f.close()

path = r'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/' + args.img

# Reading an image in default mode
image = cv2.imread(path)
height, width, channels = image.shape

# Window name in which image is displayed
window_name = 'Image'

# Start coordinate, here (0, 0)
# represents the top left corner of image
if (u > 0 and v > 0):
    start_point = (0, height)
    end_point = (int(u), height - int(v))
elif (u > 0 and v <= 0):
    start_point = (0, height)
    end_point = (int(u), -1*int(v))
elif (u <= 0 and v > 0):
    start_point = (width, height)
    end_point = (width - int(u), height - int(v))
elif (u <= 0 and v <= 0): 
    start_point = (width, 0)
    end_point = (width + int(u), -1*int(v))

# Green color in BGR
color = (0, 255, 0)

# Line thickness of 9 px
thickness = 9

# Using cv2.arrowedLine() method
# Draw a diagonal green arrow line
# with thickness of 9 px
image = cv2.arrowedLine(image, start_point, end_point,
									color, thickness)

cv2.imwrite('arrow_image.png', image)
"""

# for several images
img_list = os.listdir(r'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/test_result')
img_list.sort()
for i in range(len(img_list) - 1):
    # print(img_list[i][7:13])
    with open(f"output_{img_list[i][7:13]}.txt", "r") as fp:
        num_lines = sum(1 for line in fp)
        print(f"output_{img_list[i][7:13]}.txt total lines:", num_lines)

    f = open(f"output_{img_list[i][7:13]}.txt", "r")
    u = 0
    v = 0
    for j in range(num_lines):
        line = f.readline()
        if not line:
            break
        temp = []
        count = 0
        for pixel in line.split():
            temp.append(int(pixel))
            count += 1
            if count >= 4:
                break
        u += temp[2] - temp[0]
        v += temp[3] - temp[1]

    u /= num_lines
    v /= num_lines

    print(u, v)
    f.close()

    print(img_list[i])
    image = cv2.imread(r'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/test_result/' + img_list[i])
    height, width, channels = image.shape
    window_name = 'Image'

    if (u > 0 and v > 0):
        start_point = (0, height)
        end_point = (int(u), height - int(v))
    elif (u > 0 and v <= 0):
        start_point = (0, height)
        end_point = (int(u), -1*int(v))
    elif (u <= 0 and v > 0):
        start_point = (width, height)
        end_point = (width - int(u), height - int(v))
    elif (u <= 0 and v <= 0): 
        start_point = (width, 0)
        end_point = (width + int(u), -1*int(v))


    color = (0, 255, 0)
    thickness = 9
    image = cv2.arrowedLine(image, start_point, end_point,
                                        color, thickness)
    cv2.imwrite(f'arrow_{img_list[i][7:13]}.JPG', image)


