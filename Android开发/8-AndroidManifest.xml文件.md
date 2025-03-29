### 什么是AndroidManifest.xml文件

> Manifest的意思是清单

AndroidManifest.xml 文件是每个 Android 应用程序的核心配置文件（有且只有一个），它为 Android 操作系统提供了应用程序的基本信息，以便系统能够正确运行该应用程序。以下是 AndroidManifest.xml 文件的主要作用：
- 声明应用程序(APP)的所有组件
  - AndroidManifest.xml 文件声明了应用程序的所有组件，包括 Activity（活动）、Service（服务）、BroadcastReceiver（广播接收器）和 ContentProvider（内容提供器）。他们也被称为Android的四大基本组件
  - 这些组件是应用程序的基本构建块，它们定义了应用程序的用户界面、后台任务、系统事件响应以及数据共享方式。
  - 通过在 AndroidManifest.xml 中声明这些组件，系统能够识别并启动它们。
- 声明应用程序的权限
  - Android 应用程序需要特定的权限才能访问系统资源或执行某些操作，例如访问网络、读取联系人或使用摄像头。
  - AndroidManifest.xml 文件用于声明应用程序所需的这些权限。
  - 在安装应用程序时，系统会提示用户授予这些权限。
- 声明应用程序的硬件和软件要求：
  - AndroidManifest.xml 文件可以声明应用程序所需的硬件和软件功能，例如特定的屏幕尺寸、键盘类型或摄像头功能。
- 声明应用程序的元数据：
  - AndroidManifest.xml 文件还可以包含应用程序的元数据，例如应用程序的图标、名称、主题和版本信息。
  -  这些元数据用于向用户和系统提供有关应用程序的信息。
- 声明应用程序的入口点：
  - AndroidManifest.xml 文件定义了应用程序的入口点，即当用户启动应用程序时，系统首先启动的 Activity。

在一个简单的Android APP中，通常初始的AndroidManifest.xml如下所示：
``` xml
<!-- 声明XML的文档版本1.0和编码格式utf-8 -->
<?xml version="1.0" encoding="utf-8"?>
<!-- <manifest> 是根元素，定义了 Android 应用程序的包。 -->
<!-- xmlns:android="http://schemas.android.com/apk/res/android" 声明了 Android 命名空间，允许使用 Android 属性。 -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
<!-- <application> 元素包含应用程序的全局属性  -->
    <application
        <!-- 允许用户通过 Google 的备份服务备份应用程序数据。 -->
        android:allowBackup="true"
        <!-- 指定了数据提取的规则，这些规则在xml/data_extraction_rules.xml文件中定义。 -->
        android:dataExtractionRules="@xml/data_extraction_rules"
        <!-- 指定了完整备份的规则，这些规则在xml/backup_rules.xml文件中定义。 -->
        android:fullBackupContent="@xml/backup_rules"
        <!-- 设置应用程序的图标。@mipmap/ic_launcher 指向 res/mipmap 目录中的 ic_launcher.png -->
        android:icon="@mipmap/ic_launcher"
        <!-- 设置应用程序的名称。@string/app_name 指向 res/values/strings.xml 中定义的字符串资源 -->
        android:label="@string/app_name"
        <!-- 设置圆形图标，用于支持圆形图标的设备 -->
        android:roundIcon="@mipmap/ic_launcher_round"
        <!-- 支持从右到左 (RTL) 的布局，这对于某些语言（如阿拉伯语和希伯来语）很重要。 -->
        android:supportsRtl="true"
        <!-- 设置应用程序的主题,@style/Theme.MyApplication 指向 res/values/themes.xml 中定义的主题 -->
        android:theme="@style/Theme.MyApplication"
        <!-- 指定应用程序的目标 API 级别为 31（Android 12 -->
        tools:targetApi="31">
        <!-- <activity> 元素声明了一个 Activity 组件，即 MainActivity -->
        <activity
            <!-- 指定 Activity 的类名。.MainActivity 表示 MainActivity 类位于应用程序的包中 -->
            android:name=".MainActivity"
            <!-- 表明该activity可以被其他应用启动 -->
            android:exported="true">
            <!-- <intent-filter> 元素定义了 Activity 可以响应的 Intent -->
            <intent-filter>
                <!-- 指定 Activity 是应用程序的入口点。 -->
                <action android:name="android.intent.action.MAIN" />
                <!-- 指定 Activity 应该出现在应用程序启动器中。 -->
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

上面有那些值得注意的地方呢？
1. 当书写activity时，所有需要被显示的activity都需要在AndroidManifest中进行声明
2. 可以同时为多个activity配置为程序的入口点，但是同一个进程中只会有一个activity可以作为入口点，换句话说，会同时安装多个activity的入口点，但是他们本质上是同一个app，当进入一个app的界面后，其他的都只会进入那个界面，除非该app的进程被kill了