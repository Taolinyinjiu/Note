from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import queue
import time
from flask_cors import CORS  # 导入 CORS (如果需要)
from collections import defaultdict
import os

# --- 配置 ---
frame_queue = queue.Queue(maxsize=30)
yolo_error_data = None
svg_content_data = None
video_path_data = None
yolo_results_data = []  # 初始化为空列表
app = Flask(__name__)
CORS(app)  # 允许跨域请求 (如果需要)

# 标定参数
# OptiCalib标定结果(200w摄像头)
fx = 1462.933715
fy = 1472.343506
cx = 969.398521
cy = 545.531149 

intrinsic_matrix = np.array([[fx, 0, cx],
                             [0, fy, cy],
                             [0, 0, 1]], dtype=np.float32)

# 替换为你的实际畸变系数 (k1, k2, p1, p2, k3)(200w摄像头)
k1 =  0.057745
k2 = -0.117250
p1 = -0.001262
p2 = 0.001061
k3 = 0.0

# 设置分辨率
desired_width = 1920
desired_height = 1080

distortion_coefficients = np.array([k1, k2, p1, p2, k3], dtype=np.float32)

is_paused = False  # 新增变量，用于控制 YOLO 暂停和恢复
last_frame = None  # 全局变量，保存最后一帧

# --- YOLO 线程 函数 ---
def yolo_detection_thread():
    """YOLO 检测线程"""
    global yolo_error_data, yolo_results_data, is_paused, last_frame
    try:
        model = YOLO("F:/GitHub/Note/毕业设计思路/python_codes/yolo_model_weights/best.pt")  # 或者你的模型路径
        cap = cv2.VideoCapture(0)
        # 设置分辨率
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            yolo_error_data = "无法打开摄像头"
            return

        while True:
            if is_paused:
                time.sleep(0.1)
                continue

            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                yolo_error_data = "无法读取摄像头帧"
                break
            # --- 畸变校正 ---
            frame = cv2.undistort(frame, intrinsic_matrix, distortion_coefficients)
            # --- YOLO 检测 ---
            results = model(frame)
            # ...后续处理...

            # --- 处理 YOLO 结果 ---
            detailed_results = []
            class_boxes = defaultdict(list)  # 存储每个类别的所有框
            for i, r in enumerate(results):
                boxes = r.boxes
                for j, box in enumerate(boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = box.conf[0]
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id] if model.names and class_id in model.names else f"Class {class_id}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 在帧上绘制检测框
                    label = f"{class_name} [{j}]"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    width = x2 - x1
                    height = y2 - y1
                    detailed_results.append({
                        "class_name": class_name,
                        "index": j,  # 同一类别内的索引
                        "box_size": {"width": width, "height": height},
                        "position": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},  # 添加位置信息
                        "confidence": float(confidence),
                        "frame_index": i  # 添加帧索引
                    })
                    class_boxes[class_name].append((x1, y1, x2, y2))

            # 计算每个类别的总矩形尺寸
            class_total_sizes = {}
            for class_name, boxes in class_boxes.items():
                if boxes:
                    min_x1 = min(box[0] for box in boxes)
                    min_y1 = min(box[1] for box in boxes)
                    max_x2 = max(box[2] for box in boxes)
                    max_y2 = max(box[3] for box in boxes)
                    total_width = max_x2 - min_x1
                    total_height = max_y2 - min_y1
                    class_total_sizes[class_name] = {"width": total_width, "height": total_height}

            yolo_results_data = {
                "objects": detailed_results,
                "class_totals": class_total_sizes
            }  # 更新全局变量

            try:
                # 将处理后的帧放入队列
                frame_queue.put(frame.copy(), timeout=1.0)
                last_frame = frame.copy()  # 保存最后一帧

                # 每次检测后都保存静态帧
                cv2.imwrite(os.path.join('static', 'last_frame.jpg'), last_frame)
            except queue.Full:
                print("YOLO: Queue is full, skipping frame.")

    except Exception as e:
        print(f"YOLO 线程错误: {e}")
        yolo_error_data = f"YOLO 处理错误: {e}"

    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("YOLO: Camera released and windows destroyed.")

def generate_frames():
    """生成图像帧给 Flask (以 JPEG 流形式)"""
    while True:
        try:
            frame = frame_queue.get(timeout=1.0)
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                print("Error encoding frame to JPEG")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 'Error: 帧编码错误\r\n'.encode('utf-8'))
        except queue.Empty:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\nNo frame available\r\n')
        except Exception as e:
            print(f"帧生成器错误: {e}")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + f'Error: 帧生成错误: {e}\r\n'.encode('utf-8'))


@app.route('/')
def index():
    """使用 index_async.html 模板"""
    return render_template('index_async.html',
                           yolo_error=yolo_error_data,
                           svg_content=svg_content_data,
                           video_file_path=video_path_data or '')

# @app.route('/')
# def index():
#     """使用 index_async.html 模板"""
#     return render_template('index_async.html',
#                            yolo_error=yolo_error_data,
#                            svg_content=svg_content_data,
#                            video_file_path=video_path_data or '',
#                            yolo_results=yolo_results_data.get('objects', []) # 传递检测到的物体列表
#                            # 或者传递整个 yolo_results_data 字典
#                            # yolo_results=yolo_results_data
                        #    )

@app.route('/yolo_feed')
def yolo_feed():
    """Flask 路由，返回图像流"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/receive_svg', methods=['POST'])
def receive_svg():
    global svg_content_data
    if 'svg_data' in request.form:
        svg_content_data = request.form['svg_data']
        return jsonify({'status': 'success', 'message': 'SVG data received'})
    else:
        return jsonify({'status': 'error', 'message': 'No svg_data received'}), 400


@app.route('/receive_video_path', methods=['POST'])
def receive_video_path():
    global video_path_data
    if 'video_path' in request.form:
        video_path_data = request.form['video_path']
        return jsonify({'status': 'success', 'message': 'Video path received'})
    else:
        return jsonify({'status': 'error', 'message': 'No video_path received'}), 400

# 新增路由，用于提供 YOLO 结果
@app.route('/get_yolo_results')
def get_yolo_results():
    global yolo_results_data
    print("YOLO Results Data:", yolo_results_data)  # 添加这行来打印数据
    return jsonify({'yolo_results': yolo_results_data})

@app.route('/pause_yolo', methods=['POST'])
def pause_yolo():
    global is_paused
    is_paused = True
    return jsonify({'status': 'paused'})

@app.route('/resume_yolo', methods=['POST'])
def resume_yolo():
    global is_paused
    is_paused = False
    return jsonify({'status': 'resumed'})

if __name__ == '__main__':
    # 启动 YOLO 线程
    yolo_thread = threading.Thread(target=yolo_detection_thread)
    yolo_thread.daemon = True
    yolo_thread.start()

    # 启动 Flask 应用
    app.run(debug=True, use_reloader=False, host='0.0.0.0')