import sensor, image ,time, pyb, ustruct, math
from pyb import UART

red = (0, 100, 1, 79, -11, 63)
green = (7, 100, -48, 1, -128, 127)
black =[0, 255]
paper = [0, 255]
extern_corners = 0
intern_corners = 0
corners = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
edge = 0
edge_threashold = [0,95]
instruction = 0
kernel_size = 1
kernel = [-2, -1,  0, -1,  1,  1,  0,  1,  2]

clock = time.clock()
uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

def check_if_edge_size(corners):
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
	if l > 190 and l < 205 and w > 190 and w < 205:
		if math.fabs(l - w) < 2:
			print(l, w)
			return True
		else:
			return False
def check_if_a4_size(corners):
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
	if l > 90 and l < 130 and w > 60 and w < 90:
		print(l, w)
		return True
	else:
		return False
def check_reset():
	if uart.any():
		receive = uart.read(1).decode()
		if receive == 'R':
			print(receive)
			#pyb.hard_reset()

while 1:
	while edge == 0:
		check_reset()
		img = sensor.snapshot().histeq(adaptive=True, clip_limit=-1).lens_corr(1.8)
		img.morph(kernel_size, kernel)
		img.erode(1, threshold = 8)
		#img.binary([(edge_threashold)])
		for r in img.find_rects(threshold = 90000):
			if check_if_edge_size(r.corners()):
				edge = r.corners()

	corners[0][0] = int((edge[0][0] + edge[0][0]) / 2)
	corners[0][1] = int((edge[0][1] + edge[0][1]) / 2)
	corners[1][0] = int((edge[1][0] + edge[1][0]) / 2)
	corners[1][1] = int((edge[1][1] + edge[1][1]) / 2)
	corners[2][0] = int((edge[2][0] + edge[2][0]) / 2)
	corners[2][1] = int((edge[2][1] + edge[2][1]) / 2)
	corners[3][0] = int((edge[3][0] + edge[3][0]) / 2)
	corners[3][1] = int((edge[3][1] + edge[3][1]) / 2)
	uart.write(ustruct.pack("<HHHHHHHH", corners[3][0],corners[3][1],corners[2][0],corners[2][1],corners[1][0],corners[1][1],corners[0][0],corners[0][1]))
	print(corners[3][0],corners[3][1],corners[2][0],corners[2][1],corners[1][0],corners[1][1],corners[0][0],corners[0][1])
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_auto_exposure(False, 2800)
	pyb.delay(200)
	while 1:
		check_reset()
		img = sensor.snapshot().lens_corr(1.8)
		blobs = img.find_blobs([red],x_stride=1, y_stride=1, area_threshold=0, pixels_threshold=0,merge=True,margin=10)
		if len(blobs)>=1 :
			b = blobs[0]
			cx = b[5]
			cy = b[6]
			for i in range(len(blobs)-1):
				cx = blobs[i][5]+cx
				cy = blobs[i][6]+cy
			cx=int(cx/len(blobs))
			cy=int(cy/len(blobs))
			img.draw_cross(cx, cy, [0,255,255],2)
			print(cx,cy)
			uart.write(ustruct.pack("<HH", cx, cy))
		for p in edge:
			img.draw_cross(p[0], p[1], (0, 255, 255), 1)
