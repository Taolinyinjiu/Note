# 前言
在配置YOLO V8之前，我们需要了解到一些基础的知识
> 这里有一篇文章是讲NVIDIA显卡驱动、cuda、cudnn概念梳理的，链接是https://yuchaoshui.com/449585a/ ，不过是我写完了才看到的，但是你如果不看我写的我也会很sad的>_< 
1. CUDA
   什么是CUDA呢，很多教程里都会说配置YOLO这样的模型之前先配置一下CUDA，CUDA指的是NVIDIA开发的GPU通用计算平台，但是，但是，只对NVIDIA开发的显卡有支持，当然其他显卡厂商各有各的通用计算平台，比如AMD的RCOM ，但是这里我们不聊AMD，只聊NVIDIA，
   NVIDIA的显卡，被称为N卡，对应的，AMD的显卡被称为A卡，这两年INTEL也出独显，被称为I卡
   当然显卡指的是独显而非集显，集显指的是与CPU封装在一起的集成显卡，通常我们说的显卡都指的是独立显卡，通过PCIE通道与CPU进行通信。
   好的，然后我们提到CUDA，CUDA是GPU通用计算平台，也就是说CUDA屏蔽了硬件底层的差异，使得开发者在调用显卡的时候，可以不去关心用户到底使用的是什么显卡，就像我们使用STM32CUBEIDE，用HAL库在编程的时候，我们不会去关心USART1在初始化过程中做了什么，我们只需要在CUBEMX的图形化界面选中USART1，给定参数就好了。CUDA大抵也是这样的，我们只需要写我们需要GPU平台执行什么任务，至于任务是怎么分配GPU核心的，我们不去关心，我们只要结果。
   这也就导致，CUDA的诞生使得开发者对GPU的编程可以快速地上手，GPU的性能也被极大的运用于各项各项相关工作，比如使用CUDA加速的Opencv，在特征匹配中明显好于使用CPU的版本，
2. CUDNN
   CUDNN，看到CUD的前缀我们就能猜到，它多半是和CUDA一样的东西。实际上CUDNN是CUDA DEEP Neural Network Library，也就是说，CUDNN，是一个CUDA平台中用于为深度学习应用而设计的一个加速库。这当然很好理解了，就像C语言中有专门为数学而涉及的math.h库一样
3. TensorRT
   看到这个TensorRT你可能会觉得这也是NVIDIA家的某个东西，没错，TensorRT是一个用于AI应用的高性能优化编译器和运行时引擎。乍一看好像好复杂的样子，实际上它类似于一个什么东西呢，就比如说，举个不那么恰当的例子，当我们在思考数模题目没有思路的时候，我们会把题目给AI，让AI给出相关的思路呀，代码呀，或者我写了一个很烂的代码，我想让AI给我优化一下。Tensorrt在AI应用部署的场景中就相当于我们提到的AI。
4. YOLO
   好嘟上面提到了那么多没有关系的，最后我们还是要提一下YOLO，当然我知道你这两天也看过了跟YOLO相关的一些资料，但我习惯把东西都写清楚。
   YOLO全称就是You only Look Once ，也就说你只需要看一眼，这个命名体现了YOLO算法的实时性，它指的是，假如这里有许多个视觉方面的检测模型，比如Yolo 比如mobile net，比如别的之类的，当我们传入一帧带有目标的图像的时候，每个模型检测所消耗的时间是不一样的，而在这其中，yolo属于是比较快的那种，因为模型检测消耗的时间，与其网络结构是有关系的，当然这就是其他的话了。
   从Yolo的发展历史来看，我们习惯性把yolo分为yolov8往前和yolov8往后，yolov8往前，以yolov3和yolov5最为出名，v3在低性能开销的嵌入式平台上很吃香，v5相较于v3提升了一些性能，同时优化了一些网络结果，以及一些其他的。
   为什么我们以v8为分界呢，这主要是由于部署方式产生的差异。对于yolov8以后的yolo模型，由于ultralytics出现，ultralytics发布了yolov8，并为yolo引入了全新的存储库，所以后面的yolo系列模型，就可以免去如yolov5等较为麻烦的部署，只需几行代码即可完成快速推理，训练。

## 环境配置
话有点密了，现在我们开始对环境进行搭建
首先我们要思考要不要去搭建N卡的开发环境，也就是CUDA，CUDNN之类的
假设我们做了，也就是说可以提高模型的推理速度，最显著的特点是提高帧率，比如30 fps提到 60fps
既然有时间的话，我们就可以弄一下，
首先，安装cuda ，cudnn，tensorrt，我们用最快的办法，直接安装cuda工具箱，也就是CUDA Toolbox
```bash
# 首先打开终端查看一下N卡和N卡驱动的版本
nvidia-smi
# 这里我就不放截图什么的了
# 学姐电脑是NVIDIA RTX 4060 8GB显存 CUDA版本是12.6(这个不是已经安装的版本，是能够安装的CUDA的最高版本，如果你还么有安装CUDA)
# 学姐居然已经装完了CUDA O>O(这里应该是我看错了OvO)
# 但是终端运行
nvcc -V 
# 没有显示，并且系统里面的环境变量也没有跟cuda有关的部分，我怀疑学姐cuda安装的有问题捏，ok控制面板里面的应用程序中也没有和cuda有关的部分，现在我先重新给学姐安装一遍cuda吧
```

