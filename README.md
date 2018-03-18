# swjtu_verif

## 说明

### \data

 包含数据及相关代码。

获取数据的主要步骤为：

1. 连接URL，下载图片
2. 利用Google开源的pytesser3库将验证码识别为对应结果以备训练（==讲道理如果是为了做验证码识别直接用Google的库就好了，但是我们不是为了训练网络而训练网络么==）
3. 图片打包

### \BP

BP网络参考了mnielsen](https://github.com/mnielsen)的[教程](http://neuralnetworksanddeeplearning.com/)实现，在此向mnielsen表示感谢！  

使用BP神经网络搭建的验证码识别网络，训练识别26个字母的网络，识别一套验证码的大致步骤为：

1. 图片预处理，包括灰度化、二值化，将图片进行切分成为四个子图
2. 将每个子图送入网络进行识别
3. 将结果拼接得到最后的结果

详见目录下文件说明

### \CNN

使用CNN神经网络搭建的验证码识别网络，直接识别验证码内容无须分割

详见目录下文件说明
