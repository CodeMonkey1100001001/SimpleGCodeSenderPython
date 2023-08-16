#!/usr/bin/python
# tested on kubuntu 21.10
# test on raspberry pi OS
# modified from https://github.com/bborncr/gcodesender.py/tree/master
import serial
import time
import argparse

parser = argparse.ArgumentParser(description='Command line basic gcode sender for marlin polargraph')
parser.add_argument('-p','--port',help='Input USB port',required=True)
parser.add_argument('-b','--bps',help='USB bps',required=False,default=115200)
parser.add_argument('-f','--file',help='Gcode file to send',required=True)
args = parser.parse_args()
 
## show values ##
print ("USB Port: %s" % args.port )
print ("USB Speed: %s" % args.file )
print ("Gcode file: %s" % args.file )

# check for ; in line if there is no ; then send line else send the line up to the comment
def removeComment(string):
	if (string.find(';')==-1):
		return string
	else:
		return string[:string.index(';')]
 
# Open serial port
#s = serial.Serial('/dev/ttyACM0',115200)
s = serial.Serial(args.port,115200)
print( 'Opening Serial Port')
 
# Open g-code file
#f = open('/media/UNTITLED/shoulder.g','r');

num_lines = sum(1 for _ in open(args.file))


f = open(args.file,'r');
print ('Opening g-code file')
 
# Wake up 
s.write(b"\r\n\r\n") # Hit enter a few times to wake the Printrbot
waitCount = 3
print("Waiting for",waitCount,"seconds")
for i in range(0,waitCount):
	print("Boot ",i+1)
	time.sleep(1)   # Wait for Printrbot to initialize
s.flushInput()  # Flush startup text in serial input
print('Sending gcode')
 
# Stream g-code
lineCount = 0

startTime = time.time()

for line in f:
    lineCount += 1
    l = removeComment(line)
    l = l.strip() # Strip all EOL characters for streaming
    if  (l.isspace()==False and len(l)>0) :
        print( 'Sending: ' + l)
        toSend = l + '\n'
        toSend = toSend.encode('utf_8')
        s.write(toSend) # Send g-code block
        grbl_out = s.read_until(b'ok\n')
        #grbl_out = s.readline() # Wait for response with carriage return
        grbl_out_str = grbl_out.decode('utf_8')
        percentFinished = (lineCount/num_lines)*100
        timeNow = time.time()
        elapsedTime = timeNow - startTime
        print ("T", f'{timeNow:.1f}',
            f'{percentFinished:.1f}%',
            "Line",lineCount," of ", num_lines,
            "Run Time",
            f'{elapsedTime:.1f}s',":" + grbl_out_str.strip(),sep=",")

# Wait here until printing is finished to close serial port and file.
# raw_input("  Press <Enter> to exit.")
 
# Close file and serial port
f.close()
s.close()
