# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import rospy
# from nav_msgs.msg import Path
# from geometry_msgs.msg import PoseStamped

# class PathCompareNode:
#     def __init__(self):
#         rospy.init_node('path_compare_node', anonymous=True)

#         # --- 参数配置 ---
#         # 1. 动捕话题 (对应你提供的 PoseStamped 格式)
#         self.mocap_topic = rospy.get_param('~mocap_topic', '/vrpn_client_node_1/uav1/pose')
#         # 2. 需要对比的算法 Path 话题 (已经在累计数据的话题)
#         self.algo_path_topic = rospy.get_param('~algo_path_topic', '/baton/stereo4/odom_path')
        
#         # --- 状态变量 ---
#         self.start_time = None  # 用于记录“数据包录制开始”或“节点启动”的时间

#         # --- 发布者 ---
#         # 发布动捕转换后的实时单点 Path
#         self.mocap_path_pub = rospy.Publisher('/mocap_path_stream', Path, queue_size=10)
#         # 发布清理后的对比 Path
#         self.clean_path_pub = rospy.Publisher('/algo_path_clean', Path, queue_size=10)

#         # --- 订阅者 ---
#         # 订阅动捕数据 (PoseStamped)
#         self.mocap_sub = rospy.Subscriber(self.mocap_topic, PoseStamped, self.mocap_callback)
#         # 订阅需要对比的路径 (Path)
#         self.algo_sub = rospy.Subscriber(self.algo_path_topic, Path, self.algo_path_callback)

#         rospy.loginfo("路径对比处理节点已启动")
#         rospy.loginfo("动捕话题: %s", self.mocap_topic)
#         rospy.loginfo("对比路径话题: %s", self.algo_path_topic)

#     def mocap_callback(self, msg):
#         """
#         处理动捕数据：将 PoseStamped 转换为实时单点 Path
#         """
#         # 记录第一帧动捕数据的时间作为“基准开始时间”
#         if self.start_time is None:
#             self.start_time = msg.header.stamp

#         path_msg = Path()
#         path_msg.header = msg.header
#         path_msg.poses.append(msg) # 直接把收到的 PoseStamped 塞进去
#         self.mocap_path_pub.publish(path_msg)

#     def algo_path_callback(self, msg):
#         """
#         处理对比路径：清除历史积压点，仅保留节点启动后的数据
#         """
#         if self.start_time is None:
#             # 如果动捕还没开始，说明实验还没正式开始，不处理对比路径
#             return

#         clean_path = Path()
#         clean_path.header = msg.header

#         # 核心逻辑：遍历收到的 Path 消息中的所有点
#         # 只保留时间戳晚于我们定义的 start_time 的点
#         new_poses = [p for p in msg.poses if p.header.stamp >= self.start_time]

#         if new_poses:
#             clean_path.poses = new_poses
#             self.clean_path_pub.publish(clean_path)

# if __name__ == '__main__':
#     try:
#         node = PathCompareNode()
#         rospy.spin()
#     except rospy.ROSInterruptException:
#         pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class FoxgloveVisualizerNode:
    def __init__(self):
        rospy.init_node('foxglove_path_sync_node', anonymous=True)

        # 获取话题配置
        self.mocap_topic = rospy.get_param('~mocap_topic', '/vrpn_client_node_1/uav1/pose')
        self.algo_topic = rospy.get_param('~algo_path_topic', '/baton/stereo4/odom_path')
        
        # 状态：记录实验开始时刻
        self.experiment_start_time = None

        # 发布者
        self.mocap_pub = rospy.Publisher('/foxglove/mocap_path', Path, queue_size=10)
        self.algo_pub = rospy.Publisher('/foxglove/algo_path', Path, queue_size=10)

        # 订阅者
        rospy.Subscriber(self.mocap_topic, PoseStamped, self.mocap_cb)
        rospy.Subscriber(self.algo_topic, Path, self.algo_cb)

    def mocap_cb(self, msg):
        # 以第一帧动捕数据作为“实验开始”的信号
        if self.experiment_start_time is None:
            self.experiment_start_time = msg.header.stamp
            rospy.loginfo("检测到动捕数据，实验对齐开始！")

        # 转换并发布动捕路径（单点流）
        m_path = Path()
        m_path.header = msg.header
        m_path.header.frame_id = "world" # 统一坐标系名称
        m_path.poses.append(msg)
        self.mocap_pub.publish(m_path)

    def algo_cb(self, msg):
        if self.experiment_start_time is None:
            return

        # 核心过滤：只保留时间戳大于实验开始时间的点
        clean_path = Path()
        clean_path.header = msg.header
        clean_path.header.frame_id = "world"
        clean_path.poses = [p for p in msg.poses if p.header.stamp >= self.experiment_start_time]

        if clean_path.poses:
            self.algo_pub.publish(clean_path)

if __name__ == '__main__':
    node = FoxgloveVisualizerNode()
    rospy.spin()