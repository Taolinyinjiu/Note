# IMU系统的运动学
惯性测量单元(Inertial measurement unit 简称IMU)已经普及到了各个方面，现在绝大多数的电子设备，如手机，手表，相机等都带有IMU。通常他们的体积很小,安装在内部，可以提供有效的局部运动估计。

在自动驾驶中，惯性导航器件也是十分基础的定位装置，惯性导航提供的定位效果基本与外部环境和其他 传感器数据无关，因此具有很高的泛用性和可靠性。

典型的六轴IMU由陀螺仪(Gyroscope)和加速度计(Accelerator)组成，其测量的目标都是物体的惯性。IMU通常安装在一个运动的系统中，通过测量运动载体的惯性，推断物体本身的状态。这些与惯性相关的物理量通常不是直接的位置和旋转，而是经过微分后的物理量。IMU的陀螺仪可以测量物体的**角速度**，而加速度计可以测量物体的**加速度**。

根据运动学的相关知识，我们可以简单地列出一个连续时间模型的运动方程:
$$
\begin{equation}
  \begin{aligned}
    & \dot{\mathbf{R}} = \mathbf{R}\omega^{\wedge} 或者 \dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \mathbf{\omega} \\
    & \dot{\rho} = \upsilon \\
    & \dot{\upsilon} = \alpha 
  \end{aligned}
\end{equation}
$$