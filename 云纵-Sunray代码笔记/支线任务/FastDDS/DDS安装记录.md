# Linux Install Fast DDS From Binaries
> Ubuntu20基于预编译的二进制软件包安装FastDDS Version为2.14.4

## Install 

首先在官网页面下载压缩包，需要填写一份问卷如，然后根据平台进行下载，链接为https://eprosima.com/index.php/downloads-all，值得注意的是需要魔法上网，不然会有点慢。下载完成后进行解压，有桌面的情况直接右键解压即可，没有可视化桌面的情况下通过tar命令行进行解压即可，随后执行脚本安装FastDDS的依赖。
```bahs
cd <extraction_directory>
sudo ./install.sh
```
注意，由于Ubuntu20默认的软件仓库中并不包含有`python3-xmlschema`，因此直接运行该脚本会报错卡在apt安装`python3-xmlschema`，解决方式为使用`pip3`安装`python3-xmlschema`，然后修改`install.sh`中136行的内容
```bash
sudo apt update
# 如果没有pip3的话需要先安装
sudo apt install python3-pip
pip3 install xmlschema
```
注意，由于Ubuntu20默认的cmake版本为3.16，低于DDS要求的3.20，这里需要进行升级，但是考虑到可能会对ros noetic产生影响，这里将cmake下载到特定的目录，只在编译FastDDS时调用它

```bash
mkdir -p ~/cmake_tools
cd ~/cmake_tools
# 右键链接跳转下载的更快
wget https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-linux-x86_64.tar.gz
tar -zxvf cmake-3.28.1-linux-x86_64.tar.gz
# 确认cmake版本
~/cmake_tools/cmake-3.28.1-linux-x86_64/bin/cmake --version
```

随后修改`install.sh`，在119行处做如下修改

```bash
parse_options ${@}
# 这里需要将路径写为绝对路径，因为使用sudo执行时`~`会指向root目录下而非user目录下
export PATH=/home/taolin/cmake_tools/cmake-3.28.1-linux-x86_64/bin:$PATH
echo "Current CMake version: $(cmake --version | head -n 1)"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
```
编译时间大概在20分钟左右...但应该不会有报错，最后FastDDS相关的东西都会存放在/usr/local中，后续和ros结合的时候需要额外做一些工作，不过都是后话了

### Contents

在`src`文件夹下存放由如下软件包:
- `foonathan_memory_vendor`:一个兼容STL的C++内存分配器
- `fastcdr`:一个C++的数据序列化库，基于CDR标准(OMG CDR标准10.2.1.2)
- `fastrtps`:eProsima Fast DDS 库的核心库。
- `fastddsgen`:一个使用 IDL 文件中定义的数据类型生成源代码的 Java 应用程序。

