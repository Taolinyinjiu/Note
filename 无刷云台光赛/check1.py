import cv2
import numpy as np
from simple_pid import PID
from gimbal_create_packet import create_packet
import time


class WhiteTargetAimSystem:
    def __init__(self):
        # 初始化摄像头
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        # 控制参数
        self.search_speed = 300  # 搜索转速（度/秒）
        self.aim_threshold = 15  # 瞄准阈值（像素）
        self.max_white_area = 0  # 最大目标面积记录

        # PID控制器
        self.pid_x = PID(0.4, 0.01, 0.1, setpoint=0, output_limits=(-1000, 1000))
        self.pid_y = PID(0.5, 0.01, 0.1, setpoint=0, output_limits=(-1000, 1000))

        # 白色检测参数（HSV范围）
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 30, 255])

        # 云台控制模板
        self.control_template = [
            {"go_zero": 1, "wk_mode": 2, "op_type": 0, "op_valu": 0},  # PITCH
            {"go_zero": 1, "wk_mode": 1, "op_type": 0, "op_valu": 0},  # ROLL
            {"go_zero": 1, "wk_mode": 2, "op_type": 0, "op_valu": 0}  # YAW
        ]
        # 绝对角度存储
        self.current_pitch = 0  # 绝对角度 Pitch（Y方向）
        self.current_yaw = 0  # 绝对角度 Yaw（X方向）
        # 系统状态
        self.is_tracking = False
        self.last_yaw = 0
        self.frame_center = (320, 240)
        self.running = True

    def detect_white_object(self, frame):
        """改进的白色物体检测"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_white, self.upper_white)

        # 形态学优化
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 查找轮廓并筛选
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # 按面积筛选前3个目标
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

        # 选择最接近画面中心的目标
        min_dist = float('inf')
        best_target = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 100:
                continue

            # 计算最小外接圆
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            dist = np.linalg.norm(np.array([x, y]) - self.frame_center)

            if dist < min_dist:
                min_dist = dist
                best_target = (int(x), int(y), int(radius), area)

        return best_target

    def send_gimbal_command(self, pitch=0, yaw=0):
        """发送云台控制指令"""
        control_data = [dict(d) for d in self.control_template]
        control_data[0]["op_valu"] = int(pitch)
        control_data[2]["op_valu"] = int(yaw)
        create_packet(data={'gbc_data': control_data})

    def search_pattern(self):
        """自动旋转搜索模式"""
        current_time = time.time()
        # 正弦扫描模式（避免机械冲击）
        scan_speed = self.search_speed * np.sin(current_time * 0.5)
        self.send_gimbal_command(yaw=scan_speed)

    def aiming_control(self, target_pos, frame):
        """瞄准控制（添加frame参数）"""
        x, y, r, area = target_pos
        error_x = x - self.frame_center[0]
        error_y = y - self.frame_center[1]

        # 动态调整PID参数
        self.pid_x.tunings = (0.4 * (area/100 ), 0.01, 0.1)
        self.pid_y.tunings = (0.5 * (area/100 ), 0.01, 0.1)

        adj_x = self.pid_x(error_x)

        adj_y = self.pid_y(error_y)
        # 计算新的绝对角度
        self.current_yaw += adj_x
        self.current_pitch += adj_y
        # 发送控制指令
        self.send_gimbal_command(pitch=self.current_pitch, yaw=self.current_yaw)

        # 在传入的frame上绘制锁定状态
        if abs(error_x) < self.aim_threshold and abs(error_y) < self.aim_threshold:
            cv2.putText(frame, "LOCKED", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return True
        return False

    def run(self):
        """主控制循环"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("视频流中断")
                break

            # 图像预处理
            frame = cv2.flip(frame, -1)
            h, w = frame.shape[:2]
            self.frame_center = (w // 2, h // 2)

            # 目标检测
            target = self.detect_white_object(frame)

            if target:
                x, y, r, area = target
                self.max_white_area = max(self.max_white_area, area)

                # 绘制检测结果
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.line(frame, (x, y), self.frame_center, (0, 0, 255), 2)
                cv2.putText(frame, f"Area: {area}", (x + r + 10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # 传入当前帧进行瞄准控制
                locked = self.aiming_control(target, frame)
                self.is_tracking = not locked
            else:
                # 目标丢失进入搜索模式
                if self.is_tracking:
                    self.search_pattern()
                self.is_tracking = False
                self.max_white_area = 0
                self.pid_x.reset()
                self.pid_y.reset()

            # 显示调试信息
            cv2.circle(frame, self.frame_center, 5, (255, 0, 0), -1)
            status_text = "SEARCHING" if not self.is_tracking else "TRACKING"
            cv2.putText(frame, status_text, (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("White Target Aiming", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        # 清理资源
        self.cap.release()
        cv2.destroyAllWindows()
        self.send_gimbal_command(0, 0)  # 云台归中


if __name__ == "__main__":
    aim_system = WhiteTargetAimSystem()
    try:
        aim_system.run()
    except KeyboardInterrupt:
        aim_system.send_gimbal_command(0, 0)
