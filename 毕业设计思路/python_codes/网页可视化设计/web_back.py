from flask import Flask, render_template, request, jsonify
import base64

app = Flask(__name__)

# 使用全局变量存储接收到的数据 (简单方法，生产环境可能需要更完善的状态管理)
yolo_image_data = None
svg_content_data = None
video_path_data = None
yolo_error_data = None

@app.route('/')
def index():
    return render_template('index_dynamic.html',
                           yolo_image_data=yolo_image_data,
                           svg_content_data=svg_content_data,
                           video_path_data=video_path_data,
                           yolo_error_data=yolo_error_data)

@app.route('/receive_yolo_image', methods=['POST'])
def receive_yolo_image():
    global yolo_image_data
    global yolo_error_data
    if 'image_data' in request.form:
        yolo_image_data = request.form['image_data']
        yolo_error_data = None
        return jsonify({'status': 'success', 'message': 'YOLO image received'})
    elif 'error' in request.form:
        yolo_error_data = request.form['error']
        yolo_image_data = None
        return jsonify({'status': 'error', 'message': 'YOLO processing error'})
    else:
        return jsonify({'status': 'error', 'message': 'No image_data or error received'}), 400

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
    app.run(debug=True)