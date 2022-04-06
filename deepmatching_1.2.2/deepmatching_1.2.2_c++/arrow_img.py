import os
import cv2
import sys
import argparse
from calc_angle import angle_to

parser = argparse.ArgumentParser()
parser.add_argument('-name', type=str, required=True, 
                    help=' name of resized img dir for optical flow visualization')
parser.add_argument('-num_imgs', type=int, default=0,
                    help='number of imgs for visualization, 0 means every images in dir')                    
args = parser.parse_args()
img_ext = '.JPG'
txt_ext = '.txt'
path = '/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++'

def calc_matching(name, temp):
    file_list = os.listdir(f'{path}/resize_{name}')
    txt_list = [txt for txt in file_list if txt.endswith(txt_ext)]
    txt_list.sort()

    with open(f'{path}/resize_{name}/{temp}.txt', "r") as f:
        num_lines = sum(1 for line in f)
    
    text = open(f"{path}/resize_{name}/{temp}.txt", "r")
    u = 0
    v = 0
    for j in range(num_lines):
        line = text.readline()
        if not line:
            break
        temp = []
        count = 0
        for pixel in line.split():
            temp.append(int(pixel))
            count += 1
            if count >= 4:
                # print(temp)
                break

        # This is camera direction which is opposite of optical flow
        u += (temp[2] - temp[0])
        v += (temp[3] - temp[1])
        # u += (temp[0] - temp[2])
        # v += (temp[1] - temp[3])

    u /= num_lines
    v /= num_lines
    text.close()

    d = angle_to((0, 0), (u, v))
    print(u, v, d)

    return u, v, d

# for one image
"""
def one_image_visual():
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
def multi_image_visual(name, num_imgs):
    file_list = os.listdir(f'{path}/resize_{name}')
    img_list = [img for img in file_list if img.endswith(img_ext)]
    img_list.sort()
    if not num_imgs:
        num_imgs = len(img_list)

    exist = os.path.exists(f'{path}/arrow_{name}')
    if not exist:
        os.makedirs(f'{path}/arrow_{name}')
    output = open(f'{path}/arrow_{name}/output_{name}.txt', 'w')

    for i in range(num_imgs - 1):
        temp = img_list[i].replace(img_ext, "")
        
        u, v, d = calc_matching(name, temp)

        image = cv2.imread(f'{path}/resize_{name}/' + img_list[i])
        height, width, channels = image.shape

        if (u > 0 and v > 0):
            start_point = (0, height)
            end_point = (int(u), height - int(v))
        elif (u > 0 and v <= 0):
            start_point = (0, height)
            end_point = (int(u), -1*int(v))
        elif (u <= 0 and v > 0):
            start_point = (width, height)
            end_point = (width + int(u), height - int(v))
        elif (u <= 0 and v <= 0): 
            start_point = (width, 0)
            end_point = (width + int(u), -1*int(v))

        # direction is opposite of optical flow
        output.write(f'{str(u)} {str(v)} {str(d)}')
        output.write('\n')

        color = (0, 255, 0)
        thickness = 9
        image = cv2.arrowedLine(image, start_point, end_point,
                                            color, thickness)
        cv2.imwrite(f'{path}/arrow_{name}/' + img_list[i], image)
    output.close()

if __name__=='__main__':
    multi_image_visual(args.name, args.num_imgs)