import os
from PIL import Image, ImageGrab, ImageOps
import pytesseract

def preprocess_image(png_path):
    img = Image.open(png_path).convert("RGBA")
    white_bg = Image.new("RGBA", img.size, "WHITE")
    white_bg.paste(img, (0, 0), img)
    white_bg = white_bg.convert("RGB")

    # 反色处理
    white_bg = ImageOps.invert(white_bg)

    return white_bg

def remove_vertical_white_pixels(img):
    pixels = img.load()
    width, height = img.size

    for x in range(width - 1, -1, -1):  # 从右到左扫描
        y = 0
        while y < height - 1:
            if pixels[x, y] == (255, 255, 255) and pixels[x, y + 1] == (255, 255, 255):
                # 如果连续两个像素是白色，且没有第三个连续白色像素
                if y + 2 >= height or pixels[x, y + 2] != (255, 255, 255):
                    # 将符合条件的像素块设置为黑色
                    pixels[x, y - 2] = (0, 0, 0)
                    pixels[x, y - 1] = (0, 0, 0)
                    pixels[x, y] = (0, 0, 0)
                    pixels[x, y + 1] = (0, 0, 0)
                    pixels[x, y + 2] = (0, 0, 0)
                    y += 2
                else:
                    # 如果有第三个或更多连续白色像素，不做处理
                    while y < height and pixels[x, y] == (255, 255, 255):
                        y += 1
            else:
                y += 1

    return img


def remove_horizontal_white_pixels(img):
    pixels = img.load()
    width, height = img.size

    for y in range(height - 1, -1, -1):  # 从下到上扫描
        x = 0
        while x < width - 1:
            if pixels[x, y] == (255, 255, 255) and pixels[x + 1, y] == (255, 255, 255):
                # 如果连续两个像素是白色，且没有第三个连续白色像素
                if x + 2 >= width or pixels[x + 2, y] != (255, 255, 255):
                    # 将符合条件的像素块设置为黑色
                    pixels[x - 2, y] = (0, 0, 0)
                    pixels[x - 1, y] = (0, 0, 0)
                    pixels[x, y] = (0, 0, 0)
                    pixels[x + 1, y] = (0, 0, 0)
                    pixels[x + 2, y] = (0, 0, 0)
                    x += 2
                else:
                    # 如果有第三个或更多连续白色像素，不做处理
                    while x < width and pixels[x, y] == (255, 255, 255):
                        x += 1
            else:
                x += 1

    return img


def process_image(input_path, output_path):
    # 图像预处理：添加白色背景并反色
    img = preprocess_image(input_path)

    # 去除垂直方向的连续白色像素点
    img = remove_vertical_white_pixels(img)

    # 去除水平方向的连续白色像素点
    img = remove_horizontal_white_pixels(img)

    # 保存处理后的图像
    img.save(output_path)
    return img

def read_image(name):
    # 设置 Tesseract 路径
    
    # Windows路径示例
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # macOS路径示例
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    
    img = Image.open(name)
    custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    captcha_text = pytesseract.image_to_string(img, config=custom_config)
    return captcha_text.strip()

def process_all_captchas():
    # 创建输出目录
    input_dir = os.path.join(os.getcwd(), 'saved_captcha')
    output_dir = os.path.join(os.getcwd(), 'processed_captcha')
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            
            try:
                # 处理图片并获取识别结果
                captcha_text = process_and_read_captcha(None, input_path, output_dir)
                if captcha_text:
                    results[filename] = captcha_text
                else:
                    print(f"文件 {filename} 识别结果为空")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
    
    return results

def process_and_read_captcha(driver, input_image_path, output_dir):
    # 创建临时文件路径用于处理
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_output_path = os.path.join(temp_dir, "temp_processed.png")
    
    try:
        # 处理图片（这个处理后的图片只用于识别，作为临时文件）
        cleaned_img = process_image(input_image_path, temp_output_path)
        
        # 识别文字
        captcha_text = read_image(temp_output_path)
        
        # 如果识别成功，将原始图片复制到输出目录并重命名
        if captcha_text:
            final_output_path = os.path.join(output_dir, f"{captcha_text}.png")
            # 如果文件已存在，添加数字后缀
            counter = 1
            while os.path.exists(final_output_path):
                final_output_path = os.path.join(output_dir, f"{captcha_text}_{counter}.png")
                counter += 1
            
            # 复制原始图片到输出目录
            original_img = Image.open(input_image_path)
            original_img.save(final_output_path)
            
        # 删除临时文件和临时目录
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
            
        return captcha_text
        
    except Exception as e:
        print(f"处理图片时出错: {str(e)}")
        # 确保清理临时文件
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return None

def main():
    # 检查并创建必要的目录
    input_dir = os.path.join(os.getcwd(), 'saved_captcha')
    output_dir = os.path.join(os.getcwd(), 'processed_captcha')
    
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"已创建输入目录: {input_dir}")
        print("请将验证码图片放入 saved_captcha 文件夹中后再运行程序")
        return
    
    # 检查输入目录是否为空
    if not any(f.endswith(('.png', '.jpg', '.jpeg')) for f in os.listdir(input_dir)):
        print("saved_captcha 文件夹中没有图片文件！")
        print("请添加图片后再运行程序")
        return
    
    # 检查 Tesseract 是否已安装
    tesseract_path = r'/usr/local/bin/tesseract'
    if not os.path.exists(tesseract_path):
        print("错误：未找到 Tesseract-OCR！")
        print("请先安装 Tesseract-OCR，下载地址：https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    # 设置 Tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    try:
        # 处理所有验证码
        print("开始处理验证码...")
        results = process_all_captchas()
        
        # 输出处理结果
        print("\n处理完成！结果如下：")
        for original_name, recognized_text in results.items():
            print(f"原文件: {original_name} -> 识别结果: {recognized_text}")
        
        print(f"\n处理后的文件已保存到: {output_dir}")
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()

