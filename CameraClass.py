import numpy as np
import cv2
import time
import fileinput, sys
from ConfigParser import SafeConfigParser
import multiprocessing

cam = cv2.VideoCapture(1)

num = 0
sumCCT = 0
sumRGB = [0, 0, 0]
sumXYZ = [0, 0, 0]
sumxy = [0, 0]
CCTList = []
rValueList = []
gValueList = []
bValueList = [] 
XValueList = []
YValueList = []
ZValueList = [] 
xList = [] 
yList = []
avgCCTCopy = 0

class Camera:
	def rgbToCCT(self, rValue, gValue, bValue, colorIntensityTrue):
				
		parser = SafeConfigParser()
		
		parser.read('C:\\Python27\\Lib\\idlelib\\xyData1.txt')
		
		previousxValue = parser.get('xyValues', 'x') #saves previous values
		previousyValue = parser.get('xyValues', 'y')
		previousRMSCCT = parser.get('RMS', 'RMSCCT')
		previousRMSx = parser.get('RMS', 'RMSx')
		previousRMSy = parser.get('RMS', 'RMSy')
		
		rgbToXYZConversionMatrix = np.array([0.4124, 0.3576, 0.1805, 0.2126, 0.7152, 0.0722, 0.0193, 0.1192, 0.9502]).reshape(3,3)
		rgbValues = np.array([rValue, gValue, bValue]).reshape(3,1)
		XYZValues = np.dot(rgbToXYZConversionMatrix, rgbValues)
		
		x = XYZValues[0,:]/(XYZValues[0,:] + XYZValues[1,:] + XYZValues[2,:]) #calculates x 
		y = XYZValues[1,:]/(XYZValues[0,:] + XYZValues[1,:] + XYZValues[2,:]) #calculates y
		
		Xe = 0.3320
		Ye = 0.1858
		n = (x[0] - Xe)/(Ye - y[0])	

		CCT = 449.0 * (n**3) + 3525.0 * (n**2) + 6823.3 * n + 5520.33
			
		global num, sumCCT, sumRGB, sumXYZ, sumxy, avgCCTCopy
		global CCTList, rValueList, gValueList, bValueList, XValueList, YValueList, ZValueList, xList, yList
		
		num += 1 #keeps track of how many times method has run
		
		#puts all values in a list so can calculate RMS
		CCTList.append(CCT)  
		rValueList.append(rValue)
		gValueList.append(gValue)
		bValueList.append(bValue)
		XValueList.append(XYZValues[0])
		YValueList.append(XYZValues[1])
		ZValueList.append(XYZValues[2])
		xList.append(x)
		yList.append(y)
		
		#calculate sum to find avg later on
		sumCCT += CCT
		sumRGB = [sumRGB[0] + rValue, sumRGB[1] + gValue, sumRGB[2] + bValue]
		sumXYZ = [sumXYZ[0] + XYZValues[0], sumXYZ[1] + XYZValues[1], sumXYZ[2] + XYZValues[2]]
		sumxy = [sumxy[0] + x, sumxy[1] + y]
		
		squaredSumCCT = 0
		squaredSumRValue = 0
		squaredSumGValue = 0
		squaredSumBValue = 0
		squaredSumXValue = 0
		squaredSumYValue = 0
		squaredSumZValue = 0
		squaredSumx = 0
		squaredSumy = 0	
		
		if num == 100: #if finished get all values of each pixel in 10 by 10 grid 
			for i in range (0, num):
				squaredSumCCT += (CCTList[i] - (sumCCT/num)) ** (2)
				squaredSumRValue += (rValueList[i] - (sumRGB[0]/num)) ** (2)
				squaredSumGValue += (gValueList[i] - (sumRGB[1]/num)) ** (2)
				squaredSumBValue += (bValueList[i] - (sumRGB[2]/num)) ** (2)
				squaredSumXValue += (XValueList[i] - (sumXYZ[0]/num)) ** (2)
				squaredSumYValue += (YValueList[i] - (sumXYZ[1]/num)) ** (2)
				squaredSumZValue += (ZValueList[i] - (sumXYZ[2]/num)) ** (2)
				squaredSumx += 	(xList[i] - (sumxy[0]/num)) ** (2)
				squaredSumy += 	(yList[i] - (sumxy[1]/num)) ** (2)
			RMSCCT = (squaredSumCCT/num) ** (0.5)	
			RMSRGB = [(squaredSumRValue/num) ** (0.5), (squaredSumGValue/num) ** (0.5), (squaredSumBValue/num) ** (0.5)]
			RMSXYZ = [(squaredSumXValue/num) ** (0.5), (squaredSumYValue/num) ** (0.5), (squaredSumZValue/num) ** (0.5)]
			RMSxy = [(squaredSumx/num) ** (0.5), (squaredSumy/num) ** (0.5)]
			
			minRGB = [rValueList[0], gValueList[0], bValueList[0]]
			maxRGB = [0, 0, 0]
			#finds max and min rgb values
			for i in range (0, num):
				if minRGB[0] > rValueList[i] and minRGB[1] > gValueList[i] and minRGB[2] > bValueList[i]:
					minRGB = [rValueList[i], gValueList[i], bValueList[i]]
				if maxRGB[0] < rValueList[i] and maxRGB[1] < gValueList[i] and maxRGB[2] < bValueList[i]:
					maxRGB = [rValueList[i], gValueList[i], bValueList[i]]			
					
			print "Min RGB: ", minRGB
			print "Max RGB: ", maxRGB
			
			print "Avg RGB Values: [", sumRGB[0]/num,",", sumRGB[1]/num,",", sumRGB[2]/num,"]"	
			print "Avg XYZ Values: [", sumXYZ[0]/num,",", sumXYZ[1]/num,",", sumXYZ[2]/num,"]"	
			print "Avg x:", sumxy[0]/num
			print "Avg y:", sumxy[1]/num
			print "Avg CCT:", sumCCT/num
			
			print "RMS RGB:", RMSRGB
			print "RMS XYZ:", RMSXYZ
			print "RMS x:", RMSxy[0] 
			print "RMS y:", RMSxy[1]
			print "RMS CCT:", RMSCCT
			
			avgCCTCopy = sumCCT/num
			#saves all values to data file
			with open('C:\\Python27\\Lib\\idlelib\\rgbToCCTdata.txt', 'a') as file:
				file.write("------------------------Start------------------------ \n")		    
				file.write('Date: ' + (time.strftime("%m/%d/%Y")) + ' Time: ' + (time.strftime("%I:%M:%S")) + '\n')
				if colorIntensityTrue == False:
					file.write('No color intensity. \n')
				file.write('\t Min RGB Values:' + str(minRGB) + '\n')
				file.write('\t Max RGB Values:' + str(maxRGB) + '\n')	
				file.write('\t Avg RGB Values: [' + str(sumRGB[0]/num) + ', ' + str(sumRGB[1]/num) + ', ' + str(sumRGB[2]/num) +']\n')
				file.write('\t Avg XYZ Values: ' + str(sumXYZ[0]/num) + ", " + str(sumXYZ[1]/num) + ", " + str(sumXYZ[2]/num) + '\n')
				file.write('\t Avg x: ' + str(sumxy[0]/num) + '\n')
				file.write('\t Avg y: ' + str(sumxy[1]/num) + '\n')
				file.write('\t Avg CCT: ' + str(sumCCT/num) + '\n')
				file.write('\t RMS RGB: ' + str(RMSRGB) + '\n')
				file.write('\t RMS XYZ: '+ str(RMSXYZ) + '\n')
				file.write('\t RMS x: '+ str(RMSxy[0]) + '\n')
				file.write('\t RMS y: '+ str(RMSxy[1]) + '\n')					
				file.write('\t RMS CCT: ' + str(RMSCCT) + '\n')
				file.write("-------------------------End------------------------- \n")
			
			sumxy[0] = float(str(sumxy[0]).replace('[','').replace(']',''))
			sumxy[1] = float(str(sumxy[1]).replace('[','').replace(']',''))
			RMSxy[0] = float(str(RMSxy[0]).replace('[','').replace(']',''))
			RMSxy[1] = float(str(RMSxy[1]).replace('[','').replace(']',''))
			
			#updates x, y, RMS CCT, RMS x, and RMS y so can graph on chromaticity diagram
			for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\xyData1.txt", inplace=True):	
				line = line.replace("x=" + previousxValue, "x=" + str(sumxy[0]/num))
				sys.stdout.write(line)
			for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\xyData1.txt", inplace=True):	
				line = line.replace("y=" + previousyValue, "y=" + str(sumxy[1]/num))
				sys.stdout.write(line)
			for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\xyData1.txt", inplace=True):	
				line = line.replace("RMSCCT=" + previousRMSCCT, "RMSCCT=" + str(RMSCCT))
				sys.stdout.write(line)
			for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\xyData1.txt", inplace=True):	
				line = line.replace("RMSx=" + previousRMSx, "RMSx=" + str(RMSxy[0]))
				sys.stdout.write(line)
			for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\xyData1.txt", inplace=True):	
				line = line.replace("RMSy=" + previousRMSy, "RMSy=" + str(RMSxy[1]))
				sys.stdout.write(line)			
				
			#resets all values		
			num = 0
			sumCCT = 0
			sumRGB = [0, 0, 0]
			sumXYZ = [0, 0, 0]
			sumxy = [0, 0]
			CCTList = []
			rValueList = []
			gValueList = []
			bValueList = [] 
			XValueList = []
			YValueList = []
			ZValueList = [] 
			xList = [] 
			yList = []
			
			return(avgCCTCopy)
			
	def checkUnderOrOverSaturated(self, rgbValue):			
		if rgbValue[0] >= 225 or rgbValue[1] >= 225 or rgbValue[2] >= 225:
			print rgbValue, "Error. Oversaturated"
			return True
		elif rgbValue[0] <= 0 or rgbValue[1] <= 0 or rgbValue[2] <= 0:
			print rgbValue, "Error. Undersaturated"
			return True
		else:
			return False
			
