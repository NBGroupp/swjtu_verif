# swjtu_verif
## 教务验证码识别

### 数据预处理

preprocess.m是初期的matlab函数文件，当时尚未做成自动化的脚本

preprocess.py是python脚本文件，可以直接在命令行python3 preprocess.py，运行前需要先将data文件夹下的captcha.7z中的图片文件解压至./pic文件夹下，生成的训练数据存入./picchar文件夹下。

### 训练网络

在network.py中修改参数后直接在命令行python3 network.py即可，程序默认是从打包的data.pkl中获取数据，data.pkl见data文件夹

### 数据预处理思路

教务网验证码大概长这样：

![验证码示例](http://img.blog.csdn.net/20170404172338028?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRXJpY19LRVk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

利用和
http://www.cnblogs.com/beer/p/5672678.html
相同的方法进行处理

#### 分割

分割大概遇到几类问题：

1.字符位置不固定

2.字符宽度不固定

3.降噪后些许字符有粘连

**采用下面的算法解决问题：**

1.首先统计每一行字符的黑色像素点个数和每一列的黑色像素点个数

2.对于行需求取2个边界，像素点个数pixel<2即为边界，对于列需求取5个边界则需要考虑以下情况：

以pixel>0定义字符最左边界，设为front；

i自front向右移动，若遇到pixel=0且1<i-front<17，则back=i;

若i-front>=17，则m=min(pixel(i:i-15))，取back等于pixel=m的最右一列

若i-front<17且已到列最右侧，则back=列的最大值

若分割数！=4，则跳过本图进行下次分割

分割后的图片均放在背景为20*20的白色背景上。放置位置在左上方。

#### 训练集和测试集的制作

人工看有点烦。。。就用Google的pytessor把爬下来的验证码重命名，成功分割的图片就以图片名字的四个字母命名。放到list中，随机抽取10000作为测试集，剩余作为训练集。
