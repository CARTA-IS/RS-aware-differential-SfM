import cv2
import os
import sys
import argparse
import fractions
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
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
name = 'geomdan_210803'
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
    elif (x < 0):shift_image
    else:
        image_trans = shifter(vect=image_src, y=y, y_=y_)

    return image_trans

def read_fixed_metadata(file, sensor):
    image = Image.open(file)

    info_dict = {
    "Filename": image.filename,
    "Image Size": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1)
    }

    # for label,value in info_dict.items():
    #     print(f"{label:25}: {value}")
    
    image_width = info_dict["Image Width"]
    image_height = info_dict["Image Height"]
    sensor_width = sensor[0]
    sensor_height = sensor[1]

    exifdata = image.getexif()
    
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        try:
            if isinstance(data, bytes):
                data = data.decode()
        except UnicodeDecodeError:
            continue
        print(f"{tag:25}: {data}")
        if tag == 'FocalLength':
            focal_length = data
        elif tag == 'GPSInfo':
            altitude = data[6]
    print()
    
    focal_pixel = focal_length * image_width / sensor_width

    return image_width, image_height, focal_length, focal_pixel, altitude

def read_time(file):
    image = Image.open(file)

    exifdata = image.getexif()
    
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        try:
            if isinstance(data, bytes):
                data = data.decode()
        except UnicodeDecodeError:
            continue
        if tag == 'DateTime':
            time = data
    return time

def matching_to_velocity(file1, file2, matching, focal_pixel, altitude):
    result = open(matching)
    line = result.readline()
    x, y, angle = line.split()

    files = [file1, file2]
    time = []
    
    for file in files:
        a = read_time(file)
        time.append(a)

    if time[0].split(':')[3] == time[1].split(':')[3]:
        t = int(time[1].split(':')[4]) -int(time[0].split(':')[4])
    elif time[0].split(':')[3] < time[1].split(':')[3]:
        t = int(time[1].split(':')[4]) + 60 -int(time[0].split(':')[4])

    # pixel matching was taken by 0.3 images, so need to be enlarged by 10/3
    x = float(x)*10/3
    y = float(y)*10/3

    distance_x = (x * float(altitude)) / focal_pixel
    distance_y = (y * float(altitude)) / focal_pixel
    velocity_x = distance_x / t
    velocity_y = distance_y / t

    print('altitude(m):', altitude)
    print('matching(pix):', x, y, angle)
    print('time(s):', t)
    print('focal_pixel(pix):', focal_pixel)
    print('distance(m):', distance_x, distance_y)
    print('velocity(m/s):', velocity_x, velocity_y)
    
    return velocity_x, velocity_y

def calculate_displacement_x(sensor_width, focal_length, image_width, readout_time, altitude, velocity):
    field_of_view = sensor_width / focal_length
    displace_x = (velocity * readout_time * image_width) / (field_of_view * altitude)
    return (displace_x / 1000)

def calculate_displacement_y(sensor_height, focal_length, image_height, readout_time, altitude, velocity):
    field_of_view = sensor_height / focal_length
    displace_y = (velocity * readout_time * image_height) / (field_of_view * altitude)
    return (displace_y / 1000)

def translate_this(image_file, displacement, at, with_plot=False, gray_scale=False, displace_x=True):
    if len(at) != 2: return False
    
    name = image_file.split('/')[-1]
    image_src = read_this(image_file=image_file, gray_scale=gray_scale)
    height, width, channels = image_src.shape 
    rows = height
    
    if not gray_scale:
        r_image, g_image, b_image = image_src[:, :, 0], image_src[:, :, 1], image_src[:, :, 2]
        # r_trans = shift_image(image_src=r_image, at=at)
        # g_trans = shift_image(image_src=g_image, at=at)
        # b_trans = shift_image(image_src=b_image, at=at)

        r_trans = np.zeros(r_image.shape, dtype=np.uint8)
        g_trans = np.zeros(g_image.shape, dtype=np.uint8)
        b_trans = np.zeros(b_image.shape, dtype=np.uint8)

        if displace_x:
            print('Shift X-axis')
            # + is from left to right, - is from right to left
            for i in range(rows):
                r_trans[i] = shift(r_image[i], int(displacement*i//rows))
                g_trans[i] = shift(g_image[i], int(displacement*i//rows))
                b_trans[i] = shift(b_image[i], int(displacement*i//rows))
            
                # r_trans[i] = shift(r_image[i], 1000)
                # b_trans[i] = shift(b_image[i], 1000)
                # g_trans[i] = shift(g_image[i], 1000)
        else:
            print('Shift Y-axis')
            # + is from top to bottom, - is from bottom to top
            for i in range(rows):
                try:
                    r_trans[i + int(displacement*i//rows)] = r_image[i]
                    g_trans[i + int(displacement*i//rows)] = g_image[i]
                    b_trans[i + int(displacement*i//rows)] = b_image[i]

                    # r_trans[:,i] = shift(r_image[:,i], 1000)
                    # g_trans[:,i] = shift(g_image[:,i], 1000)
                    # b_trans[:,i] = shift(b_image[:,i], 1000)
                except IndexError:
                    print('Y-axis shift finished')
                    break

        image_trans = np.dstack(tup=(r_trans, g_trans, b_trans))

        img = Image.fromarray(image_trans)
        img.save(f'test_{name}.png')

    else:
        image_trans = shift_image(image_src=image_src, at=at)

    if with_plot:
        # plot show original and translated image same. require fix
        cmap_val = None if not gray_scale else 'gray'
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 20))

        ax1.axis("off")
        ax1.title.set_text('Original')

        ax2.axis("off")
        ax2.title.set_text("Translated")

        ax1.imshow(image_src, cmap=cmap_val)
        ax2.imshow(image_trans, cmap=cmap_val)
        
        plt.show()
        return True
    return image_trans

if __name__=='__main__':
    # move_to_of(args.name, args.dir, args.numerator, args.denominator)
    path = '/home/dhlee/meissa/RS-aware-differential-SfM/examples/real_world/example/MAX_0008.JPG'
    path2 = '/home/dhlee/meissa/RS-aware-differential-SfM/examples/real_world/example/MAX_0009.JPG'
    matching = '/home/dhlee/meissa/RS-aware-differential-SfM/deepmatching_1.2.2/deepmatching_1.2.2_c++/arrow_geomdan_210803/output_geomdan_210803.txt'    
    sensor_width, sensor_height = 6.4, 4.8
    readout_time = 30

    image_width, image_height, focal_length, focal_pixel, altitude = read_fixed_metadata(path, (sensor_width, sensor_height))
    velocity_x, velocity_y = matching_to_velocity(path, path2, matching, focal_pixel, altitude)

    shift_x = calculate_displacement_x(sensor_width, focal_length, image_width, readout_time, altitude, velocity_x)
    shift_y = calculate_displacement_y(sensor_height, focal_length, image_height, readout_time, altitude, velocity_y)
    
    # If the vertical pixel displacement is bigger than 2, it is recommended to apply the Rolling Shutter Optimization
    if shift_x > 2:
        translate_this(image_file=path, displacement=shift_x, at=(0, 0), with_plot=True, displace_x=True)
    elif shift_y > 2:
        translate_this(image_file=path, displacement=shift_y, at=(0, 0), with_plot=True, displace_x=False)

    
    # if type(plot) is not bool:
    #     img = Image.fromarray(image_trans)
    #     img.save('test.png')