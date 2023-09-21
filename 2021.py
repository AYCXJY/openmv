import sensor, image, time, pyb
from pyb import UART
from image import SEARCH_EX, SEARCH_DS

# 储存目标数字
target_num = 0
# 储存转弯信息
turn_status = []
# 储存目标数字识别模板
target_templates = ["1.pgm", "/2.pgm", "/3.pgm", "/4.pgm", "/5.pgm", "/6.pgm", "/7.pgm", "/8.pgm"]
# 储存病房数字模板
templates = ["31.pgm", "32.pgm", "33.pgm", "34.pgm", "35.pgm", "36.pgm", "37.pgm", "38.pgm", "39.pgm", "310.pgm", "41.pgm", "42.pgm", "43.pgm", "44.pgm", "45.pgm", "46.pgm", "47.pgm", "48.pgm", "49.pgm", "410.pgm", "51.pgm", "52.pgm", "53.pgm", "54.pgm", "55.pgm", "56.pgm", "57.pgm", "58.pgm", "59.pgm", "510.pgm", "61.pgm", "62.pgm", "63.pgm", "64.pgm", "65.pgm", "66.pgm", "67.pgm", "68.pgm", "69.pgm", "610.pgm", "71.pgm", "72.pgm", "73.pgm", "74.pgm", "75.pgm", "76.pgm", "77.pgm", "78.pgm", "79.pgm", "710.pgm", "81.pgm", "82.pgm", "83.pgm", "84.pgm", "85.pgm", "86.pgm", "87.pgm", "88.pgm", "89.pgm", "810.pgm"]

# 寻找平行的直线（意味着到达需要识别的路口），找到返回True，否则返回False
def find_intersection(img):
	for l in img.find_lines(threshold = 1300):
		if l.theta() > 80 and l.theta() < 150 and l.rho() > -10:
			img.draw_line(l.line())
			return True
	return False
# 寻找多个小方格（意味着到达病房门口），找到返回True，否则返回False
def find_destination(img):
	rect_count = 0
	for r in img.find_rects(threshold = 10000):
		img.draw_rectangle(r.rect())
		rect_count =rect_count + 1
		if rect_count >= 5:
			rect_count = 0
			return True
	return False
# 向串口发送数据
def send_message(msg):
	uart.write(msg)
	print(msg)  # 在上位机上显示调试信息
# 程序停止，等待小车完成转弯动作
def ACK():
	while(1):
		if uart.any():
			a = uart.read(1).decode()
			if a == 'O':
				break
# 检查复位信号
def check_reset():
	if uart.any():
		a = uart.read(1).decode()
		if a == 'T':
			pyb.hard_reset()

# 相机复位
sensor.reset()
# 设置对比度
sensor.set_contrast(1)
# 设置增益
sensor.set_gainceiling(16)
# 设置图像大小
sensor.set_framesize(sensor.QQVGA)
# 设置为黑白灰度图像
sensor.set_pixformat(sensor.GRAYSCALE)
# 图像水平翻转
sensor.set_hmirror(True)
# 图像竖直翻转
sensor.set_vflip(True)
# 设置ROI窗口
#sensor.set_windowing()
# 串口初始化
uart = UART(3, 115200)

# 识别目标数字
while target_num == 0:
	check_reset()
	# find target number
	count = 0
	for t in target_templates:
		img = sensor.snapshot()
		template = image.Image(t)
		r = img.find_template(template, 0.7, step=4, search=SEARCH_EX)
		if r:
			img.draw_rectangle(r)
			target_num = count + 1
			if target_num == 1:
				send_message('1')
			elif target_num == 2:
				send_message('2')
			elif target_num == 3:
				send_message('3')
			elif target_num == 4:
				send_message('4')
			elif target_num == 5:
				send_message('5')
			elif target_num == 6:
				send_message('6')
			elif target_num == 7:
				send_message('7')
			elif target_num == 8:
				send_message('8')
		count = count + 1


# 1 2
while target_num - 2 <= 0:
	while 1:
		check_reset()
		img = sensor.snapshot()
		if find_destination(img):
			send_message('S')
			break
	ACK()
	while 1:
		img = sensor.snapshot()
		if find_destination(img):
			send_message('S')
			while 1:
				check_reset()

# 3 4 5 6 7 8
while 1 :
	check_reset()
	img = sensor.snapshot()
	for t in templates[(target_num - 3) * 10 : (target_num - 2) * 10]:
		template = image.Image(t)
		r = img.find_template(template, 0.70, step=4, search=SEARCH_EX)
		if r:
			if r[0] < 75:
				send_message('L')
				turn_status.append('L')
				ACK()
			else:
				send_message('R')
				turn_status.append('R')
				ACK()
	if find_destination(img):
		send_message('S')
		break
ACK()
while(1):
	check_reset()
	img = sensor.snapshot()
	if turn_status:
		if find_intersection(img):
			if turn_status[-1] == 'L':
				send_message('R')
				turn_status.pop()
				ACK()
			elif turn_status[-1] == 'R':
				send_message('L')
				turn_status.pop()
				ACK()
	if find_destination(img):
		send_message('S')
		break



