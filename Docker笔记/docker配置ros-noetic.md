# 拉取镜像
sudo docker pull fishros2/ros:noetic-desktop-full

# 创建容器

sudo docker run -dit \
--name=ros-px4ctrl \
--privileged  \
-v /dev:/dev \
-v /home/taolin:/home/taolin \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /home/taolin \
--net=host \
--gpus all \
--runtime=nvidia \
fishros2/ros:noetic-desktop-full

fishros2/ros:noetic-desktop-full

command_create_x11 = "sudo docker run -dit --name={} -v {}:{} -v /tmp/.X11-unix:/tmp/.X11-unix {} -v /dev/dri:/dev/dri {} -e DISPLAY=unix$DISPLAY -w {}  {}".format(container_name,home,home,use_dri,use_snd,home,RosVersions.get_image(name))


# 创建ros包
catkin_create_pkg yolo_detect rospy sensor_msgs cv_bridge std_msgs image_transport

# 为vscode提权
sudo code --user-data-dir=/home/taolin/.config/Code/ --no-sandbox --disable-gpu-sandbox


docker run -dit \
--name=ros-px4ctrl \
--privileged  \
-v /dev:/dev \
-v /home/taolin:/home/taolin \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /home/taolin \
--net=host \
fishros2/ros:noetic-desktop-full



// 从ubuntu20创建全新的ros环境
sudo docker run -dit \
--name=ros-px4ctrl \
--privileged  \
-v /dev:/dev \
-v /home/taolin:/home/taolin \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /home/taolin \
--net=host \
--gpus all \
--runtime=nvidia \
ubuntu:20.04

// 从fishros的ros-noetic创建环境
sudo docker run -dit \
--name=ros-px4ctrl \
--privileged  \
-v /dev:/dev \
-v /home/taolin:/home/taolin \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /home/taolin \
--net=host \
--gpus all \
--runtime=nvidia \
fishros2/ros:noetic-desktop-full



sudo docker run -dit \
--name=mini-viobot \
--privileged  \
-v /dev:/dev \
-v /home/taolin:/home/taolin \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /home/taolin \
--net=host \
fishros2/ros:humble-desktop-full







```bash
sudo docker run -dit \ 
--name ubuntu22 \                                                                                                                 --privileged \                                                                                                                   --net=host \                                                                                                                     -v /dev:/dev \                                                                                                                   -v /home/taolin:/home/taolin \                                                                                                   -v /tmp/.X11-unix:/tmp/.X11-unix \                                                                                               -v $HOME/.Xauthority:/root/.Xauthority:ro \                                                                                       -e DISPLAY=$DISPLAY \                                                                                                             -e XAUTHORITY=/root/.Xauthority \                                                                                                 -w /home/taolin \                                                                                                             	ubuntu:22.04
```