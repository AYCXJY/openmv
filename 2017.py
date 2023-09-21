import sensor, image, time, pyb, ustruct
from pyb import UART

thresholds = (205, 255)

uart = UART(3, 115200)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

while 1:
	clock.tick()
	img = sensor.snapshot().lens_corr(1.8)
	for c in img.find_blobs([thresholds], x_stride=1, roi=[44,20,210,214], pixels_threshold=20):
		print('x:', c.cx(), 'y:', c.cy())
		img.draw_cross(c.cx(), c.cy(), color=0)
		uart.write(ustruct.pack("<HH", c.cx(), c.cy()))
