import serial
from ConfigParser import SafeConfigParser
import fileinput, sys

parser = SafeConfigParser()
fp = open('C:\\Python27\\Lib\\idlelib\\config.txt')
parser.readfp(fp)
fp.close()
ser = serial.Serial("COM3", 115200, timeout = None)

copyOfLastXCoord = parser.get('coordinates of last run', 'x')
copyOfLastYCoord = parser.get('coordinates of last run', 'y')
copyOfLastZCoord = parser.get('coordinates of last run', 'z')

currentXCoord = float(parser.get('coordinates of last run', 'x'))
currentYCoord = float(parser.get('coordinates of last run', 'y'))
currentZCoord = float(parser.get('coordinates of last run', 'z'))
	


class Stage:
	#keeps track of current coordinates
	
	def move(self, newXCoord, newYCoord, newZCoord, relativeCoords): #moves to new coordinates
		global copyOfLastXCoord, copyOfLastYCoord, copyOfLastZCoord
		fp = open('C:\\Python27\\Lib\\idlelib\\config.txt')
		parser.readfp(fp)

		copyOfLastXCoord = parser.get('coordinates of last run', 'x')
		copyOfLastYCoord = parser.get('coordinates of last run', 'y')
		copyOfLastZCoord = parser.get('coordinates of last run', 'z')
		fp.close()
		
		global currentXCoord, currentYCoord, currentZCoord
		
		if relativeCoords == True:
			newXCoord += currentXCoord  #calculates new coordinate to move to
			newYCoord += currentYCoord
			newZCoord += currentZCoord
		
		if self.withinLimitXandYCoord(newXCoord) == False:
			print "XCoord - Not in range. Must be between " + parser.get('limits', 'xAndYMin') + " and " + parser.get('limits', 'xAndYMax')
			newXCoord = currentXCoord	#will not move from current position
		if self.withinLimitXandYCoord(newYCoord) == False:
			print "YCoord - Not in range. Must be between " + parser.get('limits', 'xAndYMin') + " and " + parser.get('limits', 'xAndYMax')
			newYCoord = currentYCoord #will not move from current position
		if self.withinLimitZCoord(newZCoord) == False:
			print "ZCoord - Not in range. Must be between " + parser.get('limits', 'zMin') + " and " + parser.get('limits', 'zMax')
			newZCoord = currentZCoord #will not move from current position
		
		currentXCoord = newXCoord  #updates value of current coordinates
		currentYCoord = newYCoord
		currentZCoord = newZCoord	
		
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True): #updates coordinates in file
			line = line.replace("x=" + copyOfLastXCoord, "x=" + str(currentXCoord))
			sys.stdout.write(line) # sys.stdout is redirected to the file
		
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True):	
			line = line.replace("y=" + copyOfLastYCoord, "y=" + str(currentYCoord))
			sys.stdout.write(line)
		
		for line in fileinput.input("C:\\Python27\\Lib\\idlelib\\config.txt", inplace=True):	
			line = line.replace("z=" + copyOfLastZCoord, "z=" + str(currentZCoord))
			sys.stdout.write(line)
		
		fileinput.close()
		
		fp = open('C:\\Python27\\Lib\\idlelib\\config.txt')
		parser.readfp(fp)
		copyOfLastXCoord = parser.get('coordinates of last run', 'x') #update last X Coord - now last X Coord = current X Coord
		copyOfLastYCoord = parser.get('coordinates of last run', 'y')
		copyOfLastZCoord = parser.get('coordinates of last run', 'z')
		fp.close()
		
		print ser.write('{"gc":"g0 x' + str(newXCoord) + 'y' + str(newYCoord) + 'z'+ str(newZCoord) + '"} \n') #moves
		
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
			
	def returnCurrentCoordinates(self):
		print "Current Coordinates: (" , currentXCoord ,"," , currentYCoord , "," , currentZCoord , ")"

#for testing purposes
def main():
	stage = Stage()
	while True:
		quit = False
		absoluteOrRelativeCoordinates = raw_input("Absolute or relative coordinates? (a/r): ")
		
		relativeCoords = False 		
		if absoluteOrRelativeCoordinates == 'r':
			relativeCoords = True	
		
		inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit): ")
		if inputtedxCoord == 'r' :
			stage.move(0, 0, 0, False)
			stage.returnCurrentCoordinates()
			absoluteOrRelativeCoordinates = raw_input("Absolute or relative coordinates? (a/r): ")
			if absoluteOrRelativeCoordinates == 'r':
				relativeCoords = True
			inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit): ")
			
		if inputtedxCoord == 'q' :
			break
		else:
			pass
		inputtedyCoord = raw_input('Enter yCoord: ')
		inputtedzCoord = raw_input('Enter zCoord: ')
			
		inputtedxCoord = float(inputtedxCoord)
		inputtedyCoord = float(inputtedyCoord)
		inputtedzCoord = float(inputtedzCoord)
		

		stage.move(inputtedxCoord, inputtedyCoord, inputtedzCoord, relativeCoords)
		stage.returnCurrentCoordinates()
		

if __name__ == '__main__':
	main()
