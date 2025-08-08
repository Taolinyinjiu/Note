1. 更换pip3源为腾讯源
   - 先使用腾讯源更新pip
   ``` bash
   pip install -i https://mirrors.cloud.tencent.com/pypi/simple --upgrade pip
   ```
   - 设置pip3全局镜像源为腾讯源
    ``` bash
    pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
    ```

2. 下载ultralytics
   ```bash
   pip install ultralytics
   ```
3. 
