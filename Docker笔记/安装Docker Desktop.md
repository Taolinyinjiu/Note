# Install Docker Desktop on Linux

> Important
> 
> Docker Desktop on Linux runs a Virtual Machine (VM) which creates and uses a custom docker context, desktop-linux, on startup.
> 
> This means images and containers deployed on the Linux Docker Engine (before installation) are not available in Docker Desktop for Linux.
>
> 在Windows或者MacOS上Docker Desktop可以利用操作系统级别的虚拟化技术，但是在Linux上，Docker为了提供跨平台的一致性支持(如为Ubuntu，Arch，Debain，Hat提供相同的支持效果)，会在后台启动一个轻量级的虚拟机
> 因此，Docker Desktop在linux上实际上是运行在一个虚拟机内部，因此他会创建一个独立的Docker环境，这个环境被称为docker context，并且命名为desktop-linux
> 同时，这个虚拟机内部的docekr环境同宿主机实际上是隔离的
> 但是，相应的，docker desktop相较于docker engine带来了更多的性能开销和IO消耗

## General system requirements

安装Docker Desktop 有一些前置条件：
- 64位核心以及 CPU 对虚拟化的支持。
- KVM虚拟化支持
- QEMU至少为5.2版本
- systemd初始化系统
- 主流桌面环境，比如GNOME, KDE, MATE
- 内存至少为4GB

## KVM virtualization support
