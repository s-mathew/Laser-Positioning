import matplotlib.pyplot as plt
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('C:\\Python27\\Lib\\idlelib\\xyData1.txt')

xValue = float(parser.get('xyValues', 'x'))
yValue = float(parser.get('xyValues', 'y'))
RMSx = float(parser.get('RMS', 'RMSx'))
RMSy = float(parser.get('RMS', 'RMSy'))

xAxisxValue = [xValue]
yAxisyValue = [yValue]
xAxisRMSxValue = [xValue - RMSx]
yAxisRMSyValue = [yValue - RMSy]


im = plt.imread("C:\Users\Home\Desktop\PlanckianLocus.png")
plt.xlabel('x')
plt.ylabel('y', rotation=0)
plt.xlim([0, 0.8])
plt.ylim([0, 0.9])

implot = plt.imshow(im, zorder=0, extent=[0.0, 0.8, 0.0, 0.9])
plt.plot([xAxisxValue],[yAxisyValue],'bo')
plt.plot([xAxisRMSxValue],[yAxisRMSyValue],'ro')
plt.title('xy Chromaticity')
plt.show()