#include <WiFi.h>
#include <PubSubClient.h>
#include "csha1.h"
#include "cbase64.h"

#define BUILTIN_LED 23

const char* ssid = "wifi-ssid";
const char* password = "wifi-password";
const char* mqtt_server = "mqtt-cn-xxxxxxxxxxx.mqtt.aliyuncs.com"; // 使用HIVEMQ 的信息中转服务
const char* TOPIC = "my_mqtt/testMq4Iot";                     // 订阅信息主题
const char* client_id = "GID_my_mqtt@@@esp32_my";                   // 标识当前设备的客户端编号

/**
* MQ4IOT 实例 ID，购买后控制台获取
*/
String instanceId = "mqtt-cn-xxxxxxxxxxx";
/**
 * 账号 accesskey，从账号系统控制台获取
 */
String accessKey = "xxxxxxxxxxxxxxxxxxxxxxxx";
/**
 * 账号 secretKey，从账号系统控制台获取，仅在Signature鉴权模式下需要设置
 */
String secretKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

const String get_password(const char* data_text,const String secretKey);
const String passWord = get_password(client_id,secretKey);

WiFiClient espClient;             // 定义wifiClient实例
PubSubClient client(espClient);   // 定义PubSubClient的实例
long lastMsg = 0;           // 记录上一次发送信息的时长

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);    // 定义板载LED灯为输出方式
  Serial.begin(115200); 
  setup_wifi();             //执行Wifi初始化，下文有具体描述
  client.setServer(mqtt_server, 1883);    //设定MQTT服务器与使用的端口，1883是默认的MQTT端口
  client.setCallback(callback);   //设定回调方式，当ESP8266收到订阅消息时会调用此方法
}

const String get_password(const char* data_text,const String secretKey){
    unsigned char out_bytes[50];
    int secretKeyLength, data_length;
    char base64Char[50]; //注意长度要给够
    int hmac_len = 0;

    secretKeyLength = strlen(secretKey.c_str());
    data_length = strlen(data_text);

    memset(out_bytes, '\0', sizeof(out_bytes));   
    hmac_len = hmac_sha(secretKey.c_str(), secretKeyLength, data_text, data_length, out_bytes, 20);

    memset(base64Char, '\0', sizeof(base64Char));
    cbase64_encode((const char*)out_bytes, hmac_len, base64Char);
    //printf("%s, based64_encoded_len = %d\r\n", base64Char, strlen(base64Char));
    const String ret_data(base64Char);
    return ret_data;
}

void setup_wifi() {

  delay(10);
  // 板子通电后要启动，稍微等待一下让板子点亮
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);   // 打印主题信息
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]); // 打印主题内容
  }
  Serial.println();

  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, HIGH);   // 亮灯
  } else {
    digitalWrite(BUILTIN_LED, LOW);   // 熄灯
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect   (String("Signature|")+accessKey+"|"+instanceId).c_str();  "Signature|LTAI4GBNhdf2xLp8Wb9jVsJP|mqtt-cn-09k1y2eej04"
    if (client.connect(client_id, (String("Signature|")+accessKey+"|"+instanceId).c_str(), passWord.c_str())) {
      Serial.println("connected ！！！！！");
      // 连接成功时订阅主题
      client.subscribe(TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned char result[1024];
  memset(result,'\0',sizeof(result));
  while(Serial.available())//判断串口缓冲器是否有数据装入
  {
    Serial.readBytes(result,1024);
    client.publish("my_mqtt/testMq4Iot",(const char*)result);
  }
  
}