def main():
	while True:
		# Capture frame-by-frame
		ret, img = cam.read()
		
		cctTrue = raw_input('CCT? (y/n) or "q" to quit: ')
		colorIntensityTrue = raw_input('Is there color intensity? (y/n): ')
		if colorIntensityTrue == 'n':
			colorIntensityTrue = False
		if cctTrue == 'y': 
			# Our operations on the frame come here
			cv2.rectangle(img, (316, 236), (325, 245), (255, 255, 255), 2) 					
			cv2.rectangle(img, (0, 0), (640, 480), (255, 255, 255), 2)		
			
			ignoreSaturation = False
			for row in range(0, 10):
				for col in range(0, 10):				
					rgbValue = [img[316 + row][236 + col][2], img[316 + row][236 + col][1], img[316 + row][236 + col][0]] #puts rgb values in an array
					if ignoreSaturation == False:
						if Camera().checkUnderOrOverSaturated(rgbValue) == True:
							quitInput = raw_input('Ignore Saturation? (if "n" will quit) (y/n): ')
							if quitInput == 'n':
								sys.exit()
							else:
								ignoreSaturation = True
					Camera().rgbToCCT(rgbValue[0], rgbValue[1], rgbValue[2], colorIntensityTrue)
			
			execfile('C:\\Python27\\Lib\\idlelib\\xyChromaticityGraphing.py') #calls program to graph x and y values 
			print "-----------------------------------------------------------"
		if cctTrue == 'q': #if user wants to quit, break while loop
			break
		cv2.imshow('frame',img) 
		
	# When everything done, release the capture
	cam.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
