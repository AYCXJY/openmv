import sensor, image ,time, pyb, ustruct, math
from pyb import UART


red = (0, 100, 1, 79, -11, 63)

black =(120, 0)
paper = (145, 255)

extern_corners = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
intern_corners = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
corners = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
_extern = False
_intern = False

instruction = 0

clock = time.clock()
uart = UART(3, 115200)
sensor.reset()
sensor.set_auto_gain(False)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)

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
		print(l,w)
		return True
	else:
		return False

while 1:
	if uart.any():
		receive = uart.read(1).decode()
		print(receive)
		if receive == '1':
			instruction = 1
		if receive == '2':
			instruction = 2
		if receive == '3':
			instruction = 3
		if receive == '4':
			break
#instruction = 3
if instruction == 0:
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_auto_exposure(False, 2800)
	pyb.delay(200)
	while 1:
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
			#img.draw_cross(cx, cy, [0,255,255],2)
			#print(cx,cy)
			uart.write(ustruct.pack("<HH", cx, cy))
		#for p in edge:
			#img.draw_cross(p[0], p[1], (0, 255, 255), 1)


if instruction == 1 or instruction == 2:
	edge = [[65,20],[264,17],[264,213],[65,212]]
	uart.write(ustruct.pack("<HHHHHHHH", edge[0][0],edge[0][1],edge[1][0],edge[1][1],edge[2][0],edge[2][1],edge[3][0],edge[3][1]))
	#print(edge[0][0],edge[0][1],edge[1][0],edge[1][1],edge[2][0],edge[2][1],edge[3][0],edge[3][1])
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_auto_exposure(False, 2800)
	pyb.delay(200)
	while 1:
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
			#img.draw_cross(cx, cy, [0,255,255],2)
			#print(cx,cy)
			uart.write(ustruct.pack("<HH", cx, cy))
		for p in edge:
			img.draw_cross(p[0], p[1], (0, 255, 255), 1)

if instruction == 3:
	while _extern == False:
		img = sensor.snapshot().lens_corr(1.8)
		img.binary([black])
		for r in img.find_rects(threshold = 100000):
			if check_if_a4_size(r.corners()):
				intern_corners = r.corners()
				for p in intern_corners:
					img.draw_cross(p[0], p[1], (0, 255, 255), 2)
				print(intern_corners)
				_extern = True
	while _intern == False:
		img = sensor.snapshot().lens_corr(1.8)
		img.binary([paper])
		for r in img.find_rects(threshold = 100000):
			if check_if_a4_size(r.corners()):
				extern_corners = r.corners()
				for p in extern_corners:
					img.draw_cross(p[0], p[1], (0, 255, 255), 2)
				print(extern_corners)
				_intern = True
	t = intern_corners
	while math.fabs(t[0][0] - extern_corners[0][0]) > 20 or math.fabs(t[0][1] - extern_corners[0][1]) > 20:
		t = [t[1],t[2],t[3],t[0]]
	corners[0][0] = int((extern_corners[0][0] + t[0][0]) / 2)
	corners[0][1] = int((extern_corners[0][1] + t[0][1]) / 2)
	corners[1][0] = int((extern_corners[1][0] + t[1][0]) / 2)
	corners[1][1] = int((extern_corners[1][1] + t[1][1]) / 2)
	corners[2][0] = int((extern_corners[2][0] + t[2][0]) / 2)
	corners[2][1] = int((extern_corners[2][1] + t[2][1]) / 2)
	corners[3][0] = int((extern_corners[3][0] + t[3][0]) / 2)
	corners[3][1] = int((extern_corners[3][1] + t[3][1]) / 2)

	uart.write(ustruct.pack("<HHHHHHHH", corners[3][0],corners[3][1],corners[2][0],corners[2][1],corners[1][0],corners[1][1],corners[0][0],corners[0][1]))
	#print(corners[3][0],corners[3][1],corners[2][0],corners[2][1],corners[1][0],corners[1][1],corners[0][0],corners[0][1])
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_auto_exposure(False, 2800)
	pyb.delay(200)
	while 1:
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
			#print(cx,cy)
			uart.write(ustruct.pack("<HH", cx, cy))
		for p in corners:
			img.draw_cross(p[0], p[1], (0, 255, 255), 1)
