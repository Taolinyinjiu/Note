#### 添加MQTT库
在build.gradle文件中，修改dependencies部分，添加如下
``` java
dependencies {
    // ... 你的其他依赖 ...

    // Eclipse Paho MQTT 客户端
    implementation 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.5'
    implementation 'org.eclipse.paho:org.eclipse.paho.android.service:1.1.1'
}
```
添加依赖后，点击 Android Studio 顶部的 "Sync Now" 按钮，以同步 Gradle 更改。

#### 更改权限
在 AndroidManifest.xml 文件中添加以下权限：
```xml

<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    ...>

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />

    <application
        ...>
        <!-- 添加 MqttService -->
        <service android:name="org.eclipse.paho.android.service.MqttService" />
        ...
    </application>
</manifest>
```

#### 创建MQTT客户端并连接到Broker
```java
package com.example.sceactivity;

import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.example.sceactivity.databinding.ActivityMainBinding;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;
    private MqttAndroidClient mqttClient;
    private final String serverUri = "tcp://your_mqtt_broker_address:1883"; // 替换为你的 MQTT Broker 地址
    private final String clientId = "your_client_id";  // 替换为你想要的客户端 ID
    private final String subscriptionTopic = "your/subscription/topic"; // 替换为你需要订阅的主题

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // 初始化 MQTT 客户端并连接
        connectToMqttBroker();
    }

    private void connectToMqttBroker() {
        mqttClient = new MqttAndroidClient(this, serverUri, clientId);

        try {
            IMqttToken token = mqttClient.connect(getMqttConnectOptions());
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Log.d("MQTT", "Connected to broker");
                    // 连接成功后订阅主题
                    subscribeToTopic(subscriptionTopic);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.e("MQTT", "Failed to connect to broker: " + exception.getMessage());
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
        // 设置消息回调
        mqttClient.setCallback(getMqttCallback());
    }

    // 设置MQTT配置
    private MqttConnectOptions getMqttConnectOptions() {
        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true); // 设置自动重连
        options.setCleanSession(true); // 清理会话
        //options.setUserName("your_username"); // 如果需要用户名密码验证，请取消注释并填写相应信息
        //options.setPassword("your_password".toCharArray()); // 如果需要用户名密码验证，请取消注释并填写相应信息
        return options;
    }

    // 设置消息回调
    private MqttCallback getMqttCallback() {
        return new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {
                Log.e("MQTT", "Connection lost: " + cause.getMessage());
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                String payload = new String(message.getPayload());
                Log.d("MQTT", "Message arrived on topic " + topic + ": " + payload);
                // 处理接收到的消息
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
                Log.d("MQTT", "Message delivered");
            }
        };
    }

    //订阅主题
    private void subscribeToTopic(String topic) {
        try {
            mqttClient.subscribe(topic, 0);
        } catch (MqttException e) {
            Log.e("MQTT", "Error subscribing to topic: " + e.getMessage());
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        try {
            mqttClient.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
```