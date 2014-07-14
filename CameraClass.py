import numpy as np
import cv2
import time
import fileinput, sys

cam = cv2.VideoCapture(1)

class Camera:
	def rgbToCCT(self, rValue, gValue, bValue):
		rgbToXYZConversionMatrix = np.array([0.4124, 0.3576, 0.1805, 0.2126, 0.7152, 0.0722, 0.0193, 0.1192, 0.9502]).reshape(3,3)
		rgbValue = np.array([rValue, gValue, bValue]).reshape(3,1)
		XYZValues = np.dot(rgbToXYZConversionMatrix, rgbValue)
		#print "rgbValue ",(rgbValue)


		x = XYZValues[0,:]/(XYZValues[0,:] + XYZValues[1,:] + XYZValues[2,:])
		y = XYZValues[1,:]/(XYZValues[0,:] + XYZValues[1,:] + XYZValues[2,:])
		
	
		print "XYZValues : ", XYZValues
		print "x:", x
		print "y: ", y

		Xe = 0.3320
		Ye = 0.1858
		n = (x - Xe)/(Ye - y)	

		CCT = 449.0 * (n**3) + 3525.0 * (n**2) + 6823.3 * n + 5520.33
		with open('C:\\Python27\\Lib\\idlelib\\rgbToCCTdata.txt', 'a') as file:
			file.write("------------------------Start------------------------ \n")		    
			file.write('Date: ' + (time.strftime("%m/%d/%Y")) + ' Time: ' + (time.strftime("%I:%M:%S")) + '\n')
			file.write('\t XYZValues: \n')
			file.write('\t' + str(XYZValues) + '\n')	
			file.write('\t x: ' + str(x) + '\n')
			file.write('\t y: ' + str(y) + '\n')
			file.write('\t CCT: ' + str(CCT) + '\n')
			file.write("-------------------------End------------------------- \n")
		print "CCT: ", CCT
	
while(True):
	# Capture frame-by-frame
	ret, img = cam.read()
	
	cctTrue = raw_input('CCT? (y/n) or "q" to quit: ')
	if cctTrue == 'y': 
		# Our operations on the frame come here
		cv2.rectangle(img, (316, 236), (325, 245), (255, 255, 255), 2) 					
		cv2.rectangle(img, (0, 0), (640, 480), (255, 255, 255), 2)		
		sumRed = 0
		sumGreen = 0
		sumBlue = 0		
		for row in range(0, 10):
			for col in range(0, 10):	
				sumRed += img[316 + row][236 + col][2]
				sumGreen += img[316 + row][236 + col][1] 				
				sumBlue += img[316 + row][236 + col][0]
		print "Avg Red: ", (sumRed/100)				
		print "Avg Green: ", (sumGreen/100)
		print "Avg Blue: ", (sumBlue/100)
		Camera().rgbToCCT(sumRed/100, sumGreen/100, sumBlue/100)
	
		print "-----------------------------------------------------------"
	if cctTrue == 'q':
		break
	cv2.imshow('frame',img)
	#time.sleep(2)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()

