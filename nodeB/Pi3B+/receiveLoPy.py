import serial
import time
import os

port = '/dev/ttyACM0' #serial port connected

def receiveLoPy():

    SLEEP = 0.03
    data1 = ''
    fileName = ''
    send = ''
    dirToSave = 'Received/'
    
    with serial.Serial(port, 115200, timeout = 10) as ser:
        while True:
            data = ser.read(ser.in_waiting).decode('utf-8')
            
            if data != data1 and str(data[:3]) == str("{0:0=3d}".format(len(data))):
                print(data)
                if data[3:13] == 'filename: ': #new fileName

                    fileName += data[13:]
                    fileWrite = open(fileName, 'w').close() #clear ever$

                elif data[3:] == 'Finish': #finished message
                    fileName = dirToSave

                else: # writes inside of the file
                    
                    data = data[3:]
                    fileWrite = open(fileName, 'a') #opens to write inside
                    fileWrite.write(data) #writes inside the data
                    fileWrite.close() #close file
                    data1 = data
                    print (data1)

                ser.write(bytes('received')) #sends back a message to notify that was recieved
                time.sleep (SLEEP)

            elif data == data1:
                ser.write(bytes('received')) #sends back a message to notify that was recieved
                time.sleep (SLEEP)
            else:
                time.sleep(SLEEP)

receiveLoPy()