### 安装CUDA
CUDA有很多个版本，很少人对自己要安装CUDA那个版本有清晰的认知，通常都是随大流啦，比如看到csdn有贴纸说安装11.8版本好就安装，或者是根据自己看的教程去安装。实际上呢，我也不知道安装什么版本的好，在我们现在的工作内容里面，对于CUDA实际上是不使用的，我们需要的其实是TensorRT优化以后的模型文件，对于CUDA，CUDNN，TensorRT具体内容和怎么实现的，我们不关心，我们只关心我们需要的，就是优化后的模型文件。同样的，实验室里面并没有几个(划掉)学长能够去做到基于CUDA手写一些模型，我也不行，我的工作重心也不在这里，往年有学长能够自己搓网络结构写识别模型，但他不是很喜欢留知识在实验室。。。无所谓啦都小事儿啦洒洒水啦。(没事儿就喜欢蛐蛐学长嘻嘻)
我给学姐安装的版本是刚刚在终端上看到的，也就是12.6版本，我自己用的也是这个版本。
1. 打开对应网站https://developer.nvidia.com/cuda-toolkit-archive
2. 点击对应版本，这里我们选择CUDA Toolkit 12.6.3 (November 2024), 实际上理论上来说可以用最新的12.9，但是我怕出问题啦，就先上12.6啦
3. 漫长的等待(3min啦洒洒水啦饮个茶先)
4. 下载好以后双击，然后一直下一步，反正主打一个一字不改下一个，因为安装到别的盘也会有点问题索性直接安装到C盘啦，有些东西就是只能够安装在C盘的啦。之所以我觉得学姐cuda没有安装，是因为我在c盘没有看到NVIDIA GPU Computing Toolkit文件夹啦，因为CUDA一般会用这个文件夹啦
5. 安装的过程风扇还挺拽的，嘻嘻显卡马上就要当小黑奴了，哎安装的太慢了，耍会儿抖音吧 
6. 好嘟刷了三四五六七八个视频以后cuda安装完了，我们打开终端检测一下是不是安装完了
   ```bash
   nvcc -V
    PS C:\Users\yinnanzhao> nvcc -V
    nvcc: NVIDIA (R) Cuda compiler driver
    Copyright (c) 2005-2024 NVIDIA Corporation
    Built on Wed_Oct_30_01:18:48_Pacific_Daylight_Time_2024
    Cuda compilation tools, release 12.6, V12.6.85
    Build cuda_12.6.r12.6/compiler.35059454_0
   ```
   好啦，那么cuda确定安装完了
### 安装CUDNN

安装完cuda之后就来安装cudnn啦，但是安装cudnn需要注册NVIDIA的开发者账号，不过我有啦。还是先打开对应链接https://developer.nvidia.com/rdp/cudnn-archive 去下载对应的cudnn版本。这里我们选择Download cuDNN v8.9.7 (December 5th, 2023), for CUDA 12.x
这里我们会发现cudnn实际上是一个压缩包，这也就是为什么我们要先安装cuda，cudnn只是cuda的一个库，所以我们等下把cudnn中一些文件解压出来放在cuda的文件夹里就可以直接用了。
1. 下载对应版本的cudnn(还挺快的刷两个抖音低脂小视频就下好了)
2. 下载完成后解压缩，将解压缩出来的三个文件夹bin,include,lib放到C盘中cuda对应的文件夹里，路径是C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6，直接给权限粘贴进去就行
3. 接着我们检测是否安装有效，打开终端
```bash
PS C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\extras\demo_suite> .\deviceQuery.exe
```
   观察结果是否符合预期

总之我们的cuda和cudnn都安装好了。下一步是安装Tensorrt做模型优化，当然这一步其实并不是必须的，其实所有的都不是必须的，只是我想做而已哈哈哈
在安装TensorRT之前，我们需要保证有一个良好的Python环境，我总感觉学姐的Python环境有点问题的啦。学姐默认的python环境是Python 3.13.3,其实也没什么问题的啦，我觉得这个版本的也能用，而且环境里有的好像都有了，比如opencv-python,比如ultralytics,比如pytorch

