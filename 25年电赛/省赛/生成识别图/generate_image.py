from PIL import Image, ImageDraw, ImageFont
import random
import os

def is_overlap(rect1, rect2, margin=2):
    # 判断两个矩形是否重叠，margin为像素级间隔
    l1, t1, r1, b1 = rect1
    l2, t2, r2, b2 = rect2
    return not (r1 + margin <= l2 or r2 + margin <= l1 or b1 + margin <= t2 or b2 + margin <= t1)

def create_a4_image_with_numbered_squares(
    output_path="a4_numbered_squares.png",
    border_width_cm=2,
    num_squares=None,
    min_side_cm=6,
    max_side_cm=12,
    dpi=300
):
    """
    生成一张A4大小的图片，包含以下元素：
    1. 四边有指定宽度的黑色边框。
    2. 图片上随机分布多个指定范围内边长的实心黑色正方形，正方形之间保持一定间隔以避免重叠。
    3. 每个正方形内有居中的白色数字，表示正方形的编号。

    参数:
    output_path (str): 生成图片文件的保存路径和文件名。
    border_width_cm (float): 黑色边框的宽度，单位为厘米。
    num_squares (int): 要生成的正方形数量。如果为None，则随机生成2到4个正方形。
    min_side_cm (float): 正方形的最小边长，单位为厘米。
    max_side_cm (float): 正方形的最大边长，单位为厘米。
    dpi (int): 图片的每英寸点数，影响图片的分辨率和打印质量。
    """
    # A4纸张标准尺寸（毫米）
    a4_width_mm = 210
    a4_height_mm = 297
    mm_to_inch = 25.4
    cm_to_inch = 2.54

    if num_squares is None:
        num_squares = random.randint(2, 4)

    # 1. 计算图片尺寸（像素）
    width_pixels = int((a4_width_mm / mm_to_inch) * dpi)
    height_pixels = int((a4_height_mm / mm_to_inch) * dpi)

    print(f"图片将被创建为 {width_pixels}x{height_pixels} 像素 (基于A4尺寸和 {dpi} DPI)")

    # 2. 创建白色背景的图片
    img = Image.new('RGB', (width_pixels, height_pixels), color='white')
    draw = ImageDraw.Draw(img)

    # 3. 绘制黑色边框
    border_width_pixels = int((border_width_cm / cm_to_inch) * dpi)
    if border_width_pixels < 1:
        border_width_pixels = 1

    print(f"边框宽度: {border_width_cm} 厘米，转换为 {border_width_pixels} 像素")

    draw.rectangle(
        [(0, 0), (width_pixels - 1, height_pixels - 1)],
        outline="black",
        width=border_width_pixels
    )

    # 让正方形离边框和彼此之间都更远，比如至少0.5厘米
    border_margin_cm = 0.8
    border_margin_px = border_width_pixels + int((border_margin_cm / cm_to_inch) * dpi)
    min_square_margin_cm = 0.5
    min_square_margin_px = int((min_square_margin_cm / cm_to_inch) * dpi)

    squares = []
    max_attempts = 1000

    # 4. 随机生成多个实心黑色正方形
    for i in range(num_squares):
        for attempt in range(max_attempts):
            side_cm = random.uniform(min_side_cm, max_side_cm)
            side_px = (side_cm / cm_to_inch) * dpi

            # 随机生成左上角坐标，保证不靠近边框
            left = random.uniform(border_margin_px, width_pixels - border_margin_px - side_px)
            top = random.uniform(border_margin_px, height_pixels - border_margin_px - side_px)
            right = left + side_px
            bottom = top + side_px

            new_rect = (left, top, right, bottom)
            # 检查与已有正方形是否重叠，且间隔不少于min_square_margin_px
            if all(not is_overlap(new_rect, rect, margin=min_square_margin_px) for rect in squares):
                squares.append(new_rect)
                draw.rectangle([left, top, right, bottom], fill="black")

                # 字体大小为正方形边长的约一半
                font_size = int(side_px * 0.5)

                # 尝试加载Times New Roman字体
                font_path_candidates = [
                    "C:/Windows/Fonts/times.ttf",
                    "C:/Windows/Fonts/timesnewroman.ttf",
                    "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
                    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
                ]
                font_path = None
                for path in font_path_candidates:
                    if os.path.exists(path):
                        font_path = path
                        break

                if font_path:
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()

                text = str(i + 1)
                # 获取文本宽高（兼容新版Pillow）
                try:
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    text_width, text_height = font.getsize(text)
                text_x = left + (side_px - text_width) / 2
                text_y = top + (side_px - text_height) / 2

                draw.text((text_x, text_y), text, fill="white", font=font)
                print(f"正方形{i+1}: 左上角=({left/cm_to_inch*dpi:.1f}cm, {top/cm_to_inch*dpi:.1f}cm), 边长={side_cm:.2f}cm, 编号={text}")
                break
        else:
            print(f"第{i+1}个正方形在{max_attempts}次尝试后仍未找到合适位置，跳过。")

    # 5. 保存图片
    img.save(output_path, dpi=(dpi, dpi))
    print(f"\n图片已成功保存至：{output_path}")

# --- 主程序入口 ---
if __name__ == "__main__":
    create_a4_image_with_numbered_squares(
        output_path="a4_numbered_squares-4.png",
        border_width_cm=2,
        num_squares=None,  # 随机2~4个
        min_side_cm=6,
        max_side_cm=11,
        dpi=300
    )