#include <PubSubClient.h>         // MQTT
#include <WiFiManager.h>          // https://github.com/tzapu/WiFiManager WiFi Configuration Magic
#include <DNSServer.h>            // 不烧录代码进行ESP32配网
#include <WebServer.h>            // ESP32服务器
#include <WiFi.h>                 // ESP32连接WiFi
#include <ArduinoJson.h>          // MQTT消息格式
#include "aliyun_mqtt.h"          // 一个快速连接阿里云MQTT的库
#include <Ticker.h>

// 准备连接到的MQTT服务器配置信息 通过一机一密的方式连接MQTT服务器
const char* ProductKey = "hxn5m8ERYBV";
const char* DeviceName = "Device";
const char* DeviceSecret = "85f6c68fba32ae2acee25b140780e7ca";

// 订阅信息
const char* subTopic = "/hxn5m8ERYBV/Device/user/test1";                                                            // 订阅主题(需要修改)
const char* pubTopic = "/hxn5m8ERYBV/Device/user/test2";                                                            // 订阅主题(需要修改)
const char* willTopic = "/hxn5m8ERYBV/Device/user/test3"; 

// 客户端变量
WiFiClient espClient;
PubSubClient client(espClient);

// 定义需要传输到MQTT平台的数据

// 环境温度
float temp = 0;
// 环境湿度
float humi = 0;
// 环境光照
float light = 0;
// 土壤湿度
float soil0_humidity = 0;
float soil1_humidity = 0;
float soil2_humidity = 0;
// 克里斯琴森系数表征土壤滴灌均匀度
float Christ = 0;

 char uart_flag = 0;

Ticker ticker_mqtt; //建立一个Ticker对象用来发送数据包到mqtt服务器

// 定义变量，用于存储 JSON 格式的结果：
// StaticJsonDocument<256> jsonBuffer;
// JsonObject& data = jsonBuffer.to<JsonObject>();

// data["TEMPERATURE"] = String(27.6,1);//℃
// data["HUMIDITY"] = String(27.6,1);//℃
// data["LIGHT_INTENSITY"] = String(27.6,1);//℃
// data["SMOKE"] = String(27.6,1);//℃

void setup() {
  // 初始化同Typec连接的串口,参数是波特率
  Serial.begin(115200);
  // 建立 WiFiManager 对象
  WiFiManager wifiManager;  
  // 自动连接WiFi，下面这行中的参数是ESP32在未配置网络时，会启动的热点Wifi名称，链接这个网络可以对ESP32进行配网
  wifiManager.autoConnect("AutoConnectAP");

  // 当需要清除掉wifiManager中存储的配置时,取消下面两行的注释
  // wifiManager.resetSettings();
  // Serial.println("ESP8266 WiFi Settings Cleared");

  // 连接阿里云MQTT服务端，参数为阿里云MQTT服务器的地址和端口
    if (connectAliyunMQTT(client, ProductKey, DeviceName, DeviceSecret))
    {
        Serial.println("MQTT服务器连接成功!");
    };
  ticker_mqtt.attach(1,pubMQTTmsg);
  // 修改串口引脚
  int RXPIN = 9;
  int TXPIN = 10;
  //初始化串口1，波特率115200，SERIAL_8N1=8数据位无校验位1停止位 RX引脚为9 TX引脚为10
  Serial1.begin(115200, SERIAL_8N1, RXPIN, TXPIN);
  // 设置串口1的中断回调函数
  Serial1.onReceive(onReceiveFunction);
  // 初始化Serial0,用于TypeC进行调试
  Serial.printf("Hello World\r\n");
  // WiFi连接成功后将通过串口监视器输出连接成功信息 
  Serial.println(""); 
  Serial.print("ESP32 Connected to ");
  Serial.println(WiFi.SSID());              // WiFi名称
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // IP

  // char payload[256];
  // data.printTo(payload, sizeof(payload));
  // String strPayload = String(payload);
  // client.publish(topic_publish, public_messages().c_str());
}

