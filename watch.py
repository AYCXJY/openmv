import sensor, image ,time, pyb, ustruct, math
from pyb import UART


clock = time.clock()
uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
#sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

while 1:
	img = sensor.snapshot().lens_corr(1.8)
