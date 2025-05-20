import cv2
from ultralytics import YOLO
import threading
import queue
import time

# --- 配置 ---
IMAGE_WIDTH = 640  # 根据你的摄像头或需求调整
IMAGE_HEIGHT = 480
# IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT * 3  # RGB (如果需要，但通常 cv2图像已经是numpy数组)

# --- 队列 ---
frame_queue = queue.Queue(maxsize=30)  # 限制队列大小

# --- YOLO 线程 函数 ---
def yolo_detection_thread():
    """YOLO 检测线程"""
    # Load the YOLO model (do this *inside* the thread if possible, for thread safety)
    model = YOLO("yolov8n.pt")  # 或者你的模型路径

    # Open the default USB camera (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return  # 线程结束

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break  # 循环结束

        # Perform inference on the frame
        results = model(frame)

        # Process the results and draw bounding boxes
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                class_id = int(box.cls[0])
                class_name = model.names[class_id] if model.names and class_id in model.names else f"Class {class_id}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        try:
            # Put the processed frame into the queue
            frame_queue.put(frame.copy(), timeout=1.0)  # 放入 *副本*
            # print("YOLO: Frame put in queue.") # 调试信息
        except queue.Full:
            print("YOLO: Queue is full, skipping frame.")

        # Break the loop if the queue is full for too long (optional, for safety)
        # if frame_queue.full():
        #     print("YOLO: Queue consistently full, exiting YOLO thread.")
        #     break

    # Release the camera and destroy all windows (do this *inside* the thread)
    cap.release()
    cv2.destroyAllWindows()
    print("YOLO: Camera released and windows destroyed.") # 调试信息


# --- Flask 应用 (在主线程中) ---
from flask import Flask, Response, render_template

app = Flask(__name__)

def generate_frames():
    """生成图像帧给 Flask"""
    while True:
        try:
            frame = frame_queue.get(timeout=1.0)  # Get frame from queue
            # Convert frame to JPEG and yield it
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                print("Error encoding frame to JPEG")

        except queue.Empty:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\nNo frame available\r\n')
        time.sleep(0.05)  # 控制帧率 (可以调整)

@app.route('/yolo_feed')
def yolo_feed():
    """Flask 路由，返回图像流"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')  # 确保你有一个简单的 index.html

if __name__ == '__main__':
    # --- 启动YOLO线程 ---
    yolo_thread = threading.Thread(target=yolo_detection_thread)
    yolo_thread.daemon = True  # 设为守护线程，主线程退出时自动退出
    yolo_thread.start()

    # --- 启动 Flask 应用 ---
    app.run(debug=True, use_reloader=False, host='0.0.0.0')  # 禁用 reloader, 绑定到所有接口