
# 红色激光系统识别矩形

import sensor, image ,time, pyb, ustruct, math
from pyb import UART

# 红色激光阈值
red =(16, 100, 3, 79, 11, 74)
# A4靶纸顶点坐标
corners = 0

uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=900)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

def check_if_a4_size(corners):
    # 计算矩形面积
    delta_x = math.fabs(corners[1][0] - corners[0][0])
    delta_y = math.fabs(corners[1][1] - corners[0][1])
    l = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    delta_x =  math.fabs(corners[2][0] - corners[1][0])
    delta_y =  math.fabs(corners[2][1] - corners[1][1])
    w = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    if l < w:
        t = l
        l = w
        w = t
    # 是否为A4大小
    if l > 90 and l < 130 and w > 60 and w < 90:
        print(l, w)
        return True
    else:
        return False


# 基本要求3
while 3:
    img = sensor.snapshot().lens_corr(1.8)
    while corners == 0:
        img = sensor.snapshot().lens_corr(1.8)
        for r in img.find_rects(threshold = 100000):
            if check_if_a4_size(r.corners()):
                corners = r.corners()
                uart.write(ustruct.pack("<HHHHHHHH", corners[3][0]+3,corners[3][1]+3,corners[2][0]-3,corners[2][1]+3,corners[1][0]-3,corners[1][1]-3,corners[0][0]+3,corners[0][1]-3))
                print(corners[3][0]+3,corners[3][1]+3,corners[2][0]-3,corners[2][1]+3,corners[1][0]-3,corners[1][1]-3,corners[0][0]+3,corners[0][1]-3)
                # 调试
                for p in corners:
                    img.draw_cross(p[0], p[1], (0, 255, 255), 2)
    pyb.delay(100)
    while corners != 0:
        img = sensor.snapshot().lens_corr(1.8)
        blobs = img.find_blobs([red],x_stride=1, y_stride=1, area_threshold=0, pixels_threshold=0,merge=True,margin=4)
        if len(blobs)>=1 :
            b = blobs[0]
            cx = b[5]
            cy = b[6]
            for i in range(len(blobs)-1):
                cx = blobs[i][5]+cx
                cy = blobs[i][6]+cy
            cx=int(cx/len(blobs))
            cy=int(cy/len(blobs))
            img.draw_cross(cx, cy, [255,255,0], 3)
            print(cx,cy)
            uart.write(ustruct.pack("<HH", cx, cy))


