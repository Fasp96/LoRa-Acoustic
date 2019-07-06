from network import LoRa
from machine import UART
import socket
import time
import pycom
import os

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

print('Starting')

pycom.heartbeat(False)
pycom.rgbled(0xFFFFFF) #set LED to WHITE

def receiveLoRa():

    data1 = ''
    fileName = ''
    SLEEP = 0

    while True:
        received = s.recv(216)
        if received:
            print(received)
            pycom.rgbled(0xFF0000) # set LED to RED
            data = received.decode('utf-8') # recieves data and decodes from utf-8
            if data != data1 and str(data[:3]) == str("{0:0=3d}".format(len(data))):

                if data[3:13] == 'filename: ': #new fileName
                    fileName = data[13:]
                    fileWrite = open (fileName, 'w').close() #clear ever$

                elif data[3:] == 'Finish': #finished message
                    fileName = ''

                else: # writes inside of the file
                    if(fileName != ''):
                        data = data[3:]
                        fileWrite = open(fileName, 'a') #opens to write insi$
                        fileWrite.write(data) #writes inside the data
                        fileWrite.close() #close file
                        data1 = data
                        print (data1)


                s.send(bytes('received', 'utf-8')) #sends back a message to notify that was recieved
                print('recieved')
        else:
            pycom.rgbled(0xFFFFFF) # set LED to WHITE
            time.sleep(SLEEP)

###################################################################################

def UARTtransmission(): #function to know if there are files to transmit
    filesName = []

    while True:

        for file in os.listdir():
            if file.endswith('.txt'):
                filesName.append(file)

        if(len(filesName) != 0):
            for i in filesName:
                sendFileUART(i)
                os.remove(i)

def sendFileUART(fileName): #funtion to transmit any file through UART

    bufferSize = 412 #size of the buffer to send each time

    startingTime = time.time() #gets initial time

    print('Send file name...')
    toSend = 'filename: ' + fileName
    sendRPi(toSend) #sends filename

    with open(fileName, 'r') as mFile: #reads content inside the file

        content = mFile.read() #reads all the content in the file

        for i in range(0, len(content), bufferSize): #for the length of the file

            print ('\n........')
            print ('\nsending... ' + str(time.time() - startingTime) + 's')
            print ('starting point: ' + str(i))

            toSend = content[i: i + bufferSize] #slipts in to chunks of the buffer sizer

            sendRPi(toSend) #sends the buffer

        sendRPi('Finish') #sends a 'finish' message when it sends everything

        print('***Done***')
        print('Transmission time for the ' + fileName + ' was ' + str(time.time() - startingTime) + 's')

def sendRPi(toSend): #function to transmit data to RPi

    uart1 = UART(0, 115200, bits = 8, parity = None, stop = 1)
    uart1.init(baudrate = 115200, bits = 8, parity = None, stop = 1)

    toSend = str("{0:0=3d}".format(len(toSend)+3)) + toSend #adds in the beginning the length of the buffer

    while True:
        uart1.write(bytes(toSend, 'utf-8'))
        receivedMessage = ''
        timeOut = time.time() + 0.02
        while time.time() < timeOut: #waits for 0.02 seconds for message back from RPi
            if (uart1.any()):
                receivedMessage = uart1.readall().decode('utf-8')

                if 'received' in receivedMessage: #if receives 'received' breaks earlier
                    break

        if 'received' in receivedMessage: #if is received,sends a new buffer
            print('\n***received!***')
            break
        else: #sends the same buffer again
            print('\nsend again...')

#receiveLoRa()
#UARTtransmission()
