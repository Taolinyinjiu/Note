当前任务:将VINS与Sunray项目结合，首先在仿真环境中实现基于VINS里程计的定位飞行，然后尝试使用推力-姿态控制接口，底层为Sunray系列的PID控制器。

### 12.7
- 完成vins-fusion的编译工作，测试在gazebo中vins工作良好，测试模型为sunray150_mid360_d435，测试场景为cafe.world
TODO：阅读fastdrone250项目结构，观察中间件px4ctrl如何替换为sunray接口，或者根据px4ctrl改写sunray控制接口  

