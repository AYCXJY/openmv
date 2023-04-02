"""
项目功能：OpenMV识别数字（模板匹配）
硬件平台：OpenMVH7Plus
配合文件：数字模板的pgm文件
"""
import sensor, image
# SEARCH_EX是穷举搜索，SEARCH_DS是菱形搜索
# 在菱形搜索中，步长和ROI都被忽略
from image import SEARCH_EX, SEARCH_DS

# 初始化感光元件
sensor.reset()

# 设置图像对比度为1
sensor.set_contrast(1)

# 图像增益上限设置为16
sensor.set_gainceiling(16)

# 模板匹配最大分辨率为QQVGA
sensor.set_framesize(sensor.QQVGA)

# 像素格式为灰度
sensor.set_pixformat(sensor.GRAYSCALE)

# 模板导入
templates = ("/1.pgm", "/2.pgm", "/3.pgm", "/4.pgm")

while (True):
    # 拍摄一张照片，得到图像对象
    img = sensor.snapshot()
    
    # 轮询搜索目标模板，匹配成功画矩形
    for index in templates:
        template = image.Image(index)
        result = img.find_template(template, 0.70, step=4, search=SEARCH_EX)
        if result:
            img.draw_rectangle(result)
