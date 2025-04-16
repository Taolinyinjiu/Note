# ThingsCloudWiFiManager.h

## 概述
这个头文件`ThingsCloudWiFiManager.h`定义了一个名为 `ThingsCloudWiFiManager` 的 C++ 类，其目的是为了简化 ESP8266 和 ESP32 设备连接到 WiFi 网络，并提供一个配置门户（Captive Portal）用于在设备无法连接到已保存的 WiFi 网络时，通过 Web 界面进行 WiFi 配置。它还包含了与 ThingsCloud MQTT 客户端集成的功能。

## 代码具体分析

### 头文件保护
```cpp
#ifndef ThingsCloudWiFiManager_h
#define ThingsCloudWiFiManager_h
// ... 代码 ...
#endif
```
这部分是标准的头文件保护，确保`ThingsCloudWiFiManager.h`文件在同一个编译单元中只被包含一次，仿制重复定义错误

### 依赖包含
```cpp
#include <ThingsCloudMQTT.h>
#include <vector>

#if defined(ESP8266) || defined(ESP32)
  #ifdef ESP8266
    #include <core_version.h>
  #endif
  // ... 平台相关的库 ...
#endif

#include <DNSServer.h>
#include <memory>
```
- #include <ThingsCloudMQTT.h>: 表明此类与 ThingsCloud 的 MQTT 功能紧密相关，需要使用 ThingsCloudMQTT 类进行 MQTT 通信
- #include <vector>: 引入了 std::vector，这通常用于存储动态大小的元素集合，例如扫描到的 WiFi 网络列表或者菜单项
- 平台相关的包含 (#if defined(ESP8266) || defined(ESP32)): 这部分代码根据当前编译的平台选择性地包含头文件
  - 对于 ESP8266，包含了 ESP8266WiFi.h 和 ESP8266WebServer.h，以及可选的 ESP8266mDNS.h
  - 对于 ESP32，包含了 WiFi.h (ESP32 WiFi 库), esp_wifi.h (底层 WiFi API), Update.h (OTA 更新), 以及根据 WM_WEBSERVERSHIM 宏选择包含 WebServer.h (通用 WebServer 接口) 或 ESP8266WebServer.h
- #include <DNSServer.h>: 配置门户通常需要一个 DNS 服务器来将所有域名请求重定向到设备自身的 IP 地址
- #include <memory>: 引入了 std::unique_ptr，用于管理 DNSServer 和 WebServer 对象的生命周期，避免内存泄漏

### 可选功能宏
```cpp
// #define WM_MDNS            // includes MDNS, also set MDNS with sethostname
// #define WM_FIXERASECONFIG  // use erase flash fix
// #define WM_ERASE_NVS       // esp32 erase(true) will erase NVS
// #define WM_RTC             // esp32 info page will include reset reasons
```
这些宏定义允许用户在编译时选择性地启用或禁用某些功能。例如，如果定义了 WM_MDNS，则会包含 mDNS 相关的库，从而允许设备通过主机名在本地网络中被发现。这些宏通常在用户需要特定功能时在项目配置中定义

### 平台特定宏和兼容性处理
```cpp
#ifdef ARDUINO_ESP8266_RELEASE_2_3_0
#warning "ARDUINO_ESP8266_RELEASE_2_3_0, some WM features disabled"
// @todo check failing on platform = espressif8266@1.7.3
#define WM_NOASYNC      // esp8266 no async scan wifi
#define WM_NOCOUNTRY    // esp8266 no country
#define WM_NOAUTH       // no httpauth
#define WM_NOSOFTAPSSID // no softapssid() @todo shim
#endif

#define WM_WEBSERVERSHIM // use webserver shim lib

#ifdef ESP8266

extern "C"
{
#include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#ifdef WM_MDNS
#include <ESP8266mDNS.h>
#endif

#ifndef ESP_getChipId
#define ESP_getChipId() ESP.getChipId()
#endif

#define WM_WIFIOPEN ENC_TYPE_NONE

#elif defined(ESP32)

// #define STRING2(x) #x
// #define STRING(x) STRING2(x)

// // #include <esp_idf_version.h>
// #ifdef ESP_IDF_VERSION
//     #pragma message "ESP_IDF_VERSION_MAJOR = " STRING(ESP_IDF_VERSION_MAJOR)
//     #pragma message "ESP_IDF_VERSION_MINOR = " STRING(ESP_IDF_VERSION_MINOR)
//     #pragma message "ESP_IDF_VERSION_PATCH = " STRING(ESP_IDF_VERSION_PATCH)
// #endif

// // #include "esp_arduino_version.h"
// #ifdef ESP_ARDUINO_VERSION
//     #pragma message "ESP_ARDUINO_VERSION_MAJOR = " STRING(ESP_ARDUINO_VERSION_MAJOR)
//     #pragma message "ESP_ARDUINO_VERSION_MINOR = " STRING(ESP_ARDUINO_VERSION_MINOR)
//     #pragma message "ESP_ARDUINO_VERSION_PATCH = " STRING(ESP_ARDUINO_VERSION_PATCH)
// #else
//     #include <core_version.h>
//     #pragma message "ESP_ARDUINO_VERSION_GIT  = " STRING(ARDUINO_ESP32_GIT_VER)//  0x46d5afb1
//     #pragma message "ESP_ARDUINO_VERSION_DESC = " STRING(ARDUINO_ESP32_GIT_DESC) //  1.0.6
//     // #pragma message "ESP_ARDUINO_VERSION_REL  = " STRING(ARDUINO_ESP32_RELEASE) //"1_0_6"
// #endif

#include <WiFi.h>
#include <esp_wifi.h>
#include <Update.h>

#ifndef ESP_getChipId
#define ESP_getChipId() (uint64_t) ESP.getEfuseMac()
#endif

#define WM_WIFIOPEN WIFI_AUTH_OPEN

#ifndef WEBSERVER_H
#ifdef WM_WEBSERVERSHIM
#include <WebServer.h>
#else
#include <ESP8266WebServer.h>
// Forthcoming official ? probably never happening
// https://github.com/esp8266/ESPWebServer
#endif
#endif

#ifdef WM_ERASE_NVS
#include <nvs.h>
#include <nvs_flash.h>
#endif

#ifdef WM_MDNS
#include <ESPmDNS.h>
#endif

#ifdef WM_RTC
#include <rom/rtc.h>
#endif

#else
#endif

#include <DNSServer.h>
#include <memory>

```
这部分代码处理了不同 Arduino Core 版本或平台之间的兼容性问题。例如，对于较旧的 ESP8266 Core 版本，某些功能可能不可用或存在 bug，因此通过宏定义禁用这些功能 (WM_NOASYNC, WM_NOCOUNTRY 等），并可能给出警告信息 (#warning)

### 常量定义
```cpp
// HTTP状态消息，用于在Web页面上西安市WIFI连接失败的原因，PROGMEM 关键字表示这些字符串存储在 Flash 存储器中，而不是 RAM，以节省宝贵的 RAM 资源
const char HTTP_STATUS_OFFPW[] PROGMEM = "Authentication Failure"; // STATION_WRONG_PASSWORD,  no eps32
const char HTTP_STATUS_OFFNOAP[] PROGMEM = "AP not found";         // WL_NO_SSID_AVAIL
const char HTTP_STATUS_OFFFAIL[] PROGMEM = "Could not Connect";    // WL_CONNECT_FAILED

// HTML页面信息
// 根据编译平台选择不同的设备类型
#ifdef ESP32
const char HTTP_INFO_esphead[] PROGMEM = "esp32";
#else
const char HTTP_INFO_esphead[] PROGMEM = "esp8266";
#endif

const char HTTP_INFO_wifihead[] PROGMEM = "WiFi";

const char S_debugPrefix[] PROGMEM = "*wm:";
const char S_NA[] PROGMEM = "Unknown";

// debug strings
const char D_HR[] PROGMEM = "--------------------";

// Strings 这些字符串很可能用作 HTTP 请求或 Web 表单中的参数名称
const char S_ip[] PROGMEM = "ip"; // ip地址
const char S_gw[] PROGMEM = "gw"; // 网关
const char S_sn[] PROGMEM = "sn"; // 子网掩码
const char S_dns[] PROGMEM = "dns"; // DNS服务器

// http 这些字符串定义了常用的 HTTP 头部信息  
const char HTTP_HEAD_JSON[] PROGMEM = "application/json"; // 表示响应的数据格式是 JSON
const char HTTP_HEAD_CORS[] PROGMEM = "Access-Control-Allow-Origin";  
const char HTTP_HEAD_CORS_ALLOW_ALL[] PROGMEM = "*";  // 表示允许来自任何域的请求，这在某些开发或特定应用场景下可能会使用

```

### 枚举和数组定义
```cpp
const char *const WIFI_STA_STATUS[] PROGMEM{
    "WL_IDLE_STATUS",           // 0 STATION_IDLE
    "WL_NO_SSID_AVAIL",         // 1 STATION_NO_AP_FOUND
    "WL_SCAN_COMPLETED",        // 2
    "WL_CONNECTED",             // 3 STATION_GOT_IP
    "WL_CONNECT_FAILED",        // 4 STATION_CONNECT_FAIL, STATION_WRONG_PASSWORD(NI)
    "WL_CONNECTION_LOST",       // 5
    "WL_DISCONNECTED",          // 6
    "WL_STATION_WRONG_PASSWORD" // 7 KLUDGE
};

#ifdef ESP32
const char *const AUTH_MODE_NAMES[] PROGMEM{
    "OPEN",
    "WEP",
    "WPA_PSK",
    "WPA2_PSK",
    "WPA_WPA2_PSK",
    "WPA2_ENTERPRISE",
    "MAX"};
#elif defined(ESP8266)
const char *const AUTH_MODE_NAMES[] PROGMEM{
    "",
    "",
    "WPA_PSK", // 2 ENC_TYPE_TKIP
    "",
    "WPA2_PSK", // 4 ENC_TYPE_CCMP
    "WEP",      // 5 ENC_TYPE_WEP
    "",
    "OPEN",         // 7 ENC_TYPE_NONE
    "WPA_WPA2_PSK", // 8 ENC_TYPE_AUTO
};
#endif

const char *const WIFI_MODES[] PROGMEM = {"NULL", "STA", "AP", "STA+AP"};
```


### 国家代码定义
```cpp
#ifdef ESP32
// as 2.5.2
// typedef struct {
//     char                  cc[3];   /**< country code string */
//     uint8_t               schan;   /**< start channel */
//     uint8_t               nchan;   /**< total channel number */
//     int8_t                max_tx_power;   /**< This field is used for getting WiFi maximum transmitting power, call esp_wifi_set_max_tx_power to set the maximum transmitting power. */
//     wifi_country_policy_t policy;  /**< country policy */
// } wifi_country_t;
const wifi_country_t WM_COUNTRY_US{"US", 1, 11, CONFIG_ESP32_PHY_MAX_WIFI_TX_POWER, WIFI_COUNTRY_POLICY_AUTO};
const wifi_country_t WM_COUNTRY_CN{"CN", 1, 13, CONFIG_ESP32_PHY_MAX_WIFI_TX_POWER, WIFI_COUNTRY_POLICY_AUTO};
const wifi_country_t WM_COUNTRY_JP{"JP", 1, 14, CONFIG_ESP32_PHY_MAX_WIFI_TX_POWER, WIFI_COUNTRY_POLICY_AUTO};
#elif defined(ESP8266) && !defined(WM_NOCOUNTRY)
// typedef struct {
//     char cc[3];               /**< country code string */
//     uint8_t schan;            /**< start channel */
//     uint8_t nchan;            /**< total channel number */
//     uint8_t policy;           /**< country policy */
// } wifi_country_t;
const wifi_country_t WM_COUNTRY_US{"US", 1, 11, WIFI_COUNTRY_POLICY_AUTO};
const wifi_country_t WM_COUNTRY_CN{"CN", 1, 13, WIFI_COUNTRY_POLICY_AUTO};
const wifi_country_t WM_COUNTRY_JP{"JP", 1, 14, WIFI_COUNTRY_POLICY_AUTO};
#endif
```
这部分定义了不同国家/地区的 WiFi 配置信息，例如允许的信道范围和最大发射功率。wifi_country_t 是 ESP-IDF 或 ESP8266 SDK 中定义的结构体。用户可以通过 setCountry() 方法设置设备的 WiFi 国家代码

### ThingsCloudWiFiManager 类定义
```cpp
class ThingsCloudWiFiManager
{
// 公有成员函数
public:
    // 构造函数(多态)
    ThingsCloudWiFiManager(Stream &consolePort);  // 接受一个Steram对象，用于输出调试信息
    ThingsCloudWiFiManager(char const *apNamePrefix, char const *apPassword = NULL);  // 允许自定义配置门户(热点WIFI)的WIIF名和密码
    // 析构函数
    ~ThingsCloudWiFiManager();
    // 提供一个显式的初始化方法
    void WiFiManagerInit();

    // 尝试自动连接到保存的 WiFi 网络。如果失败，可能会启动配置门户。
    boolean autoConnect();

    // 手动启动配置门户，自动生成 AP 名称
    boolean startConfigPortal(); // auto generates apname

    // 手动停止配置门户
    bool stopConfigPortal();

    // 在非阻塞模式下运行配置门户时，需要周期性调用此函数来处理 Web 服务器请求
    boolean process();

    // 获取配置门户的 AP 名称
    String getConfigPortalSSID();
    // 将 RSSI 值转换为信号质量百分并返回
    int getRSSIasQuality(int RSSI);

    // 清除保存的 WiFi 凭据
    void resetSettings();

    // 重启 ESP 设备
    void reboot();

    // 断开 WiFi 连接，但不清除保存的凭据
    bool disconnect();

    // 擦除ESP上保存的配置信息
    bool erase();
    bool erase(bool opt);
    
    // 关联一个 ThingsCloudMQTT 客户端实例
    void linkMQTTClient(ThingsCloudMQTT *client);

    // 设置设备的 Key
    void setDeviceKey(String deviceKey);

    // 获取客户 ID
    String getCustomerId();

    // 设置回调函数

    // 在设置AP模式后启动回调函数
    void setAPCallback(std::function<void(ThingsCloudWiFiManager *)> func);

    // 在设置Web模式后启动回调函数
    void setWebServerCallback(std::function<void()> func);

    // 在配置清除后启动回调函数
    void setConfigResetCallback(std::function<void()> func);

    // 在设置WIFI配置保存后启动回调函数
    void setSaveConfigCallback(std::function<void()> func);

    // 设置保存配置前的回调
    void setPreSaveConfigCallback(std::function<void()> func);

    // 设置 OTA 更新前的回调
    void setPreOtaUpdateCallback(std::function<void()> func);

    // sets timeout before AP,webserver loop ends and exits even if there has been no setup.
    // useful for devices that failed to connect at some point and got stuck in a webserver loop
    // in seconds setConfigPortalTimeout is a new name for setTimeout, ! not used if setConfigPortalBlocking
    // 设置配置门户超时时间
    void setConfigPortalTimeout(unsigned long seconds);
    void setTimeout(unsigned long seconds); // @deprecated, alias

    // 设置连接 WiFi 的超时时间
    void setConnectTimeout(unsigned long seconds);

    // 设置自动连接的重试次数
    void setConnectRetries(uint8_t numRetries); // default 1

    // 设置保存配置后连接 WiFi 的超时时间
    void setSaveConnectTimeout(unsigned long seconds);

    // 控制保存配置后是否自动连接
    void setSaveConnect(bool connect = true);

    // 启用/禁用调试输出，并可设置前缀
    void setDebugOutput(boolean debug);
    void setDebugOutput(boolean debug, String prefix); // log line prefix, default "*wm:"

    // 设置扫描到的 AP 的最小信号质量
    void setMinimumSignalQuality(int quality = 8);

    // 设置静态 IP  /网关 /subnet
    void setAPStaticIPConfig(IPAddress ip, IPAddress gw, IPAddress sn);

    // sets config for a static IP
    void setSTAStaticIPConfig(IPAddress ip, IPAddress gw, IPAddress sn);

    // sets config for a static IP with DNS
    void setSTAStaticIPConfig(IPAddress ip, IPAddress gw, IPAddress sn, IPAddress dns);

    // if this is set, it will exit after config, even if connection is unsuccessful.
    void setBreakAfterConfig(boolean shouldBreak);

    // if this is set, portal will be blocking and wait until save or exit,
    // is false user must manually `process()` to handle config portal,
    // setConfigPortalTimeout is ignored in this mode, user is responsible for closing configportal
    void setConfigPortalBlocking(boolean shouldBlock);

    // if this is set, customise style
    void setCustomHeadElement(const char *element);

    // if this is true, remove duplicated Access Points - defaut true
    void setRemoveDuplicateAPs(boolean removeDuplicates);

    // setter for ESP wifi.persistent so we can remember it and restore user preference, as WIFi._persistent is protected
    void setRestorePersistent(boolean persistent);

    // if true, always show static net inputs, IP, subnet, gateway, else only show if set via setSTAStaticIPConfig
    void setShowStaticFields(boolean alwaysShow);

    // if true, always show static dns, esle only show if set via setSTAStaticIPConfig
    void setShowDnsFields(boolean alwaysShow);

    // toggle showing the saved wifi password in wifi form, could be a security issue.
    void setShowPassword(boolean show);

    // if false, disable captive portal redirection
    void setCaptivePortalEnable(boolean enabled);

    // if false, timeout captive portal even if a STA client connected to softAP (false), suggest disabling if captiveportal is open
    void setAPClientCheck(boolean enabled);

    // if true, reset timeout when webclient connects (true), suggest disabling if captiveportal is open
    void setWebPortalClientCheck(boolean enabled);

    // if true, enable autoreconnecting
    void setWiFiAutoReconnect(boolean enabled);

    // if true, wifiscan will show percentage instead of quality icons, until we have better templating
    void setScanDispPerc(boolean enabled);

    // if true (default) then start the config portal from autoConnect if connection failed
    void setEnableConfigPortal(boolean enable);

    // set a custom hostname, sets sta and ap dhcp client id for esp32, and sta for esp8266
    bool setHostname(const char *hostname);
    bool setHostname(String hostname);

    // show erase wifi onfig button on info page, true
    void setShowInfoErase(boolean enabled);

    // show OTA upload button on info page
    void setShowInfoUpdate(boolean enabled);

    // set ap channel
    void setWiFiAPChannel(int32_t channel);

    // set ap hidden
    void setWiFiAPHidden(bool hidden); // default false

    // clean connect, always disconnect before connecting
    void setCleanConnect(bool enable); // default false

    // set the webapp title, default ThingsCloudWiFiManager
    void setTitle(String title);

    // add params to its own menu page and remove from wifi, NOT TO BE COMBINED WITH setMenu!
    void setParamsPage(bool enable);

    // get last connection result, includes autoconnect and wifisave
    uint8_t getLastConxResult();

    // get a status as string
    String getWLStatusString(uint8_t status);
    String getWLStatusString();

    // get wifi mode as string
    String getModeString(uint8_t mode);

    // check if the module has a saved ap to connect to
    bool getWiFiIsSaved();

    // helper to get saved password, if persistent get stored, else get current if connected
    String getWiFiPass(bool persistent = true);

    // helper to get saved ssid, if persistent get stored, else get current if connected
    String getWiFiSSID(bool persistent = true);

    // debug output the softap config
    void debugSoftAPConfig();

    // debug output platform info and versioning
    void debugPlatformInfo();

    // helper for html
    String htmlEntities(String str);

    // set the country code for wifi settings, CN
    void setCountry(String cc);

    // set body class (invert), may be used for hacking in alt classes
    void setClass(String str);

    // set dark mode via invert class
    void setDarkMode(bool enable);

    // get default ap esp uses , esp_chipid etc
    String getDefaultAPName();

    // get esp chip unique id
    String getEspChipUniqueId();

    // set port of webserver, 80
    void setHttpPort(uint16_t port);

    // check if config portal is active (true)
    bool getConfigPortalActive();

    // check if web portal is active (true)
    bool getWebPortalActive();

    // to preload autoconnect for test fixtures or other uses that skip esp sta config
    bool preloadWiFi(String ssid, String pass);

    // get hostname helper
    String getWiFiHostname();

    std::unique_ptr<DNSServer> dnsServer;

#if defined(ESP32) && defined(WM_WEBSERVERSHIM)
    using WM_WebServer = WebServer;
#else
    using WM_WebServer = ESP8266WebServer;
#endif

    std::unique_ptr<WM_WebServer> server;

private:
    std::vector<uint8_t> _menuIds;
    std::vector<const char *> _menuIdsParams = {"wifi", "param", "info", "exit"};
    std::vector<const char *> _menuIdsUpdate = {"wifi", "param", "info", "update", "exit"};
    std::vector<const char *> _menuIdsDefault = {"wifi", "info", "exit", "sep", "update"};

    // ip configs @todo struct ?
    IPAddress _ap_static_ip;
    IPAddress _ap_static_gw;
    IPAddress _ap_static_sn;
    IPAddress _sta_static_ip;
    IPAddress _sta_static_gw;
    IPAddress _sta_static_sn;
    IPAddress _sta_static_dns;

    // defaults
    const byte DNS_PORT = 53;
    const byte HTTP_PORT = 80;
    String _apName = "";
    String _apPassword = "";
    String _ssid = "";
    String _pass = "";
    String _defaultssid = "";
    String _defaultpass = "";
    String _deviceKey = "";
    String _customerId = "";
    ThingsCloudMQTT *_mqttClient = NULL;

    // options flags
    unsigned long _configPortalTimeout = 0;   // ms close config portal loop if set (depending on  _cp/webClientCheck options)
    unsigned long _connectTimeout = 0;        // ms stop trying to connect to ap if set
    unsigned long _saveTimeout = 0;           // ms stop trying to connect to ap on saves, in case bugs in esp waitforconnectresult
    unsigned long _configPortalStart = 0;     // ms config portal start time (updated for timeouts)
    unsigned long _webPortalAccessed = 0;     // ms last web access time
    WiFiMode_t _usermode = WIFI_STA;          // Default user mode
    String _wifissidprefix = "esp32";         // auto apname prefix prefix+chipid
    uint8_t _lastconxresult = WL_IDLE_STATUS; // store last result when doing connect operations
    int _numNetworks = 0;                     // init index for numnetworks wifiscans
    unsigned long _lastscan = 0;              // ms for timing wifi scans
    unsigned long _startscan = 0;             // ms for timing wifi scans
    int _cpclosedelay = 2000;                 // delay before wifisave, prevents captive portal from closing to fast.
    bool _cleanConnect = false;               // disconnect before connect in connectwifi, increases stability on connects
    bool _connectonsave = true;               // connect to wifi when saving creds
    bool _disableSTA = false;                 // disable sta when starting ap, always
    bool _disableSTAConn = true;              // disable sta when starting ap, if sta is not connected ( stability )
    bool _channelSync = false;                // use same wifi sta channel when starting ap
    int32_t _apChannel = 0;                   // channel to use for ap
    bool _apHidden = false;                   // store softap hidden value
    uint16_t _httpPort = 8080;                // port for webserver
    // uint8_t       _retryCount             = 0; // counter for retries, probably not needed if synchronous
    uint8_t _connectRetries = 1;   // number of sta connect retries, force reconnect, wait loop (connectimeout) does not always work and first disconnect bails
    unsigned long _startconn = 0;  // ms for timing wifi connects
    bool _aggresiveReconn = false; // use an agrressive reconnect strategy, WILL delay conxs
                                   // on some conn failure modes will add delays and many retries to work around esp and ap bugs, ie, anti de-auth protections
    bool _allowExit = true;        // allow exit non blocking

#ifdef ESP32
    wifi_event_id_t wm_event_id;
    static uint8_t _lastconxresulttmp; // tmp var for esp32 callback
#endif

#ifndef WL_STATION_WRONG_PASSWORD
    uint8_t WL_STATION_WRONG_PASSWORD = 7; // @kludge define a WL status for wrong password
#endif

    // parameter options
    int _minimumQuality = -1;                // filter wifiscan ap by this rssi
    int _staShowStaticFields = 0;            // ternary 1=always show static ip fields, 0=only if set, -1=never(cannot change ips via web!)
    int _staShowDns = 0;                     // ternary 1=always show dns, 0=only if set, -1=never(cannot change dns via web!)
    boolean _removeDuplicateAPs = true;      // remove dup aps from wifiscan
    boolean _showPassword = false;           // show or hide saved password on wifi form, might be a security issue!
    boolean _shouldBreakAfterConfig = false; // stop configportal on save failure
    boolean _configPortalIsBlocking = true;  // configportal enters blocking loop
    boolean _enableCaptivePortal = false;    // enable captive portal redirection
    boolean _userpersistent = true;          // users preffered persistence to restore
    boolean _wifiAutoReconnect = true;       // there is no platform getter for this, we must assume its true and make it so
    boolean _apClientCheck = false;          // keep cp alive if ap have station
    boolean _webClientCheck = true;          // keep cp alive if web have client
    boolean _scanDispOptions = false;        // show percentage in scans not icons
    boolean _paramsInWifi = true;            // show custom parameters on wifi page
    boolean _showInfoErase = true;           // info page erase button
    boolean _showInfoUpdate = true;          // info page update button
    boolean _showBack = false;               // show back button
    boolean _enableConfigPortal = true;      // use config portal if autoconnect failed
    String _hostname = "";                   // hostname for esp8266 for dhcp, and or MDNS

    String _bodyClass = ""; // class to add to body
    String _title = "";     // app title -  default ThingsCloudWiFiManager

    // internal options

    // wifiscan notes
    // The following are background wifi scanning optimizations
    // experimental to make scans faster, preload scans after starting cp, and visiting home page, so when you click wifi its already has your list
    // ideally we would add async and xhr here but I am holding off on js requirements atm
    // might be slightly buggy since captive portals hammer the home page, @todo workaround this somehow.
    // cache time helps throttle this
    // async enables asyncronous scans, so they do not block anything
    // the refresh button bypasses cache
    // no aps found is problematic as scans are always going to want to run, leading to page load delays
    boolean _preloadwifiscan = false;    // preload wifiscan if true
    boolean _asyncScan = false;          // perform wifi network scan async
    unsigned int _scancachetime = 30000; // ms cache time for background scans

    boolean _disableIpFields = false; // modify function of setShow_X_Fields(false), forces ip fields off instead of default show if set, eg. _staShowStaticFields=-1

    String _wificountry = ""; // country code, @todo define in strings lang

    // wrapper functions for handling setting and unsetting persistent for now.
    bool esp32persistent = false;
    bool _hasBegun = false; // flag wm loaded,unloaded
    void _begin();
    void _end();

    void setupConfigPortal();
    bool shutdownConfigPortal();
    bool setupHostname(bool restart);

#ifdef NO_EXTRA_4K_HEAP
    boolean _tryWPS = false; // try WPS on save failure, unsupported
    void startWPS();
#endif

    bool startAP();
    void setupDNSD();

    uint8_t connectWifi(String ssid, String pass, bool connect = true);
    bool setSTAConfig();
    bool wifiConnectDefault();
    bool wifiConnectNew(String ssid, String pass, bool connect = true);

    uint8_t waitForConnectResult();
    uint8_t waitForConnectResult(uint32_t timeout);
    void updateConxResult(uint8_t status);

    // webserver handlers
    void handleWifiList();
    void handleWifiSave();
    void handleInfo();
    void handleReset();
    void handleNotFound();
    void handleWiFiStatus();

    boolean configPortalHasTimeout();
    uint8_t processConfigPortal();
    void stopCaptivePortal();

    // wifi platform abstractions
    bool WiFi_Mode(WiFiMode_t m);
    bool WiFi_Mode(WiFiMode_t m, bool persistent);
    bool WiFi_Disconnect();
    bool WiFi_enableSTA(bool enable);
    bool WiFi_enableSTA(bool enable, bool persistent);
    bool WiFi_eraseConfig();
    uint8_t WiFi_softap_num_stations();
    bool WiFi_hasAutoConnect();
    void WiFi_autoReconnect();
    String WiFi_SSID(bool persistent = true) const;
    String WiFi_psk(bool persistent = true) const;
    bool WiFi_scanNetworks();
    bool WiFi_scanNetworks(bool force, bool async);
    bool WiFi_scanNetworks(unsigned int cachetime, bool async);
    bool WiFi_scanNetworks(unsigned int cachetime);
    void WiFi_scanComplete(int networksFound);
    bool WiFiSetCountry();

#ifdef ESP32

// check for arduino or system event system, handle esp32 arduino v2 and IDF
#if defined(ESP_ARDUINO_VERSION) && defined(ESP_ARDUINO_VERSION_VAL)

#define WM_ARDUINOVERCHECK ESP_ARDUINO_VERSION >= ESP_ARDUINO_VERSION_VAL(2, 0, 0)

#ifdef WM_ARDUINOVERCHECK
#define WM_ARDUINOEVENTS
#else
#define WM_NOSOFTAPSSID
#endif

#endif

#ifdef WM_ARDUINOEVENTS
    void WiFiEvent(WiFiEvent_t event, arduino_event_info_t info);
#else
    void WiFiEvent(WiFiEvent_t event, system_event_info_t info);
#endif
#endif

    String getScanItems();
    // helpers
    boolean isIp(String str);
    String toStringIp(IPAddress ip);
    boolean validApPassword();
    String encryptionTypeStr(uint8_t authmode);

    // flags
    boolean connect;
    boolean abort;
    boolean reset = false;
    boolean configPortalActive = false;
    boolean webPortalActive = false;
    boolean portalTimeoutResult = false;
    boolean portalAbortResult = false;
    boolean storeSTAmode = true; // option store persistent STA mode in connectwifi
    int timer = 0;               // timer for debug throttle for numclients, and portal timeout messages

    // debugging
    typedef enum
    {
        DEBUG_ERROR = 0,
        DEBUG_NOTIFY = 1, // default stable
        DEBUG_VERBOSE = 2,
        DEBUG_DEV = 3, // default dev
        DEBUG_MAX = 4
    } wm_debuglevel_t;

    boolean _debug = true;
    String _debugPrefix = FPSTR(S_debugPrefix);

    wm_debuglevel_t debugLvlShow = DEBUG_VERBOSE; // at which level start showing [n] level tags

// build debuglevel support
// @todo use DEBUG_ESP_x?

// Set default debug level
#ifndef WM_DEBUG_LEVEL
#define WM_DEBUG_LEVEL DEBUG_VERBOSE // development default, not release
#endif

// override debug level OFF
#ifdef WM_NODEBUG
#undef WM_DEBUG_LEVEL
#endif

#ifdef WM_DEBUG_LEVEL
    uint8_t _debugLevel = (uint8_t)WM_DEBUG_LEVEL;
#else
    uint8_t _debugLevel = DEBUG_VERBOSE; // default debug level
#endif

// @todo use DEBUG_ESP_PORT ?
#ifdef WM_DEBUG_PORT
    Stream &_debugPort = WM_DEBUG_PORT;
#else
    Stream &_debugPort = Serial;         // debug output stream ref
#endif

    template <typename Generic>
    void DEBUG_WM(Generic text);

    template <typename Generic>
    void DEBUG_WM(wm_debuglevel_t level, Generic text);
    template <typename Generic, typename Genericb>
    void DEBUG_WM(Generic text, Genericb textb);
    template <typename Generic, typename Genericb>
    void DEBUG_WM(wm_debuglevel_t level, Generic text, Genericb textb);

    // callbacks
    // @todo use cb list (vector) maybe event ids, allow no return value
    std::function<void(ThingsCloudWiFiManager *)> _apcallback;
    std::function<void()> _webservercallback;
    std::function<void()> _savewificallback;
    std::function<void()> _presavecallback;
    std::function<void()> _saveparamscallback;
    std::function<void()> _resetcallback;
    std::function<void()> _preotaupdatecallback;

    template <class T>
    auto optionalIPFromString(T *obj, const char *s) -> decltype(obj->fromString(s))
    {
        return obj->fromString(s);
    }
    auto optionalIPFromString(...) -> bool
    {
        // DEBUG_WM("NO fromString METHOD ON IPAddress, you need ESP8266 core 2.1.0 or newer for Custom IP configuration to work.");
        return false;
    }
};

#endif

#endif

```