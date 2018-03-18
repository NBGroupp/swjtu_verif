#coding: utf-8
from PIL import Image
import os
import numpy as np

def pre_operation(pic_name):
    im = Image.open(pic_name)
    im = im.convert('L')  # 图像灰度化处理
    l,h = im.size
    img = np.asarray(im) # 转换为矩阵
    img.flags.writeable = True  # 允许读写
    # 二值化
    for i in range(h):
	    for j in range(l):
		    if img[i,j]>110:
			    img[i,j]=255 
		    else:
			    img[i,j]=0
	# 去掉黑框 
    i=0 
    for j in range(l):
	    img[i,j] = 255
    j=0 
    for i in range(h):
	    img[i,j] = 255
	# 去噪
    flag=np.zeros([h,l], dtype=int)
    count = 0
    for i in range(h):
        for j in range(l):
            if(img[i,j]==255):# 不是黑点则忽略
                continue 
            if(((i==0) and (j==0)) or ((i==0) and (j==l-1)) or ((i==h-1) and (j==0)) or ((i==h-1) and (j==l-1))):# A类点
                if((i==0) and (j==0)):# 左上角
                    count=int(img[i+1,j]==0)+int(img[i,j+1]==0)+int(img[i+1,j+1]==0)
                elif((i==h-1) and (j==0)):# 左下角
                    count=int(img[i,j+1]==0)+int(img[i-1,j]==0)+int(img[i-1,j+1]==0)
                elif((i==0) and (j==l-1)):# 右上角
                    count=int(img[i,j-1]==0)+int(img[i+1,j]==0)+int(img[i+1,j-1]==0)
                else:# 右下角
                    count=int(img[i,j-1]==0)+int(img[i-1,j]==0)+int(img[i-1,j-1]==0)
            elif((i==0) or (j==0) or (i==h-1) or (j==l-1)): # B类点
                if(j==0):# 左侧
                    count=int(img[i+1,j]==0)+int(img[i,j+1]==0)+int(img[i+1,j+1]==0)+int(img[i-1,j]==0)+int(img[i-1,j+1]==0)
                elif(i==0):# 上侧
                    count=int(img[i+1,j]==0)+int(img[i+1,j+1]==0)+int(img[i+1,j-1]==0)+int(img[i,j-1]==0)+int(img[i,j+1]==0)
                elif(j==l-1):# 右侧
                    count=int(img[i-1,j-1]==0)+int(img[i,j-1]==0)+int(img[i+1,j-1]==0)+int(img[i-1,j]==0)+int(img[i+1,j]==0)
                else:# 下侧
                    count=int(img[i,j-1]==0)+int(img[i-1,j-1]==0)+int(img[i-1,j]==0)+int(img[i-1,j+1]==0)+int(img[i,j+1]==0)
            else:# C类点
                count=int(img[i+1,j]==0)+int(img[i,j+1]==0)+int(img[i+1,j+1]==0)+int(img[i,j-1]==0)+int(img[i-1,j+1]==0)+int(img[i-1,j-1]==0)+int(img[i-1,j]==0)+int(img[i+1,j-1]==0)# B类点
            if(count<2):# 是孤立点
                flag[i,j]=1# 清除标志
    for i in range(h):
        for j in range(l):
            if(flag[i,j] == 1):
                img[i,j]=255 

    b1 = sum(img.transpose()==0) # 统计行
    b2 = sum(img==0) # 统计列
    roof=0 # 上方边界
    for roof in range(h):
        if b1[roof]>=2:
            break 
    floor=0 # 下方边界
    for floor in range(h-1, -1, -1):
        if b1[floor]>=2:
            break
	
    front=-1*np.ones([4], dtype=int) # 存放四个图片的左侧边界
    hind=-1*np.ones([4], dtype=int) # 存放四个图片的右侧边界
    pic=0 # 截取的图片个数
    
    #print(img[:, 0:15])
    #print(b1)
    #print(b2)
    
    for i in range(l):
        if pic==4:
            break 
        if(b2[i]==0): # 图像有0分割
            if((i>0) and (i-front[pic]<17) and (b2[i-1]!=0)):# 图像宽度小于16且有0分割说明是右侧边界
                hind[pic]=i-1 
                pic=pic+1 
            if((i<l-1) and b2[i+1]!=0):# 说明是左侧边界
                front[pic]=i+1 
        elif(i-front[pic]>16):# 图像宽度大于16，说明没有0分割
            hind[pic]=max(np.argwhere(b2[i-15:i-1]==min(b2[i-15:i-1])))+front[pic]+1 
            pic=pic+1 
            front[pic]=hind[pic-1]+1 
        elif(i==l-1):# 最右侧
            hind[pic]=i 
            pic=pic+1 
    if((pic==4) and (sum(front==-1)==0) and (sum(hind==-1)==0)): # 确定有四张图
        p = 255 * np.ones([15,18,4], dtype=np.uint8)
        for k in range(4):
            for ii in range(roof,floor+1):
                for jj in range(front[k],hind[k]+1):
                    p[ii-roof+1,jj-front[k]+1,k]=img[ii,jj] # 放在白色背景板上
            imgout = revert_image(p[:,:,k], 15, 18)
            imgout.save('./picchar/'+pic_name[k+6]+str(k)+'_'+pic_name[6:10]+'.jpg') # 写入分割后的图片
    else:#截图不符合要求，直接放弃
        print("不符合要求 pic = %d" % (pic))
        print(front)
        print(hind)
        return

def revert_image(img_mat, h, l): # 转换矩阵为图片
    imgout = Image.fromarray(img_mat)
    # imgout.show()
    return imgout

if __name__ == '__main__':
    file_dir = "./pic/"
    file_name=[]
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            pre_operation(file_dir+file)

