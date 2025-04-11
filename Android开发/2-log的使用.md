### 什么是log?
在 Android 开发中，日志（Log）是开发者用来调试和追踪应用程序行为的重要工具。通过在代码中插入日志语句，开发者可以在运行时输出信息，帮助他们了解程序的执行流程、变量的值以及可能出现的错误。Android 提供了一个强大的日志系统，允许开发者在开发过程中记录各种类型的信息。
#### log类
Android SDK 提供了 android.util.Log 类，它包含了用于输出日志信息的静态方法。
通过 Log 类，开发者可以输出不同级别的日志信息，例如调试信息、错误信息和警告信息。

#### log日志级别
Android 日志系统定义了不同的日志级别，用于区分日志信息的重要性。常用的日志级别包括：
- Log.v(String tag, String msg)：Verbose（详细）：用于输出最详细的调试信息。
- Log.d(String tag, String msg)：Debug（调试）：用于输出调试信息，在开发阶段使用。
- Log.i(String tag, String msg)：Info（信息）：用于输出一般的信息。
- Log.w(String tag, String msg)：Warn（警告）：用于输出警告信息，表示可能存在潜在问题。
- Log.e(String tag, String msg)：Error（错误）：用于输出错误信息，表示程序发生了错误。
- Log.wtf(String tag, String msg): 用于输出严重错误信息，表示程序发生了非常严重的错误。

##### log tag(标签)
log中的tag是一个字符串,用于表示log信息的来源,通过使用不同的log tag,开发者可以轻松的过滤和查找特定模块的log信息


##### Example
``` java
import android.util.Log;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d(TAG, "onCreate() called");

        int value = 10;
        Log.i(TAG, "Value: " + value);

        try {
            // Some code that might cause an error
        } catch (Exception e) {
            Log.e(TAG, "Error: ", e);
        }
    }
}
```