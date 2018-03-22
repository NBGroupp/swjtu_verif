# 搭建CNN神经网络识别验证码    

训练数据准确率：97.34%    
测试数据准确率：85.00%    

## 使用教程    

### 安装环境   

python 2.7.12/13（包括pip）     
keras 1.2.2（配置好GPU环境）     
pillow 4.0.0     
numpy 1.12.0+mkl     
theano 0.8.2     
h5py 2.6.0    
captcha 0.2.1    
lxml 3.7.2     
scipy 0.18.1     
PyYAML 3.12      

### 提示

前排友情提示，由于训练神经网络需要花费一定的时间，作者已将训练好的网络的参数一并上传。           
因此如只需应用该脚本，可跳过网络的训练步骤，直接跳到步骤3.                

### 详细步骤

1. 那么你可以通过在终端输入：                  

   cd ./SAMPLE            
   python ../tools/GetImage.py 20             
   生成20组160×60的图片(jpg),事实上20组远远不够，要达到训练的要求，至少需要20000组以上              

2. 接着在终端输入：              

   cd..             
   python train_cnn_network.py vegalearning                
   来训练cnn神经网络。（并且训练好后权值矩阵会保存在vega_weights.model里）     

3. 对验证码进行识别输出识别的结果并输出识别的准确率，                

   步骤：           
   1）、将要测试的图片放入SAMPLE_TEST里           
   2）、在终端输入：           
   cd ./SAMPLE_TEST             
   python ../tools/ImgResize.py          
   （python ../tools/GetImage.py 20）或者用验证码生成器生成多组测试图片           
   python ../evaluate.py ../vegalearning_model.json ../vegalearning_weights.model                
   ​              
