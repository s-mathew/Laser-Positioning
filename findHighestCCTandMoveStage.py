import StageClass
import CameraClass
import cv2

cam = cv2.VideoCapture(1)
highestCCTValue = 0
avgCCT = 0

numOfTimesMoved = 0
currentYPos = 0

stage = StageClass.Stage()
while True:
	# Capture frame-by-frame
	ret, img = cam.read()
	global avgCCT
	quit = raw_input('Quit? (y/n): ')
	if quit == 'n':
		for row in range(0, 10):
			for col in range(0, 10):				
				rgbValue = [img[316 + row][236 + col][2], img[316 + row][236 + col][1], img[316 + row][236 + col][0]]
				avgCCT = CameraClass.Camera().rgbToCCT(rgbValue[0], rgbValue[1], rgbValue[2], True)
		#print CameraClass.num
		print "Avg CCT: ", avgCCT		
		print "Highest CCT Value So Far:", highestCCTValue
		if highestCCTValue <= avgCCT:
			highestCCTValue = avgCCT		
			numOfTimesMoved += 1
			
			stage.move(0, StageClass.currentYCoord + 0.5, 0)
			
			
			stage.returnCurrentCoordinates()
		else:
			break
		
	else:
		break
			
			
		
