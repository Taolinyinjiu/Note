# Docker创建镜像

sudo docker run -dit --name=sg-slam -v /home/taolin:/home/taolin -v /tmp/.X11-unix:/tmp/.X11-unix  --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all --device /dev/snd -e DISPLAY=unix$DISPLAY -w /home/taolin fishros2/ros:melodic-desktop-ful ubunt