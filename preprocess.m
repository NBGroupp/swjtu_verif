%%预处理
clc,clear;
dirOutput = dir(fullfile('pic*.jpg'));   % 提取路径  
fileNames = {dirOutput.name}';% 获得符合条件文件名
for fn=1:length(fileNames)%1000
I=imread(fileNames{fn}); %读取图像文件
%figure(1);
%imshow(I);
%title('原图');
I=rgb2gray(I);%图像灰度化处理
%figure(2);
%imshow(I);
%title('灰度化');
[h,l]=size(I);
%二值化
for i=1:h
	for j=1:l
		if I(i,j)>110
			I(i,j)=255;
		else
			I(i,j)=0;
		end
	end
end
i=1;
for j=1:l
	I(i,j)=255;
end
j=1;
for i=1:h
	I(i,j)=255;
end%去掉黑框
%figure(4);
%imshow(I);
%title('二值化处理后');
flag=zeros(h,l);
%去噪
	for i=1:h
		for j=1:l
			if(I(i,j)==255)%不是黑点则忽略
				continue;
			end
			if(((i==1)&&(j==1))||((i==1)&&(j==l))||((i==h)&&(j==1))||((i==h)&&(j==l)))%A类点
				if((i==1)&&(j==1))%左上角
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0);
				elseif((i==h)&&(j==1))%左下角
				count=(I(i,j+1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0);
				elseif((i==1)&&(j==l))%右上角
				count=(I(i,j-1)==0)+(I(i+1,j)==0)+(I(i+1,j-1)==0);
				else%右下角
				count=(I(i,j-1)==0)+(I(i-1,j)==0)+(I(i-1,j-1)==0);
				end
			elseif((i==1)||(j==1)||(i==h)||(j==l))%B类点
				if(j==1)%左侧
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0);
				elseif(i==1)%上侧
				count=(I(i+1,j)==0)+(I(i+1,j+1)==0)+(I(i+1,j-1)==0)+(I(i,j-1)==0)+(I(i,j+1)==0);
				elseif(j==l)%右侧
				count=(I(i-1,j-1)==0)+(I(i,j-1)==0)+(I(i+1,j-1)==0)+(I(i-1,j)==0)+(I(i+1,j)==0);
				else%下侧
				count=(I(i,j-1)==0)+(I(i-1,j-1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0)+(I(i,j+1)==0);
				end
			else%C类点
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0)+(I(i,j-1)==0)+(I(i-1,j+1)==0)+(I(i-1,j-1)==0)+(I(i-1,j)==0)+(I(i+1,j-1)==0);%B类点
			end
			if(count<2)%是孤立点
			flag(i,j)=1;%清除标志
				end
		end
	end
	for i=1:h
		for j=1:l
		if(flag(i,j))
			I(i,j)=255;
		end
		end
	end
	%figure(5);
	%imshow(I);
	%title('去噪');
	b1=sum(I'==0);%统计行
	b2=sum(I==0);%统计列
	roof=0;%上方边界
	for roof=1:h
		if b1(roof)>=2
		break;
		end
	end
	floor=0;%下方边界
	for floor=h:-1:1
		if b1(floor)>=2
		break;
		end
	end
	front=zeros(1,4);%存放四个图片的左侧边界
	hind=zeros(1,4);%存放四个图片的右侧边界
	pic=1;%截取的图片个数
	for i=1:l
		if pic==5
			break;
		end
		if((b2(i)==0))%图像有0分割
			if((i>1)&&(i-front(pic)<17)&&(b2(i-1)~=0))%图像宽度小于16且有0分割说明是右侧边界
				hind(pic)=i-1;
				pic=pic+1;
			end
			if((i<l)&&b2(i+1)~=0)%说明是左侧边界
				front(pic)=i+1;
			end
		elseif(i-front(pic)>16)%图像宽度大于16，说明没有0分割
			hind(pic)=max(find(b2(i-15:i-1)==min(b2(i-15:i-1))))+front(pic)+1;
			pic=pic+1;
			front(pic)=hind(pic-1)+1;
		elseif(i==l)%最右侧
			hind(pic)=i;
			pic=pic+1;
		end
	end
	if((pic==5)&&(sum(front==0)==0)&&(sum(hind==0)==0))%确定有四张图
		p=255*ones(15,18,4);
		for k=1:4
			for ii=roof:floor
				for jj=front(k):hind(k)
				p(ii-roof+1,jj-front(k)+1,k)=I(ii,jj);%放在白色背景板上
				end
			end
		imwrite(p(:,:,k),[int2str(k),'-',fileNames{fn}],'jpg');
		end
	else
		continue;
	end
end
%D:\deeplearning\1\dean-captcha,