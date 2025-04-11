# 阿里云MQTT服务器配置记录

## Arduino环境下ESP32连接MQTT
### 1.安装PubSubClient库
首先启动Arduino IDE 并在左侧工具栏中添加PubSubClient库,具体操作可以看链接https://www.jianshu.com/p/7f54b92d7a7b
在默认情况下，Arduino会将C盘对应的文档文件夹作为项目的文件夹,库也是安装到这个文件夹下，我们需要先进入到这个文件夹中，找到PubSubClient.h，将其中的MQTT_MAX_PACKET_SIZE的值改成1024，MQTT_KEEPALIVE的值改成60，如果不这样做的话，无法连接上阿里云的MQTT服务器

### 2.获得MQTT的客户端连接的签名鉴权

