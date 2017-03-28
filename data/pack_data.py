import os
import numpy as np
from PIL import Image
from pre_operation import pre_operation


def cut_captcha(im):
    """ 传入经过预处理的Image对象，分割为四张字母.
        分割成功返回分割位置列表：
            [(left, upper, right, lower), (...), (...), (...)] 
        分割失败返回 False
    """
    pic_sizes = im.size  # （长， 高）
    b_dot_sum = {'col':[0 for x in range(pic_sizes[0])], 
            'row': [0 for x in range(pic_sizes[1])]}
    
    # 统计每行每列黑色像素点个数
    for i in range(pic_sizes[0]):  # 图片列
        for j in range(pic_sizes[1]):  # 图片行
            if im.getpixel((i, j)) == 0: # 黑色像素点
                b_dot_sum['col'][i] += 1
                b_dot_sum['row'][j] += 1
    
    # 寻找行边界
    for j in range(pic_sizes[1] + 1):
        if b_dot_sum['row'][j] > 2:  # 黑色像素点数大于5的即为上边界
            upper = j
            break
    # 寻找底边界
    for j in range(upper + 1, pic_sizes[1]):
        if b_dot_sum['row'][j] < 1:  # 黑色像素点数小于5的即为下边界
            lower = j
            break
    # 从左到右寻找四个字母左右位置
    let_pic_boxes = []
    front = 0
    back = 0
    i = 0
    while i < pic_sizes[0]:
        if not front and b_dot_sum['col'][i] >= 1:  # J等字母左边界像素点少
            # 寻找到一个字母的左边界
            front = i
        elif front > 0 and (b_dot_sum['col'][i] == 0 or i == pic_sizes[0] - 2): # L等字母右边界像素点少
            # 寻找到一个字母的右边界
            back = i
        elif front and i - front >= 16:
            # 字母有粘结
            let_list = b_dot_sum['col'][front:i]
            min_value = min(let_list)
            min_pos = front + let_list.index(min_value) + 1
            if min_pos - front < 2:  # 选取的最小位置离front太近
               min_pos += 1
               while b_dot_sum['col'][min_pos] != min_value and min_pos < pic_sizes[0] - 1:
                   min_pos += 1
            back = min_pos
            i = min_pos + 1  # i跳回到粘结位置附近
        if front and back:
            # 一个字母左右边界都已经找到
            if back - front < 2:  # 失败
                break
            let_pic_boxes.append((front, upper, back, lower))
            front = 0
            back = 0
        i += 1
    if len(let_pic_boxes) != 4:
        return False
    else:
        return let_pic_boxes


def test_accuracy(pic_dir_pos):
    """ 测试 cut_captcha 准确度"""
    import os 
    file_num = 0
    success_num = 0
    f = open('fail.txt', 'w')
    for root, dirs, files in os.walk(pic_dir_pos):
        for one_pic in files:
            file_num += 1
            im = pre_operation(os.path.join(root, one_pic))
            if cut_captcha(im):
                success_num += 1
            else:
                f.write(one_pic + '\n')
            if file_num > 10000:
                break
    f.close()
    print(str(file_num) + ' pictures')
    print(str(success_num) + ' success')
    print(str(success_num * 100 // file_num) + ' % success rate')


def pack_data(raw_captcha_dir, pack_num):
    """ 传入含有原始验证码图片的文件夹位置，打包为训练神经网络输入形式。
        输入形式是一个列表，基本元素是元组(x, y)。元组的第一个值x是一
        个324 × 1的 numpy.ndarray 对象，第二个值是一个10×1的 numpy.ndarray
        对象，含有x的正确值。
        [((单张字母图片像素值), (24维正确结果)), (...), ....] """
    let_list = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    data = []
    suc_packed_data = 0
    for root, dirs, files in os.walk(raw_captcha_dir):
        for one_pic in files:
            pre_im = pre_operation(os.path.join(root, one_pic))
            four_let_boxes = cut_captcha(pre_im)
            if not four_let_boxes:
                continue
            # 截取成功
            cor_letters = os.path.splitext(one_pic)[0]
            for i, one_let_box in enumerate(four_let_boxes):
                # 截取字母贴到白色背景上
                # 像素值列表
                pixels = np.zeros((18*18, 1), dtype=float)
                pos = 0
                for x in range(one_let_box[0], one_let_box[2] + 1):
                    for y in range(one_let_box[1], one_let_box[3] + 1):
                        pixels[pos] = pre_im.getpixel((x, y))
                        pos += 1
                # 正确结果列表
                cor_let = np.zeros((26, 1), dtype=float)
                cor_let[let_list.index(cor_letters[i])] = 1  # 结果numpy矩阵
                data.append((pixels, cor_let))
                suc_packed_data += 1
                if suc_packed_data == pack_num:
                    return data

if __name__ == '__main__':
    import pickle
    data = pack_data('test_pics', 200000)
    
    f = open('data.pkl', 'wb')
    pickle.dump([data[0:150000], data[150000:200000]], f)  # 150k训练数据,50k验证数据
    f.close()
