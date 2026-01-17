在sunray300上部署vins，标定外参，飞行，部署ego

## Sunray300硬件环境
机载电脑: Orin Nano 8GB (ARN64)
操作系统: Ubuntu20
引导存储: NVME 256GB
L4T 版本: R35.6.3
JetPack: 5.1.4

## docker部署相关
docker run -it --rm \
    --runtime nvidia \
    --network host \
    --privileged \
    --ipc=host \
    -v /dev:/dev
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /home/yundrone:/workspace \
    dustynv/ros:noetic-desktop-l4t-r35.4.1


    docker run -it \
    --name vins_container
    --runtime nvidia \
    --network host \
    --ipc=host \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /dev:/dev \
    -v /home/yundrone:/workspace \
    -w /workspace \
    dustynv/ros:noetic-desktop-l4t-r35.4.1






xhost +local: >> /dev/null
echo "请输入指令控制vins容器: 重启(r) 进入(e) 启动(s) 关闭(c) 删除(d) 测试(t):"
read choose
case $choose in
s) docker start vinsvins_container;;
r) docker restart ;;
e) docker exec -it vinsvins_container /bin/bash;;
c) docker stop vinsvins_container;;
d) docker stop vinsvins_container && docker rm vinsvins_container && sudo rm -rf ~/.docker_container/vinsvins_container;;
t) docker exec -it vinsvins_container /bin/bash -c "source /ros_entrypoint.sh && roscore";;
esac
newgrp docker


sunray300部署vins结束，里程计稳定，
问题在于Sunray300的姿态控制器参数有问题，导致炸鸡