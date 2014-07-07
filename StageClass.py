import serial
from ConfigParser import SafeConfigParser
import fileinput, sys

parser = SafeConfigParser()
parser.read('C:\\Python27\\Lib\\idlelib\\config.txt')

ser = serial.Serial("COM3", 115200, timeout = None)

copyOfLastXCoord = parser.get('coordinates of last run', 'x')
copyOfLastYCoord = parser.get('coordinates of last run', 'y')
copyOfLastZCoord = parser.get('coordinates of last run', 'z')

currentXCoord = float(parser.get('coordinates of last run', 'x'))
currentYCoord = float(parser.get('coordinates of last run', 'y'))
currentZCoord = float(parser.get('coordinates of last run', 'z'))
	

class Stage:
	#keeps track of current coordinates
	
	def move(self, newXCoord, newYCoord, newZCoord): #moves to new coordinates
		global currentXCoord, currentYCoord, currentZCoord
		
		if relativeCoords == True:
			newXCoord += currentXCoord 
			newYCoord += currentYCoord
			newZCoord += currentZCoord
		
		if self.withinLimitXandYCoord(newXCoord) == False:
			print "XCoord - Not in range. Must be between " + parser.get('limits', 'xAndYMin') + " and " + parser.get('limits', 'xAndYMax')
			newXCoord = currentXCoord	#will not move from current position
		if self.withinLimitXandYCoord(newYCoord) == False:
			print "YCoord - Not in range. Must be between " + parser.get('limits', 'xAndYMin') + " and " + parser.get('limits', 'xAndYMax')
			newYCoord = currentYCoord
		if self.withinLimitZCoord(newZCoord) == False:
			print "ZCoord - Not in range. Must be between " + parser.get('limits', 'zMin') + " and " + parser.get('limits', 'zMax')
			newZCoord = currentZCoord	
		
		currentXCoord = newXCoord  
		currentYCoord = newYCoord
		currentZCoord = newZCoord	
		print ser.write('{"gc":"g0 x' + str(newXCoord) + 'y' + str(newYCoord) + 'z'+ str(newZCoord) + '"} \n')
	##def moveRelative(self, newXCoord, newYCoord, newZCoord):
		
	def withinLimitXandYCoord(self, newXOrYCoord): #checks if the X or Y coordinates are within bounds
		
		if newXOrYCoord > float(parser.get('limits', 'xAndYMax')):
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
		#print ser.write('{"gc":"g28"} \n')
		print ser.write('{"gc":"g0 x0 y0 z0"} \n')
		#print ser.write("G28 \n") 	
		global currentXCoord, currentYCoord, currentZCoord
		currentXCoord = 0
		currentYCoord = 0
		currentZCoord = 0

	def returnCurrentCoordinates(self):
		print "Current Coordinates: (" , currentXCoord ,"," , currentYCoord , "," , currentZCoord , ")"

#for testing purposes
while True:
	quit = False
	absoluteOrRelativeCoordinates = raw_input("Absolute or relative coordinates? (a/r): ")
	
	#if absoluteOrRelativeCoordinates == 'a':
	relativeCoords = False 		
	if absoluteOrRelativeCoordinates == 'r':
		relativeCoords = True	
	
	inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit): ")
	if inputtedxCoord == 'r' :
		Stage().resetToOrigin()
		Stage().returnCurrentCoordinates()
		absoluteOrRelativeCoordinates = raw_input("Absolute or relative coordinates? (a/r): ")
		if absoluteOrRelativeCoordinates == 'r':
			relativeCoords = True
		inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit): ")
		
	if inputtedxCoord == 'q' :
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True):
			line = line.replace("x = " + copyOfLastXCoord, "x = " + str(currentXCoord))
			sys.stdout.write(line) # sys.stdout is redirected to the file
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True):	
			line = line.replace("y = " + copyOfLastYCoord, "y = " + str(currentYCoord))
			sys.stdout.write(line)
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True):	
			line = line.replace("z = " + copyOfLastZCoord, "z = " + str(currentZCoord))
			sys.stdout.write(line)
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
	

	
