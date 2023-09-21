
# 红色激光系统锁定单个坐标

import sensor, image ,time, pyb, ustruct, math
from pyb import UART

# 红色激光阈值
red = (0, 100, 1, 79, -11, 63)

uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=900)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

# 基本要求1
while 1:
	img = sensor.snapshot().lens_corr(1.8)
	blobs = img.find_blobs([red],x_stride=1, y_stride=1, area_threshold=0, pixels_threshold=0,merge=True,margin=3)
	if len(blobs) >= 1:
		b = blobs[0]
		cx = b[5]
		cy = b[6]
		for i in range(len(blobs)-1):
			cx = blobs[i][5]+cx
			cy = blobs[i][6]+cy
		cx = int(cx / len(blobs))
		cy = int(cy / len(blobs))
		img.draw_cross(cx, cy, [255,255,0], 3)
		print(cx,cy)
		uart.write(ustruct.pack("<HH", cx, cy))


