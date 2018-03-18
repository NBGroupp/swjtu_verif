# -- coding: utf-8 --   
#=====================================================================
from PIL import Image
import os
root = './'
for i in os.listdir(root):
	if os.path.isfile(os.path.join(root,i)):
		im = Image.open(i)
		out = im.resize((160,60),Image.ANTIALIAS) #改变图片大小为160*60
		out.save(i)
		#print "Resize " + str(i)
