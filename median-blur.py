import numpy as np
import os
import cv2
import copy
import glob
import matplotlib.pyplot as plt

# img:input 1-, 3-, or 4-channel image; when ksize is 3 or 5, the image depth should be CV_8U, CV_16U, or CV_32F, for larger aperture sizes, it can only be CV_8U.
# kernel:aperture linear size; it must be odd and greater than 1, for example: 3, 5, 7 ..
# padding_way : REPLICA & ZERO
def medianBlur(img, kernel, padding_way):
    img_width = img.shape[1]
    img_height = img.shape[0]
    pad_rsize = kernel[0] // 2  
    pad_csize = kernel[1] // 2

    # 生成一个值为0的单通道数组
    zeros = np.zeros([img_height + 2 * pad_rsize, img_width + 2 * pad_csize])
    if len(img.shape) == 2:   #(height,width)灰度图，len(img.shape)==2
        padding_image = zeros
    else:    
        padding_image = cv2.merge([zeros,zeros,zeros])   ##(height,width,3)，len(img.shape)==3

    if padding_way == "ZERO":
        padding_image[pad_rsize:img_height + pad_rsize, pad_csize:img_width + pad_csize] = img[:,:]
    if padding_way == "REPLICA":
        padding_image[pad_rsize:img_height + pad_rsize, pad_csize:img_width + pad_csize] = img[:,:]
        for i in range(pad_rsize):
            # up
            padding_image[i, pad_csize:img_width + pad_csize] = img[0]
            # down
            padding_image[-i + img_height + 2 * pad_rsize - 1:, pad_csize:img_width + pad_csize] = img[-1]
            # left
            padding_image[pad_rsize :img_height + pad_rsize, i] = img[:, 0]
            # right
            padding_image[pad_rsize :img_height + pad_rsize, -i + img_width + 2 * pad_csize-1] = img[:, -1]
            # Four corners filling
            for j in range(pad_rsize):
                padding_image[i, j] = img[0, 0]
                padding_image[i, -j + img_width + 2 * pad_csize -1] = img[0, -1]
                padding_image[-i + img_height + 2 * pad_rsize -1, j] = img[-1, 0]
                padding_image[-i + img_height + 2 * pad_rsize -1, -j + img_width + 2*pad_csize -1] = img[-1, -1]

    wind_ones = np.ones([kernel[0], kernel[1]])
	
    Kimg_height = (img_height-kernel[0] + 2 * pad_rsize) + 1
    Kimg_width = (img_width-kernel[1] + 2 * pad_csize) + 1
    Kimg_zeros = np.zeros([Kimg_height, Kimg_width])
    if len(img.shape) == 2:   
        Kimg = Kimg_zeros
        for j in range(img_width):
            for i in range(img_height):
                wind_img = wind_img * padding_image[i:i + kernel[0], j:j + kernel[1]]
                list_wind = wind_img.flatten()
                # medianvalue=mediannum(list_wind)
                if i >= Kimg_height or j >= Kimg_width:
                    break
                else:
                    list_wind.sort()  #生成list_wind由小到大排序
                    Kimg[i, j] = list_wind[kernel[0] // 2 + 1]
        return Kimg       
    else:    
        B_Kimg = Kimg_zeros
        G_Kimg = Kimg_zeros
        R_Kimg = Kimg_zeros
        B,G,R = cv2.split(padding_image)
        #B
        for j in range(img_width):
            for i in range(img_height):
                B_wind_img = wind_ones * B[i:i + kernel[0], j:j + kernel[1]]
                B_list_wind = B_wind_img.flatten()
                if i >= Kimg_height or j >= Kimg_width:
                    break
                else:
                    B_list_wind.sort()
                    B_Kimg[i, j] = B_list_wind[kernel[0] // 2 + 1]
        #G
        for j in range(img_width):
            for i in range(img_height):
                G_wind_img = wind_ones * G[i:i + kernel[0], j:j + kernel[1]]
                G_list_wind = G_wind_img.flatten()
                if i >= Kimg_height or j >= Kimg_width:
                    break
                else:
                    G_list_wind.sort()
                    G_Kimg[i, j] = G_list_wind[kernel[0] // 2 + 1]  
        #R
        for j in range(img_width):
            for i in range(img_height):
                R_wind_img = wind_ones * R[i:i + kernel[0], j:j + kernel[1]]
                R_list_wind = R_wind_img.flatten()
                if i >= Kimg_height or j >= Kimg_width:
                    break
                else:
                    R_list_wind.sort()
                    R_Kimg[i, j] = R_list_wind[kernel[0] // 2 + 1]
        Kimg = cv2.merge((R_Kimg,G_Kimg,B_Kimg))
        return Kimg  
		
if __name__=="__main__":
    save_path = './results'
    imgs = glob.glob('./data\*.jpg')
    for img in imgs:
        img_str = os.path.basename(img)
        print(img_str)
        pic = cv2.imread(img)
        medianBlur = medianBlur(pic, (5,5), 'REPLICA')
		#medianBlur = medianBlur(pic, (3,5), 'REPLICA')
		#medianBlur = medianBlur(pic, (5,5), 'ZERO')		
        save_name = save_path + '/' + img_str[:-4] + '_' + 'medianBlur' +'.jpg'
        cv2.imwrite(save_name,medianBlur)