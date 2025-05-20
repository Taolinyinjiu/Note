from flask import Flask, render_template
import cv2
import numpy as np
import base64

app = Flask(__name__)

# 假设你有一个函数 process_image_with_yolo(image_path) 返回处理后的 NumPy 数组
def process_image_with_yolo(image_path):
    # 这里是你的 OpenCV YOLO 模型处理代码
    # 示例：创建一个简单的蓝色图像
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = [255, 0, 0]
    return img

def encode_image_to_base64(img_np):
    _, buffer = cv2.imencode('.png', img_np)
    return base64.b64encode(buffer).decode('utf-8')

def read_svg_file(svg_path):
    with open(svg_path, 'r') as f:
        return f.read()

@app.route('/')
def index():
    # 处理 YOLO 图像
    yolo_image_path = 'path/to/your/input_image.jpg'  # 替换为你的输入图像路径
    processed_image = process_image_with_yolo(yolo_image_path)
    yolo_image_base64 = encode_image_to_base64(processed_image)

    # 读取 SVG 文件
    svg_file_path = 'static/your_svg_file.svg'  # SVG 文件放在 static 文件夹中
    svg_content = read_svg_file(svg_file_path)

    # 视频文件路径 (假设放在 static 文件夹中)
    video_file_path = 'static/your_video.mp4'

    return render_template('index.html',
                           yolo_image_base64=yolo_image_base64,
                           svg_content=svg_content,
                           video_file_path=video_file_path)

if __name__ == '__main__':
    app.run(debug=True)