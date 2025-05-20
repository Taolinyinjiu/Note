from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key!'  # 替换为你的密钥
socketio = SocketIO(app, cors_allowed_origins="*", transport='websocket') # 尝试强制使用 WebSocket

yolo_image_data = None
svg_content_data = None
video_path_data = None
yolo_error_data = None

@app.route('/')
def index():
    return render_template('index_websocket.html',
                           svg_content_data=svg_content_data,
                           video_path_data=video_path_data,
                           yolo_error_data=yolo_error_data)

@app.route('/receive_yolo_image', methods=['POST'])
def receive_yolo_image():
    global yolo_image_data
    global yolo_error_data
    if 'image_data' in request.form:
        yolo_image_data = request.form['image_data']
        socketio.emit('yolo_image', {'image_data': yolo_image_data}, namespace='/yolo')
        yolo_error_data = None
        return {'status': 'success', 'message': 'YOLO image received'}
    elif 'error' in request.form:
        yolo_error_data = request.form['error']
        socketio.emit('yolo_error', {'error': yolo_error_data}, namespace='/yolo')
        yolo_image_data = None
        return {'status': 'error', 'message': 'YOLO processing error'}
    else:
        return {'status': 'error', 'message': 'No image_data or error received'}, 400

@app.route('/receive_svg', methods=['POST'])
def receive_svg():
    global svg_content_data
    if 'svg_data' in request.form:
        svg_content_data = request.form['svg_data']
        return {'status': 'success', 'message': 'SVG data received'}
    else:
        return {'status': 'error', 'message': 'No svg_data received'}, 400

@app.route('/receive_video_path', methods=['POST'])
def receive_video_path():
    global video_path_data
    if 'video_path' in request.form:
        video_path_data = request.form['video_path']
        return {'status': 'success', 'message': 'Video path received'}
    else:
        return {'status': 'error', 'message': 'No video_path received'}, 400

@socketio.on('connect', namespace='/yolo')
def connect_yolo():
    print(f'Client connected to /yolo namespace (SID: {request.sid})')
    global yolo_image_data
    global yolo_error_data
    if yolo_image_data:
        emit('yolo_image', {'image_data': yolo_image_data})
    elif yolo_error_data:
        emit('yolo_error', {'error': yolo_error_data})

@socketio.on('disconnect', namespace='/yolo')
def disconnect_yolo():
    print(f'Client disconnected from /yolo namespace (SID: {request.sid})')

if __name__ == '__main__':
    socketio.run(app, debug=True)