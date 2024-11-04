import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 修改保存图像路径的设置
save_image_path = os.path.join(os.getcwd(), 'saved_captcha')

# 确保文件夹存在
os.makedirs(save_image_path, exist_ok=True)

def process_and_read_captcha(driver, save_image_path):
    # 显式等待确保 captchaImg 元素加载完成
    wait = WebDriverWait(driver, 10)
    box_certification_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "box_certification")))
    captcha_element = box_certification_element.find_element(By.CLASS_NAME, "captcha")
    api_element = captcha_element.find_element(By.CLASS_NAME, "api")
    captcha_img_element = api_element.find_element(By.ID, "captchaImg")

    # 获取图片的 base64 数据
    captcha_img_src = captcha_img_element.get_attribute("src")

    # 确保获取的是base64编码的数据
    if captcha_img_src.startswith("data:image"):
        base64_img_data = captcha_img_src.split(",")[1]
        img_data = base64.b64decode(base64_img_data)

        # 使用 os.path.join 构建完整的文件路径
        image_file_path = os.path.join(save_image_path, f'{i + 1}.png')
        
        # 保存图片
        with open(image_file_path, 'wb') as file:
            file.write(img_data)
        print(f"验证码图片已保存: {image_file_path}")
    else:
        print("验证码图片源格式不正确")

# 浏览器配置对象
chrome_options = Options()
print("浏览器配置对象")

# 连接到手动启动的 Chrome 实例
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
print("连接到手动启动的 Chrome 实例")

# 隐藏 WebDriver 的痕迹
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
print("隐藏 WebDriver 的痕迹")

# 启动 WebDriver 并连接到已启动的 Chrome 实例
driver = webdriver.Chrome(options=chrome_options)
print("启动 WebDriver 并连接到已启动的 Chrome 实例")

# 设置隐式等待
driver.implicitly_wait(5)
print("设置隐式等待")

tabs = driver.window_handles
print("打开多个标签页后所有窗口句柄：", tabs)

input("等待用户按回车键以开始检测预订按钮")

try:
    # 打印当前Chrome的所有句柄
    print("当前Chrome的所有句柄：", driver.window_handles)

    # 检查是否有窗口句柄可用
    if driver.window_handles:
        # 指定切换窗口默认为最新
        driver.switch_to.window(driver.window_handles[0])
        print("切换到的窗口句柄：", driver.current_window_handle)
    else:
        print("没有可用的窗口句柄。")

    # 循环语句进行200次
    for i in range(200):
        # 使用正确的文件路径格式
        process_and_read_captcha(driver, save_image_path)

        # 等待时间逐渐增加
        n = 1
        time.sleep(n)
        n += 0.1

        # 点击刷新按钮
        reload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnReload'))
        )
        reload_button.click()

except Exception as e:
    print(f"发生错误: {str(e)}")
