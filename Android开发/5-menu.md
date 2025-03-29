#### menu
通常所提到的menu,指的是下拉菜单.下拉菜单让用户单击图标，文本字段或其他组件，然后会跳出一个菜单,用户可以选择菜单上的选项进行点击.

#### 新建资源文件
在res文件夹下新建一个文件夹，命名为menu
在menu文件夹下创建一个文件，命名可随意。这里我命名为main.xml，该文件即为菜单选项的布局文件。
例如：
```xml

<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:id="@+id/add_item"
        android:title="我是一个添加"/>
    <item android:id="@+id/remove_item"
        android:title="我是一个删除"/>

</menu>
```

该文件定义了两个菜单的选项，分别是添加和删除，在活动中进行注册，以及回调
```java
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if(item.getItemId() == R.id.add_item) {
            Toast.makeText(this, "You clicked Add", Toast.LENGTH_SHORT).show();
        }
        else
            Toast.makeText(this, "You clicked Remove", Toast.LENGTH_SHORT).show();
        return true;
    }
```

值得注意的是，在新版的Android中，menu的item已不再是一个常量，因此无法使用switch进行处理