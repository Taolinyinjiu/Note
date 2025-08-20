1. 确认nvidia显卡是否就绪
```bash
lspci | grep -i nvidia
```
2. 查看linux版本
```bash
hostnamectl
```
3. 查看gcc版本
```bash
gcc --version
```
4. 选择CUDA Toolkit的安装方式
注意，cuda13并不支持ubuntu20，因此我们选择CUDA Toolkit 12.8.0版本安装，方式为run包
```bash
wget https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux.run

sudo sh cuda_12.8.0_570.86.10_linux.run
```
5. 安装cudnn
进入下载页面，选择合适版本的cudnn下载，然后安装即可
https://developer.nvidia.com/rdp/cudnn-archive
```bash
 sudo dpkg -i cudnn-local-repo-ubuntu2004-8.9.7.29_1.0-1_amd64.deb 
```
