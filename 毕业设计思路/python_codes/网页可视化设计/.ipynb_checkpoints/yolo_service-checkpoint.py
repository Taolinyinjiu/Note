import time
import cv2
import numpy as np
import base64
import requests
import threading
import random

def process_frame(frame):
    # 简单处理：在纯色图像上画一个随机颜色的圆
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    cv2.circle(frame, (center_x, center_y), 50, color, 5)
    return frame

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def send_processed_image(encoded_image, web_server_url='http://localhost:5000/receive_yolo_image'):
    try:
        response = requests.post(web_server_url, data={'image_data': encoded_image})
        response.raise_for_status()
        print(f"成功发送图像数据到 {web_server_url}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"发送图像数据失败: {e}")

def send_error_to_web(error_message, web_server_url='http://localhost:5000/receive_yolo_image'):
    try:
        response = requests.post(web_server_url, data={'error': error_message})
        response.raise_for_status()
        print(f"成功发送错误信息到 {web_server_url}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"发送错误信息失败: {e}")

def generate_solid_color_image(width=640, height=480):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image

def yolo_detection_loop():
    while True:
        # 生成纯色图像
        solid_image = generate_solid_color_image()
        # 进行“处理”
        processed_image = process_frame(solid_image)
        # 编码并发送
        encoded_image = encode_frame_to_base64(processed_image)
        send_processed_image(encoded_image)
        time.sleep(2) # 每隔 2 秒发送一张图像

if __name__ == "__main__":
    print("YOLO 检测服务启动 (生成纯色图像)")
    yolo_detection_thread = threading.Thread(target=yolo_detection_loop)
    yolo_detection_thread.daemon = True
    yolo_detection_thread.start()

    while True:
        time.sleep(1)