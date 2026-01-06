docker run -it \
  --name boton_mini \
  --privileged \
  --net=host \
  --ipc=host \
  --pid=host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /dev:/dev \
  -v /dev/shm:/dev/shm \
  -v /etc/localtime:/etc/localtime:ro \
  -v /home/yundrone:/workspace \
  --security-opt seccomp=unconfined \
  boton_mini_test:v1.0