# -- coding: utf-8 --  
#=====================================================================

import glob
import numpy as np
from scipy import misc
from keras.layers import Input, Convolution2D, MaxPooling2D, Flatten, Activation, Dense, Dropout
from keras.models import Model
from keras.utils.np_utils import to_categorical
from tqdm import tqdm
import sys

if (len(sys.argv)<=1):    #传参
	print("Please input Deep Learning project name")
	sys.exit()

	
#读取数据
imgs = glob.glob('SAMPLE/*.jpg') #SAMPLE里所有的图片
img_size = misc.imread(imgs[0]).shape #图片imgs[0]的shape
data = np.array([misc.imresize(misc.imread(i), img_size).T for i in imgs]) #data为所有图片像素矩阵
data = 1 - data.astype(float)/255.0     
target = np.array([[ord(i)-ord('0') for i in j[7:11]] for j in imgs])
target = [to_categorical(target[:,i], 43) for i in range(4)] #one-hot（4个分类器）
img_size = img_size[::-1]

#build VGG 16 CNN
input = Input(img_size)
cnn = Dropout(0.25)(input)
cnn = Convolution2D(32, 3, 3)(cnn)
cnn = MaxPooling2D((2, 2))(cnn)
cnn = Convolution2D(32, 3, 3)(cnn)
cnn = MaxPooling2D((2, 2))(cnn)
cnn = Activation('relu')(cnn)
cnn = Convolution2D(64, 3, 3)(cnn)
cnn = MaxPooling2D((2, 2))(cnn)
cnn = Activation('relu')(cnn)
cnn = Convolution2D(64, 3, 3)(cnn)
cnn = MaxPooling2D((2, 2))(cnn)
cnn = Flatten()(cnn)
cnn = Dense(512)(cnn)#if not delete
cnn = Activation('relu')(cnn)
cnn = Dropout(0.5)(cnn)#if not delete

#4个分类器，每个分类器43个神经元，输出43个字符的概率
model = Model(input=input, output=[Dense(43, activation='softmax')(cnn) for i in range(4)]) 

#编译
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#model.summary()

batch_size = 256
nb_epoch = 50
model.fit(data, target, batch_size=batch_size, nb_epoch=nb_epoch) #训练
model.save_weights(str(sys.argv[1]) + "_weights.model") #保存训练的权值矩阵
rr = [''.join(chr(i.argmax()+ord('0')) for i in model.predict(data[[k]])) for k in tqdm(range(len(data)))]
s = [imgs[i][7:11]==rr[i] for i in range(len(imgs))]

print ("\ntotal acc: %f \n"%(1.0*sum(s)/len(s)))

def ocr(filename):
	img = misc.imresize(misc.imread(filename), img_size[::-1]).T
	img = np.array([1 - img.astype(float)/255])
	return ''.join(chr(i.argmax()+ord('0')) for i in model.predict(img))
	
print 'test result: '+(ocr('test.jpg')) #测试test.jpg
json_string = model.to_json()  
open(str(sys.argv[1]) + '_model.json','w').write(json_string)
