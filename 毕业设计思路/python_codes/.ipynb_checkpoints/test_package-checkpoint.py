import cv2
import numpy as np
import svgwrite

def draw_circle(dwg, center_x, center_y, radius, color='blue'):
    # 确保坐标是 Python 的数字类型
    dwg.add(dwg.circle(center=(float(center_x), float(center_y)), r=float(radius), fill='none', stroke=color, stroke_width=1))

def generate_svg_from_corners(corners, output_filename="detected_box.svg", img_width=None, img_height=None):
    if corners is None or len(corners) == 0:
        print("未检测到角点。")
        return

    if img_width is None or img_height is None:
        min_x = min(c[0][0] for c in corners)
        max_x = max(c[0][0] for c in corners)
        min_y = min(c[0][1] for c in corners)
        max_y = max(c[0][1] for c in corners)
        # 确保画布尺寸是正数
        canvas_width = max(1, max_x - min_x + 20)
        canvas_height = max(1, max_y - min_y + 20)
        translate_x = -min_x + 10
        translate_y = -min_y + 10
    else:
        canvas_width = img_width
        canvas_height = img_height
        translate_x = 0
        translate_y = 0

    dwg = svgwrite.Drawing(output_filename, size=(canvas_width, canvas_height)) # 使用 size 参数

    for corner in corners:
        x, y = corner.ravel()
        # 将 NumPy float 转换为 Python float (或 int)
        draw_circle(dwg, float(x + translate_x), float(y + translate_y), 5, 'red')

    dwg.save()
    print(f"检测到的角点已保存到 {output_filename}")

if True:
    image_path = "package.jpeg"  # 替换为您的文件路径
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法加载图像: {image_path}")
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        max_corners = 200
        quality_level = 0.01
        min_distance = 10
        block_size = 7

        corners = cv2.goodFeaturesToTrack(gray,
                                          maxCorners=max_corners,
                                          qualityLevel=quality_level,
                                          minDistance=min_distance,
                                          blockSize=block_size)

        if corners is not None:
            print(f"检测到 {len(corners)} 个角点。")
            generate_svg_from_corners(corners, output_filename="detected_box_corners.svg", img_width=img.shape[1], img_height=img.shape[0])

            # 在原始图像上绘制角点
            img_with_corners = img.copy()
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(img_with_corners, (int(x), int(y)), 5, (0, 0, 255), -1)

            # 显示带有角点的图像
            cv2.imshow('Detected Corners on Original Image', img_with_corners)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # 保存带有角点的图像
            output_image_path = "detected_box_on_image.png"
            cv2.imwrite(output_image_path, img_with_corners)
            print(f"带有角点的图像已保存为 {output_image_path}")

        else:
            print("未检测到角点。请尝试调整检测参数。")