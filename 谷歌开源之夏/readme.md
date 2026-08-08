## ArduPilot在2026年谷歌编程之夏建议项目列表

> https://summerofcode.withgoogle.com/programs/2026/organizations/ardupilot
> https://ardupilot.org/dev/docs/gsoc-ideas-list.html

这是ArduPilot开发者为GSoC 2026推荐的项目列表。这些只是建议，如果你有自己的想法，请在ArduPilot Discord聊天或讨论服务器上讨论。

- SITL Model Generation from Flight Data

- Multi-Drone Mesh Networking (MAVLink-aware)

- ArduHumanoid (ArduPilot controlling a simple humanoid)

- AI-Assisted Log Diagnosis & Root-Cause Detection

- Real-Time Companion-Computer Health Monitoring & Failsafe

## 时间线

时间线参照 https://developers.google.com/open-source/gsoc/timeline

## 如何提高被录用的机会

在做出录取学生的艰难决定时，我们会关注：

- Clear and detailed application explaining how you think the project could be done

- Relevant prior experience

- Experience contributing to ArduPilot or other open source projects

- Understanding of Git and/or GitHub

## SITL Model Generation from Flight Data

- Skills required: Python, C++ (ArduPilot/SITL), system identification
- Mentors: Nathaniel Mailhot
- Expected Size: 350h
- Level of Difficulty: Hard
- Expected Outcome: A toolchain that auto-builds or tunes SITL airframe models from real flight logs

该项目的目标是获取ArduPilot日志，估算SITL所需的关键动力学/传感器参数，然后输出更新后的模型+参数，以更好地匹配真实车辆。

## Multi-Drone Mesh Networking (MAVLink-aware)

- Skills required: Networking, C/C++, Linux, MAVLink

- Mentors: Nathaniel Mailhot

- Expected Size: 350h

- Level of Difficulty: Hard

- Expected Outcome: A practical mesh networking layer for multi-vehicle comms (telemetry + coordination)

该项目的目标是实现多台ArduPilot载具之间的弹性多跳链路，以便在直接链路中断时，遥测和指令能够通过群组路由。

##　ArduHumanoid (ArduPilot controlling a simple humanoid)

- Skills required: C++, control, servo systems, simulation (Gazebo/Ignition)

- Mentors: Nathaniel Mailhot

- Expected Size: 175h

- Level of Difficulty: Medium

- Expected Outcome: A minimal humanoid “vehicle type” running on ArduPilot with SITL support

该项目的目标是证明ArduPilot能够控制一个小型类人型关节框架（类似“伺服机器人”），配备基本控制界面和简单的模拟模型。

## AI-Assisted Log Diagnosis & Root-Cause Detection

- Skills required: Python, ML (classification + retrieval), ArduPilot logs/parameters

- Mentors: Nathaniel Mailhot

- Expected Size: 350h

- Level of Difficulty: Hard

- Expected Outcome: A model/service that flags likely root causes from logs and suggests fixes with confidence

该项目的目标是通过学习标记的日志段、已知的问题模式和参数状态，自动诊断常见故障和配置错误。它应输出可能的根本原因、建议的修复方法和置信度评分（并附有日志中相关证据的链接）。

## Real-Time Companion-Computer Health Monitoring & Failsafe
- Skills required: C/C++ or Python, MAVLink, Linux companion computers

- Mentors: Jaime Machuca

- Expected Size: 175h

- Level of Difficulty: Medium

- Expected Outcome: A standard MAVLink-based health reporting + failsafe mechanism for companion computers

该项目的目标是定义并实现一致的“伴随健康”报告（CPU/GPU负载、心跳、关键服务、看门狗），并将其与可配置的保护措施连接起来，使ArduPilot能够在伴随设备性能下降或失效时做出可预测的响应。
