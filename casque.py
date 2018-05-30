#############################################
#
#   Helmet Guardian: Impact Force Monitor
#
#############################################
# Code by jenfoxbot <jenfoxbot@gmail.com>
# Code is open-source, coffee/beerware
# Please keep header :)
# If you like the content, consider
#    buying me a coffee/beer if ya see me 
#    or contributing to my patreon (jenfoxbot)
#    to support projects like this! :D
#############################################
#
# SO MANY THANKS to the wonderful folks who
#    make & document libraries.
#

####################################
# Libraries
####################################
#I2C library
import smbus

#GPIO
import RPi.GPIO as GPIO

#Other
import time, os, cv2, xlsxwriter


####################################
#        User Parameters
#    (Edit these as necessary)
####################################
#Set LIS331 address
addr = 0x18

#Set the acceleration range
maxScale = 16

#Set the LED GPIO pin
LED = 26

#Date pr le nom du fichier

Date=time.localtime()
Jour=Date.tm_mday
Mois=Date.tm_mon
Heure=Date.tm_hour
#Open file to save all data
#(creates new file in same folder if none
#and appends to existing file)
allData = open("AllSensorData.txt", "a")
allDataexcel=xlsxwriter.Workbook(str(Jour)+'_'+str(Mois)+'_'+str(Heure)+'.xlsx')
allworksheet=allDataexcel.add_worksheet()

#Open file to save alert data
#(creates new file in same folder if none
#and appends to existing file)
alrtData = open("AlertData.txt", "a")


####################################
# Initializations & Functions
# (Leave as-is unless you are
#   comfortable w/ code)
####################################
#LIS331 Constants (see Datasheet)
CTRL_REG1 = 0x20
CTRL_REG4 = 0x23
OUT_X_L = 0x28
OUT_X_H = 0x29
OUT_Y_L = 0x2A
OUT_Y_H = 0x2B
OUT_Z_L = 0x2C
OUT_Z_H = 0x2D

POWERMODE_NORMAL = 0x27
RANGE_2G = 0x00
RANGE_4g= 0x10
RANGE_8G = 0x20
RANGE_16G= 0x30


# Create I2C bus
bus = smbus.SMBus(1)

#Initialize GPIO and turn GPIO 26 to low
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

#Initiliaze LIS331
def initialize(addr, maxScale):
    scale = int(maxScale)
    #Initialize accelerometer control register 1: Normal Power Mode and 50 Hz sample rate
    bus.write_byte_data(addr, CTRL_REG1, POWERMODE_NORMAL)
    #Initialize acceleromter scale selection (6g, 12 g, or 24g). This example uses 24g
    if maxScale == 4:
        bus.write_byte_data(addr, CTRL_REG4, RANGE_4G)
    elif maxScale == 8:
        bus.write_byte_data(addr, CTRL_REG4, RANGE_8G)
    elif maxScale == 16:
        bus.write_byte_data(addr, CTRL_REG4, RANGE_16G)
    else:
        print "Error in the scale provided -- please enter 4, 8, or 16"


#Function to read the data from accelerometer
def readAxes(addr):
    data0 = bus.read_byte_data(addr, OUT_X_L)
    data1 = bus.read_byte_data(addr, OUT_X_H)
    data2 = bus.read_byte_data(addr, OUT_Y_L)
    data3 = bus.read_byte_data(addr, OUT_Y_H)
    data4 = bus.read_byte_data(addr, OUT_Z_L)
    data5 = bus.read_byte_data(addr, OUT_Z_H)
    #Combine the two bytes and leftshit by 8
    x = data0 | data1 << 8
    y = data2 | data3 << 8
    z = data4 | data5 << 8
    #in case overflow
    if x > 32767 :
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767 :
        z -= 65536
    #Calculate the two's complement as indicated in the datasheet
    x = ~x
    y = ~y
    z = ~z
    return x, y, z

#Function to calculate g-force from acceleration data
def convertToG(maxScale, xAccl, yAccl, zAccl):
    #Caclulate "g" force based on the scale set by user
    #Eqn: (2*range*reading)/totalBits (e.g. 48*reading/2^16)
    X = (2*float(maxScale) * float(xAccl))/(2**16);
    Y = (2*float(maxScale) * float(yAccl))/(2**16);
    Z = (2*float(maxScale) * float(zAccl))/(2**16);
    return X, Y, Z

def isDanger(timestamp, x, y, z):
    counter = 0
    x = long(x)
    y = long(y)
    z = long(z)
    if abs(x) > 9 or abs(y) > 9 or abs(z) > 9:
			print("Impact")
			alrtData.write(str(timestamp) + "\t" + "x: " + str(x) + "\t" + "y: " + str(y) + "\t" + "z: " +  str(z) + "\n")
			GPIO.output(LED, GPIO.HIGH)
			Video()
    elif abs(x) > 4 or abs(y) > 4 or abs(z) > 4:
            print("Impact")
            while abs(x) > 4 or abs(y) > 4 or abs(z) > 4:
                counter = counter + 1
                if counter > 4:
                    break
            if (counter > 4):
				alrtData.write(str(timestamp) + "\t" + "x: " + str(x) + "\t" + "y: " + str(y) + "\t" + "z: " + str(z) + "\n")
				GPIO.output(LED, GPIO.HIGH)
				Video()
			
def Video():
	tour=0
	if __name__ == "__main__":
		# find the webcam
		capture = cv2.VideoCapture(0)
		print("Debut Video")
		# video recorder
		fourcc = cv2.cv.CV_FOURCC(*'XVID')  # cv2.VideoWriter_fourcc() does not exist
		videoOut = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

		# record video
		while(capture.isOpened()):
			ret,frame = capture.read()
			if ret:
				videoOut.write(frame)
				tour=tour+1
				print(tour)
				if(tour>100):
					break
					
			else:
				break
			
			key=cv2.waitKey(1)
	print("Fin Video")
	capture.release()
	videoOut.release()
	cv2.destroyAllWindows()

####################################
#       Main Function
####################################
def main():
    print ("Starting stream")
    row1=0

	
    while True:
        #initialize LIS331 accelerometer
        initialize(addr, maxScale)
	
        #Start timestamp
        ts = time.ctime()
        
        #Write timestamp to AllSensorData file 
        allData.write(str(ts) + "\t")

        #Get acceleration data for x, y, and z axes
        xAccl, yAccl, zAccl = readAxes(addr)
        #Calculate G force based on x, y, z acceleration data
        x, y, z = convertToG(maxScale, xAccl, yAccl, zAccl)
        #Determine if G force is dangerous to human body & take proper action
        isDanger(ts, x, y, z)

        #Write all sensor data to file AllSensorData (as you probably guessed :) )
        allData.write("x: " + str(x) + "\t" + "y: " + str(y) + "\t" + "z: " + str(z) + "\n")
        allworksheet.write(row1,0,x)
        allworksheet.write(row1,1,y)
        allworksheet.write(row1,2,z)
		
        row1=row1+1
        #print G values (don't need for full installation)
        print "Acceleration in X-Axis : %d" %x
        print "Acceleration in Y-Axis : %d" %y
        print "Acceleration in Z-Axis : %d" %z
        print "\n"

        #Short delay to prevent overclocking computer
        time.sleep(0.2)

    #Run this program unless there is a keyboard interrupt
    try:
        while True:
            pass
    except KeyboardInterrupt:
		
        myprocess.kill()
        allData.close()
        alrtData.close()
        GPIO.cleanup()
		
		


if __name__ =="__main__":
    main()
    allData.close()
    alrtData.close()
    GPIO.cleanup()