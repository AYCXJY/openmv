"""
项目功能：OpenMV舵机云台追踪色块
硬件平台：OpenMVH7Plus + 星瞳舵机云台
配合文件：pid.py
"""
import sensor, image
from pid import PID
from pyb import Servo

# 设定目标颜色LAB阈值
target_threshold  = (36, 79, 13, 58, 3, 38)

# 创建舵机实例
pan_servo = Servo(1)
tilt_servo = Servo(2)

# 规定PWM范围500~2500，起始位置在500
pan_servo.calibration(500, 2500, 500)
tilt_servo.calibration(500, 2500, 500)

# 初始化舵机PID参数（在线调试设定值）
pan_pid = PID(p=0.1, i=0, imax=90)
tilt_pid = PID(p=0.05, i=0, imax=90)

# 初始化感光元件
sensor.reset()

# 设置为彩色
sensor.set_pixformat(sensor.RGB565)

# 设置图像的大小
sensor.set_framesize(sensor.QQVGA)

# 跳过n张照片，在更改设置后，跳过一些帧，等待感光元件变稳定。
sensor.skip_frames(10)

# 在颜色追踪中，需要关闭白平衡
sensor.set_auto_whitebal(False)

# 开启垂直翻转
sensor.set_vflip(True)

# 开启水平镜像
sensor.set_hmirror(True)

def find_maxblob(blobs):
	"""返回blobs组中外接矩形面积最大的blob对象"""
	max_size = 0
	for blob in blobs:
		if blob.w() * blob.h() > max_size:
			max_blob = blob
			max_size = blob.w() * blob.h()
	return max_blob

while(True):	
	# 拍摄一张照片，得到图像对象
	img = sensor.snapshot()
	
	# 查找图像中所有目标颜色色块，并返回一个色块对象列表
	blobs = img.find_blobs([target_threshold])
	
	# 如果列表不为空（找到了目标颜色色块）
	if blobs:
		# 得到面积最大色块对象
		max_blob = find_maxblob(blobs)
		
		# 为保持色块在图像中央，计算色块偏离的误差
		pan_error = max_blob.cx() - img.width() / 2
		tilt_error = max_blob.cy() - img.height() / 2
		
		# 用矩形框住目标色块
		img.draw_rectangle(max_blob.rect())
		
		# 用十字标记目标色块
		img.draw_cross(max_blob.cx(), max_blob.cy())
		
		# 得到矫正值
		pan_output = pan_pid.get_pid(pan_error, 1) / 2
		tilt_output = tilt_pid.get_pid(tilt_error, 1)
		
		# 驱动舵机使目标色块处于图像中央
		pan_servo.angle(pan_servo.angle()-pan_output)
		tilt_servo.angle(tilt_servo.angle()+tilt_output)
