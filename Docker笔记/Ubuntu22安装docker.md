# 发展历史

随着Docker技术的发展，目前Docker官网提供Docker Desktop和Docker Engine两种产品。

Docker Desktop是一个桌面应用程序，可以在Mac ，Windows ，Linux上运行，它为开发人员提供了一个方便的方式来使用Docker和运行本地容器。

# 安装Docker Desktop

> 官网link：https://docs.docker.com/desktop/setup/install/linux/ubuntu/

1. 通过APT仓库下载一些依赖
   ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```
2. 下载Docker的包
   ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
3. 验证组件完整性
   ```bash
   sudo docker run hello-world
   ```
   这里可能会由于网络问题失败，这里提供一个第三方的docker仓库，以供尝试
   ```bash
   sudo docker run -d -P m.daocloud.io/docker.io/library/nginx
   ```
   注意这里我没有将user加入到docker组，因此需要使用sudo提权
4. 登录docker desktop
   在登录之前，需要先初始化GPG密钥
   gpg --generate-key