### 安装TensorRT
1. 下载对应版本的TensorRT，当然他也是一个压缩包，网站链接是https://developer.nvidia.com/tensorrt/download/10x ，我们选择的版本是TensorRT 10.10 GA for x86_64 Architecture
2. 等待下载完成，解压缩
3. 将压缩包中的include文件夹放到CUDA对应的include文件夹，将lib文件夹中的所有lib文件放到CUDA的lib/x64文件夹中，lib文件夹中所有的dll文件放到CUDA的bin文件夹中。
4. 在python文件夹中，安装对应的py库，这里学姐的python环境是3.13.3，所以我们选择tensorrt-10.10.0.31-cp313-none-win_amd64.whl，安装方式也很简单，打开终端，输入
```bash
# 需要先进入对应的路径下哦
python -m pip insatll tensorrt-10.10.0.31-cp313-none-win_amd64.whl
# 检测是否安装好
# 进入python环境
python 
# 导入tensorrt
import tensorrt
# 如果没有报错就是安装完成了
```

### 安装Ultralytics
按道理来说，Ultralytics你已经安装好了呀，学姐，你的pytorch(一个深度学习框架)是CPU版的，呃呃，我决定，把跟有关Ultralytics的推到重来嘻嘻。

#### 安装Pytorch
安装Ultralytics之前，我们需要先安装好pytroch，在pytorch的官网提供了不同类型的torch的安装方式，如连接https://pytorch.org/get-started/locally/
这里我们选择pip的安装方式，
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```
漫长的等待，再去耍会儿低脂小视频，，，感觉天津好会吃饭啊什么时候能去天津蹭饭哪啊啊啊啊啊啊半夜刷到碳水+碳水我了个豆啊我都要晕碳了

好啦，安装完了，检查一下torch是不是支持cuda了
```python
>>> import torch
>>> print(torch.cuda.is_available())
True
>>> exit()
```
ok了

#### 卸载然后重装Ultralytics

```bash
pip uninstall ultralytics
pip install ultralytics

```
### 安装Jupyter
Jupyter 是一个比较好用的python的IDE，其实也不能说是IDE吧，它更像是一种笔记本，就是怎么说呢，你当初学习Python的时候不知道有没有谁用过它，它就是按代码块儿去执行代码，然后会很直观地看到每一行的结果，我先给你安装了吧
#### 安装
```bash
pip install jupyter
```

#### 使用方式
在终端中直接输入
```bash
jupyter-notebook
```
然后会自动跳转到浏览器，但是jupyter能够打开的文件局限于你在终端中的路径，因此我一般会在代码对应的文件夹中打开，比如我在F盘里面给你放YOLO V8的示例代码，Jupyter也得在F盘对应的路径中打开才能读取到这份示例代码

这里还有一些有趣的知识，比如你可以在jupyter中展示图片或者视频流，但是需要使用matlabplt去转换一下，不过你在自己电脑上，可以直接使用cv2.imshow去实现展示，也不需要就是非要用jupyter去看

### 部署Yolo V8
好了接着来到最动人心弦的部分，是什么呢，就是yolo v8的部署啦，不过呢，这个部署也分为两种，一种是带有可以训练的部署方法，一种是直接推理方法，这里的话，我先给一个特别快的部署方法

#### 基于Ultarlytics的快速部署
在F盘的YoloV8里面我写了简单的示例，你可以用jupyter一步步运行也可以直接python test.py去运行，但是有个问题，就是，，，，学姐你的前置摄像头略显红色，也不是很严重的那种，应该是晚上的光线不太好，导致摄像头泛红。都小事儿啦，但是给哥们儿拍的很潦草，不嘻嘻


#### 关于如何训练自己的模型
如何训练一个属于自己的模型，其实是一个比较常谈的话题了，我们一般要求先把摄像头固定好，比如你要去做光电小车，就把摄像头先固定在车上，然后摄像头连接在电脑上，接着疯狂的拍照拍照拍照，一般拍个几百张就好了，重复的照片不宜太多，一般是物体在摄像头的各个位置，以及各种光照条件下的照片，各种各样的啦，当然其实也不宜太多，兼顾准确性和泛化性就好啦。

当把原始数据拍好了以后，就要自己再挑一挑，把那些模糊的删掉，不完整的删掉，不好看的删掉，总是不符合自己心意的统统删掉，然后保留下来的，接着去框图
框图就是说在图片中框选我们需要识别的模型，这个框吧，基本上就是说框出要识别的物体，然后框尽可能的，恰好覆盖即可。框图工具有很多种，你自己百度啦，选一个比较心仪的就好啦

数据标注完了以后就要划分数据集，一般是三七分啦，70%做为数据集，用来训练，30%用作验证集，用来观察模型的性能。

训练的过程其实也很简单的啦，我找个链接给你吧，因为我懒得写了嘻嘻嘻嘻嘻
https://blog.csdn.net/weixin_42166222/article/details/129391260
如果看不懂再问我啦

#### 关于如何使用TensorRT加速你的模型

这部分，等你训练好模型之后来问我啦，有点懒啦，现在写了也没啥用啦


## 结语

照着自己感兴趣的方向一直走下去吧！美好的明天不需要以牺牲当下的兴趣，警惕陷阱和欺诈嘻嘻嘻嘻
