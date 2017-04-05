# -- coding: utf-8 --  
#=====================================================================
from captcha.image import ImageCaptcha
import random
import sys
image=ImageCaptcha()
numbers=1
while numbers <= int(sys.argv[1]):
	ranstr = ''.join(random.sample('ABCDEFGHIJKLMNPQRSTUVWXYZ123456789',4))
	image.write(ranstr,ranstr + '.jpg')
	#print "Write " + ranstr + '.jpg'
	numbers += 1


import ImgResize
	
