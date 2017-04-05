# -- coding: utf-8 --   
#=====================================================================


from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.utils import np_utils


batch_size = 128
nb_classes = 10
nb_epoch = 20

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784) #将60000*28*28的张量变为60000*784,即将每幅图片变为一个向量
X_test = X_test.reshape(10000, 784)  
X_train = X_train.astype('float32')  #将数据类型变为float
X_test = X_test.astype('float32')
X_train /= 255		#数据大小由0~255归一化到0~1
X_test /= 255
print(X_train.shape[0], 'train samples') #X_train的第一维大小输出为60000
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
#one-hot  比如将5变为[0000010000],位数为nb_classes
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#搭网络
model = Sequential()
model.add(Dense(512, input_shape=(784,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))  #除第一层外，其他曾只要有output参数即可，input=上一层的output
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))

model.summary()

#编译
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

#训练
history = model.fit(X_train, Y_train,          
                    batch_size=batch_size, nb_epoch=nb_epoch,
                    verbose=1, validation_data=(X_test, Y_test))

#网络测试
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])  #所有loss函数平均值
print('Test accuracy:', score[1]) #测试准确率
