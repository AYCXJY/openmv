import sensor, image ,time, pyb, ustruct, math
from pyb import UART

red = (0, 100, 1, 79, -11, 63)

green = (7, 100, -48, 1, -128, 127)

red_cx = 0
red_cy = 0
green_cx = 0
green_cy = 0

uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False, 2800)
pyb.delay(200)

while 1:
	img = sensor.snapshot().lens_corr(1.8)

	blobs = img.find_blobs([red],x_stride=1, y_stride=1, area_threshold=0, pixels_threshold=0,merge=True,margin=10)
	if len(blobs)>=1 :
		b = blobs[0]
		red_cx = b[5]
		red_cy = b[6]
		for i in range(len(blobs)-1):
			red_cx = blobs[i][5]+red_cx
			red_cy = blobs[i][6]+red_cy
		red_cx=int(red_cx/len(blobs))
		red_cxy=int(red_cy/len(blobs))

		img.draw_cross(red_cx, red_cy, [255,0,0],2)

	blobs = img.find_blobs([green],x_stride=1, y_stride=1, area_threshold=0, pixels_threshold=0,merge=True,margin=10)
	if len(blobs)>=1 :
		b = blobs[0]
		green_cx = b[5]
		green_cy = b[6]
		for i in range(len(blobs)-1):
			green_cx = blobs[i][5]+green_cx
			green_cy = blobs[i][6]+green_cy
		green_cx=int(green_cx/len(blobs))
		green_cy=int(green_cy/len(blobs))

		img.draw_cross(green_cx, green_cy, [0,255,0],2)

	print(red_cx, red_cy, green_cx, green_cy)
	uart.write(ustruct.pack("<HHHH", red_cx, red_cy, green_cx, green_cy))
