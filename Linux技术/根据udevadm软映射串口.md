首先，在 Linux 开发中，串口设备的插拔确实可能导致 COM 号（在 Linux 中通常是 /dev/ttyXXX）的改变，这给应用程序带来了不便。为了解决这个问题，可以通过匹配设备型号的方式来动态地对应 COM 号，确保应用程序始终能够找到正确的串口设备。对于这个问题常见的解决方法为udevadm规则软映射

**udev** 是 Linux 内核的设备管理器，它可以根据设备的属性（如设备型号、序列号等）来创建符号链接，从而实现 COM 号的动态映射。
假设我们当前有个设备的串口号为/dev/ttyACM0

- 首先，我们需要查找设备的相关信息
  - ``` 
  udevadm info --name=/dev/ttyACM0 | grep -E "ID_VENDOR | ID_MODEL | ID_SERIAL"
  ```
  接着会显示一些信息，其中重点关注
    - ID_VENDOR_ID
    - ID_MODEL_ID

- 接着，我们创建一个udevadm规则文件
  - sudo vim /etc/udev/rules.d/my_serial.rules
  - 写入内容 SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", SYMLINK+="my_serial_port"

- 使规则生效
  - sudo udevadm control --reload-rules
  - sudo udevadm trigger