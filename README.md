# MedianBlur-Opencv
- MedianBlur有两种padding方式: REPLICA & ZERO。
- "REPLICA"：填充像素与边框像素相同。
- "ZERO"：填充补零。
- MedianBlur的kernel_size可根据需要调整


## 引言
- 主要进行了median-blur的底层实现，并且将生成的结果merge并生成gif直观显示。


## 主要使用环境与库

- python3.6

- opencv-3.1.0

- matplotlib

- PIL

- imageio

## 数据
![avatar](./data/rabbit.jpg)
为1500*1500大小图片，对其进行了kernel_size=(5,5)的REPLICA与ZERO两种padding_way

![avatar](./data/rabbit.jpg)
为1500*1500大小图片，对其进行了kernel_size=(5,5)和kernel_size=(3,5)的REPLICA

## 运行
run median-blur.py 进行median-blur
run merge_and_gif.py 对结果图进行merge与gif

## 结果
![avatar](./result/merge.gif)


