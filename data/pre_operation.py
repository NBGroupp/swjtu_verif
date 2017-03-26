#coding: utf-8
from PIL import Image

def get_table(threshold):
    
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def pre_operation(pic_name):

    im = Image.open(pic_name)
    im1 = im.convert('L')  # 灰度化
    im2 = im1.point(lambda p: p > 90 and 255)  # 灰度值大于100，设为255
    im3 = im2.point(get_table(110), '1');  # 二值化
    #im3 = im3.resize((110, 44), Image.ANTIALIAS)  # 放大
    #box = (5, 2, 108, 43)
    box = (2.5, 1, 54, 22)
    im3 = im3.crop(box)
    
    return im3  # 返回一个Image对象

if __name__ == '__main__':
    im = pre_operation('AABF.jpg')
    im.save('pre_result.bmp')
