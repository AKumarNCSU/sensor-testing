#Talha: most modern 7156 reader ever. Use low level programming to speed up data rate

#Pass in inputs like
#	python SingleLineLog.py comport filename
#	python SingleSensorGraph_Wireless.py COM7 CottonShieldexCycle_1.txt

import serial
import os
import numpy as np
import time
import logging
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

print ("This is the name of the script: ", sys.argv[0])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))

#inputs to the program:
filename_arg = sys.argv[2]
comport = sys.argv[1]

#global variables
counter = 1 
subtVal = 192
rangeC = 4
x = [0]*100 
y = [0]*100 
lastBiasVal = 0

#logging setup
logging.basicConfig(filename=filename_arg, level=logging.DEBUG, format='%(relativeCreated)d, %(message)s')
ser =  serial.Serial(comport, 57600, timeout=1)
time.sleep(2)
ser.write('2')

#graph setup
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def clipper(inp, max, min):
	res = inp
	if (inp>max):
		res = max
	if (inp<min):
		res = min
	return res

def themath(splitted):
	global Data_Matrix
	rawCh = clipper(int(splitted[2]), 53248,12288)
	capData = ((rawCh - 12288.0) * rangeC)/40960.0
	capdacBias = int(splitted[3]) - subtVal
	#some magic here to add the autocapdac because every cap val is about 0.2pF of inc. Experimentally. 
	capData = capData+capdacBias*0.2
	return capData

def takeReading(i):
        global counter
        global x
        global y
        global lastBiasVal
        line = ser.readline().strip()
        print (line)
        splitted = line.split(',')
        if counter > 9 and len(splitted)==6:# and lastBiasVal==splitted[3]:
            curCap = themath(splitted)
            numpyify = np.array([int(splitted[5])/1000.0, curCap])
            data_Comp = '{0:s}, {1:}, {2:}, {3:.3f}, {4:0.3f}'.format(splitted[1],splitted[0],splitted[4], numpyify[0], numpyify[1])
            print(data_Comp)
            logging.debug(data_Comp)
            x_new = numpyify[0]
            y_new = numpyify[1]
            del x[0]
            del y[0]
            x.append(x_new)
            y.append(y_new)
        if counter > 8:
                lastBiasVal = splitted[3]
        ax1.clear()
        ax1.plot(x, y)
        counter+=1 

ani = animation.FuncAnimation(fig, takeReading, interval=10)
plt.show()

