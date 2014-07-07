import serial
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('C:\\Python27\\Lib\\idlelib\\config.txt')

ser = serial.Serial("COM3", 115200, timeout = None)

currentXCoord = 0
currentYCoord = 0
currentZCoord = 0
	

class Stage:
	#keeps track of current coordinates
	
	def move(self, newXCoord, newYCoord, newZCoord): #moves to new coordinates
		global currentXCoord, currentYCoord, currentZCoord
		if self.withinLimitXandYCoord(newXCoord) == False:
			print "XCoord - Not in range. Must be between -6.5 and 6.5"
			newXCoord = currentXCoord	#will not move from current position
		if self.withinLimitXandYCoord(newYCoord) == False:
			print "YCoord - Not in range. Must be between -6.5 and 6.5"
			newYCoord = currentYCoord
		if self.withinLimitZCoord(newZCoord) == False:
			print "ZCoord - Not in range. Must be between -3.25 and 3.25"
			newZCoord = currentZCoord	
		
		currentXCoord = newXCoord  
		currentYCoord = newYCoord
		currentZCoord = newZCoord	
		print ser.write('{"gc":"g0 x' + newXCoord + 'y' + newYCoord + 'z'+ newZCoord + '"} \n')
	
	def withinLimitXandYCoord(self, newXOrYCoord): #checks if the X or Y coordinates are within bounds
		
		if newXOrYCoord > float(parser.get('limits', 'xAndYMax')):
			print "New Xor Y coord: " , newXOrYCoord
			print "Limit: " , float(parser.get('limits', 'xAndYMax'))
			return False
		elif newXOrYCoord < float(parser.get('limits', 'xAndYMin')):	
			return False
		else:
			return True
			
	def withinLimitZCoord(self, newZCoord): #checks if the Z coordinate is within bounds
		if newZCoord < float(parser.get('limits', 'zMin')):
			return False
		elif newZCoord > float(parser.get('limits', 'zMax')):	
			return False
		else:
			return True
			
	def resetToOrigin(self): 
		print ser.write('{"gc":"g28"} \n')
		#print ser.write("G28 \n") 	
		global currentXCoord, currentYCoord, currentZCoord
		currentXCoord = 0
		currentYCoord = 0
		currentZCoord = 0

	def returnCurrentCoordinates(self):
		print "Current Coordinates: (" , currentXCoord ,"," , currentYCoord , "," , currentZCoord , ")"

#for testing purposes
while True:
	inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit) : ")
	if inputtedxCoord == 'r' :
		Stage().resetToOrigin()
		Stage().returnCurrentCoordinates()
		inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit) : ")
	elif inputtedxCoord == "q" :
		break
	else:
		pass
	inputtedyCoord = raw_input('Enter yCoord: ')
	inputtedzCoord = raw_input('Enter zCoord: ')
	
	inputtedxCoord = float(inputtedxCoord)
	inputtedyCoord = float(inputtedyCoord)
	inputtedzCoord = float(inputtedzCoord)
	
	Stage().move(inputtedxCoord, inputtedyCoord, inputtedzCoord)
	Stage().returnCurrentCoordinates()
	
