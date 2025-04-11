### Toast
在Android开发中,Toast是一种向用户显示简短消息的视图,它通常出现在屏幕的底部,短暂的显示一段时间后自动消失,不会打断用户当前的操作.

#### Toast的特点
- 非模态： Toast 不会中断用户的交互，用户可以继续与应用程序进行交互，而无需关闭 Toast。
- 短暂显示： Toast 会自动在屏幕上显示一段时间（通常是短时间或长时间），然后自动消失。
- 简单易用： Toast 的使用非常简单，只需要几行代码即可显示一条消息。
- 轻量级： Toast 是一种轻量级的通知方式，不会占用太多系统资源。

#### Toast的基本用法
- 使用 Toast.makeText() 方法创建一个 Toast 对象。
- 调用 Toast 对象的 show() 方法显示 Toast。

#### Toast 的常用方法

- Toast.makeText(Context context, CharSequence text, int duration): 创建一个 Toast 对象。
  - context: 上下文对象，通常是 Activity 或 Application。
  - text: 要显示的文本消息。
  - duration: Toast 的显示时长，可以是 Toast.LENGTH_SHORT（短时间）或 Toast.LENGTH_LONG（长时间）。
- Toast.show(): 显示 Toast。
- Toast.setGravity(int gravity, int xOffset, int yOffset): 设置 Toast 的显示位置。
  - gravity: 显示位置，例如 Gravity.CENTER（居中）、Gravity.TOP（顶部）或 Gravity.BOTTOM（底部）。
  - xOffset: 水平偏移量。
  - yOffset: 垂直偏移量。

#### Example
``` java
import android.content.Context;
import android.widget.Toast;

public class ToastUtil {

    public static void showShortToast(Context context, String message) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }

    public static void showLongToast(Context context, String message) {
        Toast.makeText(context, message, Toast.LENGTH_LONG).show();
    }
}
```
在一个activity中使用Toast
``` java
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 注意,需要先执行setContentView函数,加载布局文件,否则findViewById函数将返回null.
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ToastUtil.showShortToast(MainActivity.this, "Button clicked!");
            }
        });
    }
}
```