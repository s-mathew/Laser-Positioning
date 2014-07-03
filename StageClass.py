import serial
ser = serial.Serial("COM3", 115200, timeout = None)
class Stage:
	#keeps track of current coordinates
	x = 0
	y = 0
	z = 0
	
	def move(self, xCoord, yCoord, zCoord):
		print ser.write('{"gc":"g0 x' + xCoord + 'y' + yCoord + 'z'+ zCoord + '"} \n')
		x = xCoord
		y = yCoord
		z = zCoord
	def resetToOrigin(self):
		print ser.write('{"gc":"g28"} \n')
		#print ser.write("G28 \n") 	
		x = 0
		y = 0
		z = 0

#for testing purposes
while True:
	inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit) : ")
	if inputtedxCoord == 'r' :
		Stage().resetToOrigin()
		inputtedxCoord = raw_input("Enter xCoord (or 'r' to reset to origin or 'q' to quit) : ")
	elif inputtedxCoord == "q" :
		break
	else:
		pass
	inputtedyCoord = raw_input('Enter yCoord: ')
	inputtedzCoord = raw_input('Enter zCoord: ')
	 
	Stage().move(inputtedxCoord, inputtedyCoord, inputtedzCoord)
	print "New Coordinates: (" + x +", " + y + ", " + z + ")"
