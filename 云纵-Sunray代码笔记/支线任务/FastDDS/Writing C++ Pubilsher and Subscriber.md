#　Writing a simple C++ publisher and subscriber application

> 本节记录如何创建一个FastDDS应用程序，同时有发布者和订阅者，逐步使用C++ api 也可以通过FastDDS-Gen工具

## Background
DDS 是一种以**数据为中心（Data-Centric）**的通信中间件，它实现了 DCPS（Data Centric Publish-Subscribe，以数据为中心的发布-订阅） 模型。该模型基于以下元素的开发：
- 发布者（Publisher）：产生数据的元素；
- 订阅者（Subscriber）：消耗数据的元素。
这些实体通过 主题（Topic） 进行通信，主题是连接这两个 DDS 实体的纽带。发布者在某个主题下生成信息，而订阅者通过订阅同一个主题来接收信息。

## Prerequisites
首先，你需要按照《安装手册》（Installation Manual）中概述的步骤，完成 eProsima Fast DDS 及其所有依赖项的安装。

此外，你还需要完成《安装手册》中关于 eProsima Fast DDS-Gen 工具安装的步骤。

另外请注意，本教程中提供的所有命令都是针对 Linux 环境编写的。

## Create the application workspace
在项目结束时，应用程序的工作区将具有以下结构。其中，build/DDSHelloWorldPublisher 和 build/DDSHelloWorldSubscriber 文件分别是**发布者（Publisher）应用程序和订阅者（Subscriber）**应用程序

```bash
.
└── workspace_DDSHelloWorld
    ├── build
    │   ├── CMakeCache.txt
    │   ├── CMakeFiles
    │   ├── cmake_install.cmake
    │   ├── DDSHelloWorldPublisher
    │   ├── DDSHelloWorldSubscriber
    │   └── Makefile
    ├── CMakeLists.txt
    └── src
        ├── HelloWorld.cxx
        ├── HelloWorld.h
        ├── HelloWorld.idl
        ├── HelloWorldCdrAux.hpp
        ├── HelloWorldCdrAux.ipp
        ├── HelloWorldPublisher.cpp
        ├── HelloWorldPubSubTypes.cxx
        ├── HelloWorldPubSubTypes.h
        └── HelloWorldSubscriber.cpp
```
那么让我们迈出第一步吧
```bash
mkdir workspace_DDSHelloWorld && cd workspace_DDSHelloWorld
mkdir src build
```

## Import linked libraries and its dependencies
DDS 应用程序需要 Fast DDS 和 Fast CDR 库。根据所采用的安装步骤，让这些库在我们的 DDS 应用程序中可用的过程会略有不同。

### Installation from binaries and manual installation
如果我们是按照二进制包安装或手动安装（指执行了 install 步骤）的，那么这些库在工作区中已经是可访问的了。在 Linux 系统上，Fast DDS 和 Fast CDR 的头文件分别位于 /usr/include/fastrtps/ 和 /usr/include/fastcdr/ 目录中。而这两者的已编译库文件则可以在 /usr/lib/ 目录中找到。

### Colcon installation
通过 Colcon 安装后，有多种方式可以导入这些库。如果只需要在当前会话（即当前的终端窗口）中使用这些库，请运行以下命令：
```bash
source <path/to/Fast-DDS/workspace>/install/setup.bash
```
通过将 Fast DDS 的安装目录添加到当前用户的 Shell 配置文件中的 $PATH 变量里，可以使这些库在任何会话中都可访问。请通过运行以下命令来完成：
```bash
echo 'source <path/to/Fast-DDS/workspace>/install/setup.bash' >> ~/.bashrc
```

## Configure the CMake project
我们将使用 CMake 工具来管理项目的构建过程。请使用你偏好的文本编辑器，创建一个名为 CMakeLists.txt 的新文件，并复制粘贴以下代码段。将该文件保存在工作区的根目录下。如果你按照之前的步骤操作，该根目录应该是 workspace_DDSHelloWorld
```bash
cmake_minimum_required(VERSION 3.20)

project(DDSHelloWorld)

# Find requirements
if(NOT fastcdr_FOUND)
    find_package(fastcdr 2 REQUIRED)
endif()

if(NOT fastrtps_FOUND)
    find_package(fastrtps 2.12 REQUIRED)
endif()

# Set C++11
include(CheckCXXCompilerFlag)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_COMPILER_IS_CLANG OR
        CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    check_cxx_compiler_flag(-std=c++11 SUPPORTS_CXX11)
    if(SUPPORTS_CXX11)
        add_compile_options(-std=c++11)
    else()
        message(FATAL_ERROR "Compiler doesn't support C++11")
    endif()
endif()

message(STATUS "Configuring HelloWorld publisher/subscriber example...")
file(GLOB DDS_HELLOWORLD_SOURCES_CXX "src/*.cxx")
```

## Build the topic data type
eProsima Fast DDS-Gen 是一个 Java 应用程序，它能够根据**接口定义语言（IDL）**文件中定义的数据类型生成源代码。该程序主要有两个功能：

- 为你的自定义主题（Topic）生成 C++ 定义。
- 生成一个使用你主题数据的功能性示例程序。

在本教程中，我们将采用前者（即只生成 C++ 定义）。若要查看后者的应用示例，可以参考另一个示例（详见“简介”部分）。在本项目中，我们将使用 Fast DDS-Gen 来定义发布者发送和订阅者接收的消息数据类型。

请在工作区目录中执行以下命令：
```bash
cd src && touch HelloWorld.idl
```
这会在 src 目录中创建 HelloWorld.idl 文件。
在文本编辑器中打开文件，复制粘贴以下代码片段。
```bash
struct HelloWorld
{
    unsigned long index;
    string message;
};
```
通过这样做，我们定义了 HelloWorld 数据类型，它有两个元素：类型为 uint32_t 的索引以及类型为 std：：string 的消息。剩下的就是生成实现该数据类型的 C++11 的源代码。为此，从src目录中执行以下命令。
```bash
<path/to/Fast DDS-Gen>/scripts/fastddsgen HelloWorld.idl
```
这会生成以下文件
- HelloWorld.cxx: HelloWorld type definition.
- HelloWorld.h: Header file for HelloWorld.cxx.
- HelloWorldPubSubTypes.cxx: Interface used by Fast DDS to support HelloWorld type.
- HelloWorldPubSubTypes.h: Header file for HelloWorldPubSubTypes.cxx.
- HelloWorldCdrAux.ipp: Serialization and Deserialization code for the HelloWorld type.
- HelloWorldCdrAux.hpp: Header file for HelloWorldCdrAux.ipp.

## Write the Fast DDS publisher
在工作区目录中，执行下面的命令下载HelloWorldPublisher.cpp
```bash
wget -O HelloWorldPublisher.cpp \
    https://raw.githubusercontent.com/eProsima/Fast-DDS-Docs/2.x/code/Examples/C++/DDSHelloWorld/src/HelloWorldPublisher.cpp
```

这是发布者应用程序的 C++ 源代码。它将以HelloWorldTopic为主题发送10次消息。
```cpp


```