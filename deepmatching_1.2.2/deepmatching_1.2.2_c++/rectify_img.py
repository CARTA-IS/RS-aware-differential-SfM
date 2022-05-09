import cv2
import os
import sys
import argparse
import fractions
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy.ndimage.interpolation import shift


parser = argparse.ArgumentParser()
# parser.add_argument('-name', type=str, default="name", 
#                     help='resized img dir name for optical flow visualization')
# parser.add_argument('-dir', type=str, default="dir", 
#                     help='original img dir for optical flow visualization')
# parser.add_argument('-numerator', type=int, required=True, 
#                     help='if you want resized img to be rectified is 1. if you want to rectify original img, then input the multiple as they were resized')
# parser.add_argument('-denominator', type=int, required=True, 
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
        file_list = os.listdir(f'{dir}/')
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
            src = cv2.imread(f'{dir}/' + img)
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

# def move_by_scanline(name, dir, numerator, denominator):
def displacement_x():
    path = '/home/dhlee/meissa/RS-aware-differential-SfM/examples/real_world/example/'

    # src = cv2.imread(path + 'MAX_0008.JPG')
    # dst = cv2.resize(src, (0, 0), fx=0.01, fy=0.01, interpolation=cv2.INTER_LINEAR)
    # cv2.imwrite(path + 'small.JPG', dst)

    # sys.exit()
    
    # Open image with Pillow
    # image = Image.open(path + 'MAX_0008.JPG')
    image = Image.open(path + 'small.JPG')
    
    image_array = np.array(image)
    width, height = image.size

    pixels = list(image.getdata())
    one_d = np.array(pixels)
    # print(one_d.shape)
    # print(one_d)

    pixels2 = []
    for i in range(0, height):
        pixels2.append(pixels[i * width:(i + 1) * width])

    two_d = np.array(pixels2)
    print(two_d.shape)
    print(two_d[0])

    # for i in range(0, height):
    #     two_d[i] = shift(two_d[i], 6.64)

    print(two_d.shape)
    print(shift(two_d[0], 3)) 

    img = Image.fromarray(two_d)

    img.save('test.png')


def displacement_y():
    path = '/home/dhlee/meissa/RS-aware-differential-SfM/examples/real_world/example/'
    
    image = Image.open(path + 'MAX_0008.JPG')
    width, height = image.size

    pixels = list(image.getdata())
    one_d = np.array(pixels)
    print(one_d.shape)
    
    pixels2 = []
    for i in range(0, height):
        pixels2.append(pixels[i * width:(i + 1) * width])

    two_d = np.array(pixels2, dtype=np.uint8)
    print(two_d.shape)

    img = Image.fromarray(two_d)
    img.save('test.png')

def read_this(image_file, gray_scale=False):
    image_src = cv2.imread(image_file)
    if gray_scale:
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
    else:
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
    return image_src

def pad_vector(vector, how, depth, constant_value=0):
    vect_shape = vector.shape[:2]
    if (how == 'upper') or (how == 'top'):
        pp = np.full(shape=(depth, vect_shape[1]), fill_value=constant_value)
        pv = np.vstack(tup=(pp, vector))
    elif (how == 'lower') or (how == 'bottom'):
        pp = np.full(shape=(depth, vect_shape[1]), fill_value=constant_value)
        pv = np.vstack(tup=(vector, pp))
    elif (how == 'left'):
        pp = np.full(shape=(vect_shape[0], depth), fill_value=constant_value)
        pv = np.hstack(tup=(pp, vector))
    elif (how == 'right'):
        pp = np.full(shape=(vect_shape[0], depth), fill_value=constant_value)
        pv = np.hstack(tup=(vector, pp))
    else:
        return vector
    return pv

def shifter(vect, y, y_):
    if (y > 0):
        image_trans = pad_vector(vector=vect, how='lower', depth=y_)
    elif (y < 0):
        image_trans = pad_vector(vector=vect, how='upper', depth=y_)
    else:
        image_trans = vect
    return image_trans

def shift_image(image_src, at):
    x, y = at
    x_, y_ = abs(x), abs(y)

    if (x > 0):
        left_pad = pad_vector(vector=image_src, how='left', depth=x_)
        image_trans = shifter(vect=left_pad, y=y, y_=y_)
    elif (x < 0):
        right_pad = pad_vector(vector=image_src, how='right', depth=x_)
        image_trans = shifter(vect=right_pad, y=y, y_=y_)
    else:
        image_trans = shifter(vect=image_src, y=y, y_=y_)

    return image_trans

def translate_this(image_file, at, with_plot=False, gray_scale=False, displace_x=True):
    if len(at) != 2: return False

    image_src = read_this(image_file=image_file, gray_scale=gray_scale)
    height, width, channels = image_src.shape

    if not gray_scale:
        r_image, g_image, b_image = image_src[:, :, 0], image_src[:, :, 1], image_src[:, :, 2]
        r_trans = shift_image(image_src=r_image, at=at)
        g_trans = shift_image(image_src=g_image, at=at)
        b_trans = shift_image(image_src=b_image, at=at)

        if displace_x:
            for i in range(height):
                r_trans[i] = shift(r_image[i,:], 1000)
                g_trans[i] = shift(g_image[i,:], 1000)
                b_trans[i] = shift(b_image[i,:], 1000)
        
        else:
            for i in range(width):
                r_trans[:,i] = shift(r_image[:,i], 1000)
                g_trans[:,i] = shift(g_image[:,i], 1000)
                b_trans[:,i] = shift(b_image[:,i], 1000)

        image_trans = np.dstack(tup=(r_trans, g_trans, b_trans))
        img = Image.fromarray(image_trans)
        img.save('test.png')
    else:
        image_trans = shift_image(image_src=image_src, at=at)

    # if with_plot:
    #     cmap_val = None if not gray_scale else 'gray'
    #     fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 20))

    #     ax1.axis("off")
    #     ax1.title.set_text('Original')

    #     ax2.axis("off")
    #     ax2.title.set_text("Translated")

    #     ax1.imshow(image_src, cmap=cmap_val)
    #     ax2.imshow(image_trans, cmap=cmap_val)
    #     plt.show()
    #     return True
    # return image_trans

if __name__=='__main__':
    # move_to_of(args.name, args.dir, args.numerator, args.denominator)
    path = '/home/dhlee/meissa/RS-aware-differential-SfM/examples/real_world/example/frame1.JPG'

    translate_this(image_file=path, at=(0, 0), with_plot=True, displace_x=False)
    # translate_this(image_file=path, at=(60, 60), with_plot=True)
    
