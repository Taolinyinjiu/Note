model = YOLO("F:/GitHub/Note/毕业设计思路/python_codes/yolo_model_weights/best.pt")  # 或者你的模型路径
cap = cv2.VideoCapture(0)
# --- 畸变校正 ---
frame = cv2.undistort(frame, intrinsic_matrix, distortion_coefficients)
# --- YOLO 检测 ---
results = model(frame)
for i, r in enumerate(results):
    #处理每个检测到的对象

for class_name, boxes in class_boxes.items():
    # 计算每个物体的矩形尺寸




# 框宽高（像素）
pixel_width = x2 - x1
pixel_height = y2 - y1

# 实际宽高（mm）
real_width = (pixel_width * Z) / fx
real_height = (pixel_height * Z) / fy