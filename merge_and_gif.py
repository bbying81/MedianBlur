import cv2
import glob
import PIL.Image as Image
import os
import imageio   # 在生成gif时候用到


def merge(imgs_path,imgs_format,imgs_size,imgs_row,imgs_column,imgs_save_path):
    # imgs_path : 图片集地址
    # imgs_format : 图片格式
    # imgs_size : 每张小图片的大小,可对传进来的图片resize成imgs_size
    # imgs_row : 图片间隔，也就是合并成一张图后，一共有几行
    # img_column : 图片间隔，也就是合并成一张图后，一共有几列
    # imgs_save_path : 图片转换后的地址

    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]

    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != imgs_row * imgs_column:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")

    def image_compose():
        to_image = Image.new('RGB', (imgs_column * imgs_size, imgs_row * imgs_size))  # 创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, imgs_row + 1):
            for x in range(1, imgs_column + 1):
                from_image = Image.open(imgs_path + image_names[imgs_column * (y - 1) + x - 1]).resize(
                    (imgs_size, imgs_size), Image.ANTIALIAS)
                to_image.paste(from_image, ((x - 1) * imgs_size, (y - 1) * imgs_size))
        return to_image.save(imgs_save_path)  # 保存新图


def create_gif(image_list, gif_name, duration=0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

def main():
    image_list = ['./results/final1.jpg', './results/final2.jpg']  
    gif_name = './results/merge.gif'
    duration = 0.35  #停留时间
    create_gif(image_list, gif_name, duration)


if __name__ == '__main__':

    # merge
    imgs_path = r'./merge_data1/'  # 图片集地址，注意results图片中的数量要为imgs_row * imgs_column,在自行创建merge的时候需要关注
    imgs_format = ['.jpg', '.JPG']  # 图片格式
    imgs_size = 125  # 每张小图片resize的大小
    imgs_row = 2  # 图片间隔，也就是合并成一张图后，一共有几行
    imgs_column = 2  # 图片间隔，也就是合并成一张图后，一共有几列
    imgs_save_path = r'./results/final1.jpg'  # 图片转换后的地址
    merge(imgs_path, imgs_format, imgs_size, imgs_row, imgs_column, imgs_save_path)
	imgs_path2 = r'./merge_data2/'
	imgs_save_path2 = r'./results/final2.jpg'
	merge(imgs_path2, imgs_format, imgs_size, imgs_row, imgs_column, imgs_save_path2)

    # gif
    main()