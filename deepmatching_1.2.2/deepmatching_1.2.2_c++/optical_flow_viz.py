import os
import cv2
import sys
import argparse
from calc_angle import angle_to

# bring output.txt to make (u,v)
parser = argparse.ArgumentParser()
parser.add_argument('-dir', type=str, default="resize_real", 
                    help='img dir for optical flow visualization')
parser.add_argument('-num_imgs', type=int, default=0,
                    help='choose number of imgs used for visualization')                    
args = parser.parse_args()

# for one image
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


# for several images
def multi_image_visual(dir, num_imgs):
    img_list = os.listdir(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}')
    img_list.sort()
    if not num_imgs:
        num_imgs = len(img_list)
    for i in range(num_imgs - 1):
        temp = img_list[i].replace("resize_", "")
        name = temp.replace(".JPG", "")
        with open(f"output_{name}.txt", "r") as f:
            num_lines = sum(1 for line in f)
            # print(f"{img_list[i]}\noutput_{name}.txt\ntotal lines: {num_lines}")

        output_file = open(f"output_{name}.txt", "r")
        u = 0
        v = 0
        for j in range(num_lines):
            line = output_file.readline()
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
        output_file.close()
        print(u, v)

        image = cv2.imread(f'/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/{dir}/' + img_list[i])
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
            end_point = (width + int(u), height - int(v))
        elif (u <= 0 and v <= 0): 
            start_point = (width, 0)
            end_point = (width + int(u), -1*int(v))

        direction = angle_to(start_point, (u,v))
        print(direction)
        lines = [str(u), str(v), str(direction)]
        with open(f"of_{name}.txt", "w") as f:
            f.write('\n'.join(lines))

        color = (0, 255, 0)
        thickness = 9
        image = cv2.arrowedLine(image, start_point, end_point,
                                            color, thickness)
        cv2.imwrite(f'arrow_{name}.JPG', image)

if __name__=='__main__':
    multi_image_visual(args.dir, args.num_imgs)