void onReceiveFunction(void)
{
  // 处理接收到的数据
  while (Serial1.available())
  {
    char receivedData = Serial1.read(); // 读取接收缓冲区中的数据
    Data_Analyse(receivedData); 
  } 

}

void Data_Analyse(uint8_t rec)
{
	static uint8_t ch;  // 临时变量，存储传入参数
	// 共用体,解析串口传输数据
  static union
	{
		uint8_t date[24];
		float ActVal[6];
	} uart_data;
	// count用作计数器，记录传入长度
  static uint8_t count = 0;
	static uint8_t i = 0;

	ch = rec;

	switch (count)
	{
	case 0:
		if (ch == 0x0d) // 帧头0x0D
			count++;
		else
			count = 0;
		break;
	case 1:
		if (ch == 0x0a) // 帧头0x0A
		{
			i = 0;
			count++;
		}
		else if (ch == 0x0d) // 重复检测到0x0D
			;
		else
			count = 0;  // 没有检测到目标帧则回到最开始
		break;
	case 2:
    // 开始记录数据
		uart_data.date[i] = ch;
		i++;
		if (i >= 24)
		{
			i = 0;
			count++;
		}
		break;
	case 3:
		if (ch == 0x0a)
			count++;
		else
			count = 0;
		break;
	case 4:
		if (ch == 0x0d)
		{
			temp = uart_data.ActVal[0];
			humi = uart_data.ActVal[1];
			light = uart_data.ActVal[2];
			soil0_humidity = uart_data.ActVal[3];
			soil1_humidity = uart_data.ActVal[4];
			soil2_humidity = uart_data.ActVal[5];
      // Serial.printf("temp = %f \r\n",temp);
      // Serial.printf("humi = %f \r\n",humi);
      // Serial.printf("light = %f \r\n",light);
      // Serial.printf("soil0_humidity = %f \r\n",soil0_humidity);
      // Serial.printf("soil1_humidity = %f \r\n",soil1_humidity);
      // Serial.printf("soil2_humidity = %f \r\n",soil2_humidity);
		}
    uart_flag = 1;
		count = 0;
		break;
	default:
		count = 0;
		break;
	}
}

// 发布信息
void pubMQTTmsg(){
  static int value;   // 客户端发布信息用数字
 
  // 建立发布主题。主题名称以Taichi-Maker-为前缀，后面添加设备的MAC地址。
  // 这么做是为确保不同用户进行MQTT信息发布时，ESP8266客户端名称各不相同，
  String topicString = "Taichi-Maker-Pub-" + WiFi.macAddress();
  char publishTopic[topicString.length() + 1];  
  strcpy(publishTopic, topicString.c_str());
 
  // 建立发布信息。信息内容以Hello World为起始，后面添加发布次数。
  String messageString = "Hello World " + String(value++); 
  char publishMsg[messageString.length() + 1];   
  strcpy(publishMsg, messageString.c_str());
  
  // 实现ESP8266向主题发布信息
  if(client.publish(subTopic, publishMsg)){
    Serial.println("Publish Topic:");Serial.println(publishTopic);
    Serial.println("Publish message:");Serial.println(publishMsg);    
  } else {
    Serial.println("Message Publish Failed."); 
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(uart_flag == 1){
    Serial.printf("temp = %f \r\n",temp);
    Serial.printf("humi = %f \r\n",humi);
    Serial.printf("light = %f \r\n",light);
    Serial.printf("soil0_humidity = %f \r\n",soil0_humidity);
    Serial.printf("soil1_humidity = %f \r\n",soil1_humidity);
    Serial.printf("soil2_humidity = %f \r\n",soil2_humidity);
    uart_flag = 0;
  }
  if (client.connected()) { // 如果开发板成功连接服务器    
    client.loop();          // 保持客户端心跳
  }
}
