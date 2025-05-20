import time
import cv2
import numpy as np
import base64
import threading
import random
import socketio

sio = socketio.Client()
connected = False
reconnect_delay = 5  # 秒

def process_frame(frame):
    # 这里替换为你的实际 YOLO 模型处理代码
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    cv2.circle(frame, (center_x, center_y), 50, color, 5)
    return frame

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def generate_solid_color_image(width=640, height=480):
    color = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], dtype=np.uint8)
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image

def send_processed_image(encoded_image):
    global connected
    if connected:
        try:
            sio.emit('yolo_image', {'image_data': encoded_image}, namespace='/yolo')
            print("成功发送图像数据 (WebSocket)")
        except Exception as e:
            print(f"发送图像数据失败 (WebSocket 发送时错误): {e}")
            connected = False
            threading.Thread(target=reconnect_with_delay).start()
    else:
        print("尚未连接到 WebSocket 服务器，无法发送图像数据 (WebSocket 未连接)")

def send_error_to_web(error_message):
    global connected
    if connected:
        try:
            sio.emit('yolo_error', {'error': error_message}, namespace='/yolo')
            print(f"成功发送错误信息: {error_message}")
        except Exception as e:
            print(f"发送错误信息失败 (WebSocket 发送时错误): {e}")
            connected = False
            threading.Thread(target=reconnect_with_delay).start()
    else:
        print("尚未连接到 WebSocket 服务器，无法发送错误信息 (WebSocket 未连接)")

def yolo_detection_loop():
    while not connected:  # 等待连接成功
        time.sleep(0.1)
    time.sleep(2)  # 确保连接稳定
    while True:
        solid_image = generate_solid_color_image()
        processed_image = process_frame(solid_image)
        encoded_image = encode_frame_to_base64(processed_image)
        send_processed_image(encoded_image)
        time.sleep(0.1)

def connect_handler():
    global connected
    connected = True
    print(f'YOLO service connected to WebSocket server (SID: {sio.sid})')

def disconnect_handler():
    global connected
    connected = False
    print('YOLO service disconnected from WebSocket server')
    threading.Thread(target=reconnect_with_delay).start()

def reconnect_with_delay():
    global connected
    time.sleep(reconnect_delay)
    try:
        sio.connect('http://localhost:5000', transports=['websocket'])
    except socketio.exceptions.ConnectionError as e:
        print(f"重新连接 WebSocket 服务器失败: {e}")
        threading.Thread(target=reconnect_with_delay).start() # 继续尝试重新连接

if __name__ == "__main__":
    sio.on('connect', connect_handler)
    sio.on('disconnect', disconnect_handler)

    try:
        sio.connect('http://localhost:5000', transports=['websocket'])
    except socketio.exceptions.ConnectionError as e:
        print(f"连接 WebSocket 服务器失败: {e}")
        exit()

    print("YOLO 检测服务启动 (尝试使用 WebSocket)")
    yolo_detection_thread = threading.Thread(target=yolo_detection_loop)
    yolo_detection_thread.daemon = True
    yolo_detection_thread.start()

    while True:
        time.sleep(1)