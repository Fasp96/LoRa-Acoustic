import serial
import time
import os

port = '/dev/ttyACM0'#serial port connected
#port = '/dev/ttyS5'
bufferSize = 412 #chunck size being sent


def sendSerial(dirToBeSend): #main function to see if there are files to be sent
    while True:
        filesName = os.listdir(dirToBeSend) #List of files in the directory
	print (filesName)
        if(len(filesName) != 0):
            for i in filesName:
                sendFileLoPy(dirToBeSend + i)
                os.remove(dirToBeSend + i)

def sendFileLoPy (fileName): #function to transmit any file through serial

    global bufferSize

    startingTime = time. time() #gets initial time

    print('Sending file name...')
    file = fileName.split('/')
    file = file[-1]
    toSend = 'filename: ' + file
    sendLoPy(toSend) #sends the filename

    with open(fileName, 'r') as mFile: #reads content inside the file
        
        content = mFile.read() #reads all the content in the file

        for i in range(0, len(content), bufferSize): #for the length of the file

            print ('\n........')
            print ('\nsending... ' + str(time.time() - startingTime) + 's')
            print ('starting point: ' + str(i))

            toSend = content[i: i + bufferSize] #slipts in to chunks of the buffer sizer

            sendLoPy(toSend) #sends the buffer

        sendLoPy('Finish') #sends a 'finish' message when it sends everything

        print('***Done***')
        print('Transmission time for the ' + fileName + ' was ' + str(time.time() - startingTime) + 's')


def sendLoPy (toSend): #function to transmit of data to LoPy

    global s
    toSend = str("{0:0=3d}".format(len(toSend)+3)) + toSend #adds in the beginning the length of the buffer

    with serial.Serial( port, 115200, timeout = 10) as ser:
        while True:
            ser.write(bytes(toSend))# sends the buffer coded in uft-8

            timeOut = time.time() + 0.02
            while time.time() < timeOut: #waits for 2 seconds for message back from LoPy
                receivedMessage = ser.read(ser.in_waiting).decode('utf-8')
                
                if 'received' in receivedMessage: #if it receives 'received' breaks earlier
                    break

            if 'received' in receivedMessage: # is is received, sends a new buffer
                print('\n***received!***')
                receivedMessage = ''
                break

            else: #sends the same buffer again
                print('sending again...')

#sendFileLoPy('GOPR2049.txt')
