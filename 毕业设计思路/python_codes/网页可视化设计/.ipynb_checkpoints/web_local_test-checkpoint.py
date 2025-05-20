# from flask import Flask, render_template, request, jsonify, Response
# import cv2
# from ultralytics import YOLO
# import threading
# import queue
# import time

# app = Flask(__name__)

# # --- 配置 ---
# IMAGE_WIDTH = 640
# IMAGE_HEIGHT = 480
# frame_queue = queue.Queue(maxsize=30)
# yolo_error_data = None
# svg_content_data = None
# video_path_data = None

# def yolo_detection_thread():
#     """YOLO 检测线程"""
#     global yolo_error_data
#     try:
#         model = YOLO("F:/GitHub/Note/毕业设计思路/python_codes/yolo_model_weights/best.pt")  # 或者你的模型路径
#         cap = cv2.VideoCapture(0)

#         if not cap.isOpened():
#             print("Error: Could not open camera.")
            
#             yolo_error_data = "无法打开摄像头"
#             return

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: Could not read frame.")
#                 yolo_error_data = "无法读取摄像头帧"
#                 break

#             results = model(frame)
#             for r in results:
#                 boxes = r.boxes
#                 for box in boxes:
#                     x1, y1, x2, y2 = map(int, box.xyxy[0])
#                     confidence = box.conf[0]
#                     class_id = int(box.cls[0])
#                     class_name = model.names[class_id] if model.names and class_id in model.names else f"Class {class_id}"
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     label = f"{class_name}: {confidence:.2f}"
#                     cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             try:
#                 frame_queue.put(frame.copy(), timeout=1.0)
#             except queue.Full:
#                 print("YOLO: Queue is full, skipping frame.")

#     except Exception as e:
#         print(f"YOLO 线程错误: {e}")
#         yolo_error_data = f"YOLO 处理错误: {e}"

#     finally:
#         if 'cap' in locals() and cap.isOpened():
#             cap.release()
#         cv2.destroyAllWindows()
#         print("YOLO: Camera released and windows destroyed.")

# def generate_frames():
#     """生成图像帧给 Flask"""
#     while True:
#         try:
#             frame = frame_queue.get(timeout=1.0)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if ret:
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#             else:
#                 print("Error encoding frame to JPEG")
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + 'Error: 帧编码错误\r\n'.encode('utf-8'))
#         except queue.Empty:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\nNo frame available\r\n')
#         except Exception as e:
#             print(f"帧生成器错误: {e}")
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + f'Error: 帧生成错误: {e}\r\n'.encode('utf-8'))

# @app.route('/')
# def index():
#     """使用 index_async.html 模板"""
#     return render_template('index_async.html',
#                            yolo_error=yolo_error_data,
#                            svg_content=svg_content_data,
#                            video_file_path=video_path_data)

# @app.route('/yolo_feed')
# def yolo_feed():
#     """Flask 路由，返回图像流"""
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/receive_svg', methods=['POST'])
# def receive_svg():
#     global svg_content_data
#     if 'svg_data' in request.form:
#         svg_content_data = request.form['svg_data']
#         return jsonify({'status': 'success', 'message': 'SVG data received'})
#     else:
#         return jsonify({'status': 'error', 'message': 'No svg_data received'}), 400

# @app.route('/receive_video_path', methods=['POST'])
# def receive_video_path():
#     global video_path_data
#     if 'video_path' in request.form:
#         video_path_data = request.form['video_path']
#         return jsonify({'status': 'success', 'message': 'Video path received'})
#     else:
#         return jsonify({'status': 'error', 'message': 'No video_path received'}), 400

# if __name__ == '__main__':
#     # 启动 YOLO 线程
#     yolo_thread = threading.Thread(target=yolo_detection_thread)
#     yolo_thread.daemon = True
#     yolo_thread.start()

#     # 启动 Flask 应用
#     app.run(debug=True, use_reloader=False, host='0.0.0.0')


from flask import Flask, render_template, request, jsonify, Response
import cv2
from ultralytics import YOLO
import threading
import queue
import time
import base64  # 导入 base64 库

app = Flask(__name__)

# --- 配置 ---
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
frame_queue = queue.Queue(maxsize=30)
yolo_error_data = None
svg_content_data = None
video_path_data = None

def yolo_detection_thread():
    """YOLO 检测线程"""
    global yolo_error_data
    try:
        model = YOLO("F:/GitHub/Note/毕业设计思路/python_codes/yolo_model_weights/best.pt")  # 或者你的模型路径
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            yolo_error_data = "无法打开摄像头"
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                yolo_error_data = "无法读取摄像头帧"
                break

            results = model(frame)
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
                # 将处理后的帧放入队列
                frame_queue.put(frame.copy(), timeout=1.0)
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
                           video_path=video_path_data or '')

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

if __name__ == '__main__':
    # 启动 YOLO 线程
    yolo_thread = threading.Thread(target=yolo_detection_thread)
    yolo_thread.daemon = True
    yolo_thread.start()

    # 启动 Flask 应用
    app.run(debug=True, use_reloader=False, host='0.0.0.0')