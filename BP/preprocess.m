%%Ԥ����
clc,clear;
dirOutput = dir(fullfile('pic*.jpg'));   % ��ȡ·��  
fileNames = {dirOutput.name}';% ��÷��������ļ���
for fn=1:length(fileNames)%1000
I=imread(fileNames{fn}); %��ȡͼ���ļ�
%figure(1);
%imshow(I);
%title('ԭͼ');
I=rgb2gray(I);%ͼ��ҶȻ�����
%figure(2);
%imshow(I);
%title('�ҶȻ�');
[h,l]=size(I);
%��ֵ��
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
end%ȥ���ڿ�
%figure(4);
%imshow(I);
%title('��ֵ�������');
flag=zeros(h,l);
%ȥ��
	for i=1:h
		for j=1:l
			if(I(i,j)==255)%���Ǻڵ������
				continue;
			end
			if(((i==1)&&(j==1))||((i==1)&&(j==l))||((i==h)&&(j==1))||((i==h)&&(j==l)))%A���
				if((i==1)&&(j==1))%���Ͻ�
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0);
				elseif((i==h)&&(j==1))%���½�
				count=(I(i,j+1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0);
				elseif((i==1)&&(j==l))%���Ͻ�
				count=(I(i,j-1)==0)+(I(i+1,j)==0)+(I(i+1,j-1)==0);
				else%���½�
				count=(I(i,j-1)==0)+(I(i-1,j)==0)+(I(i-1,j-1)==0);
				end
			elseif((i==1)||(j==1)||(i==h)||(j==l))%B���
				if(j==1)%���
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0);
				elseif(i==1)%�ϲ�
				count=(I(i+1,j)==0)+(I(i+1,j+1)==0)+(I(i+1,j-1)==0)+(I(i,j-1)==0)+(I(i,j+1)==0);
				elseif(j==l)%�Ҳ�
				count=(I(i-1,j-1)==0)+(I(i,j-1)==0)+(I(i+1,j-1)==0)+(I(i-1,j)==0)+(I(i+1,j)==0);
				else%�²�
				count=(I(i,j-1)==0)+(I(i-1,j-1)==0)+(I(i-1,j)==0)+(I(i-1,j+1)==0)+(I(i,j+1)==0);
				end
			else%C���
				count=(I(i+1,j)==0)+(I(i,j+1)==0)+(I(i+1,j+1)==0)+(I(i,j-1)==0)+(I(i-1,j+1)==0)+(I(i-1,j-1)==0)+(I(i-1,j)==0)+(I(i+1,j-1)==0);%B���
			end
			if(count<2)%�ǹ�����
			flag(i,j)=1;%�����־
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
	%title('ȥ��');
	b1=sum(I'==0);%ͳ����
	b2=sum(I==0);%ͳ����
	roof=0;%�Ϸ��߽�
	for roof=1:h
		if b1(roof)>=2
		break;
		end
	end
	floor=0;%�·��߽�
	for floor=h:-1:1
		if b1(floor)>=2
		break;
		end
	end
	front=zeros(1,4);%����ĸ�ͼƬ�����߽�
	hind=zeros(1,4);%����ĸ�ͼƬ���Ҳ�߽�
	pic=1;%��ȡ��ͼƬ����
	for i=1:l
		if pic==5
			break;
		end
		if((b2(i)==0))%ͼ����0�ָ�
			if((i>1)&&(i-front(pic)<17)&&(b2(i-1)~=0))%ͼ����С��16����0�ָ�˵�����Ҳ�߽�
				hind(pic)=i-1;
				pic=pic+1;
			end
			if((i<l)&&b2(i+1)~=0)%˵�������߽�
				front(pic)=i+1;
			end
		elseif(i-front(pic)>16)%ͼ���ȴ���16��˵��û��0�ָ�
			hind(pic)=max(find(b2(i-15:i-1)==min(b2(i-15:i-1))))+front(pic)+1;
			pic=pic+1;
			front(pic)=hind(pic-1)+1;
		elseif(i==l)%���Ҳ�
			hind(pic)=i;
			pic=pic+1;
		end
	end
	if((pic==5)&&(sum(front==0)==0)&&(sum(hind==0)==0))%ȷ��������ͼ
		p=255*ones(15,18,4);
		for k=1:4
			for ii=roof:floor
				for jj=front(k):hind(k)
				p(ii-roof+1,jj-front(k)+1,k)=I(ii,jj);%���ڰ�ɫ��������
				end
			end
		imwrite(p(:,:,k),[int2str(k),'-',fileNames{fn}],'jpg');
		end
	else
		continue;
	end
end
%D:\deeplearning\1\dean-captcha,
