from network import LoRa
from machine import UART
import socket
import time
import pycom
import os
import _thread

pycom.heartbeat(False)
pycom.rgbled(0xFFFFFF)


def UARTtransmission():

    uart1 = UART(0, 115200, bits = 8, parity = None, stop = 1)
    uart1.init(baudrate = 115200, bits = 8, parity = None, stop = 1)

    SLEEP = 0.03
    data1 = ''
    fileName = ''
    send = ''

    while True:
        if(uart1.any()):
            pycom.rgbled(0xFF0000) # set LED to RED
            data = uart1.readall().decode('utf-8') # recieves data and decodes from utf-8

            if data != data1 and str(data[:3]) == str("{0:0=3d}".format(len(data))):

                if data[3:13] == 'filename: ': #new fileName
                    fileName = data[13:]
                    fileWrite = open(fileName, 'w').close() #clear ever$

                elif data[3:] == 'Finish': #finished message
                    fileName = ''
                    pycom.rgbled(0xFFFFFF) # set LED to WHITE

                else: # writes inside of the file
                    data = data[3:]
                    fileWrite = open(fileName, 'a') #opens to write insi$
                    fileWrite.write(data) #writes inside the data
                    fileWrite.close() #close file
                    data1 = data
                    print (data1)

                uart1.write(bytes('received', 'utf-8')) #sends back a message to notify that was recieved
                time.sleep (SLEEP)

            elif data == data1:
                uart1.write(bytes('received', 'utf-8')) #sends back a message to notify that was recieved
                time.sleep (SLEEP)
            else:
                pycom.rgbled(0xFFFFFF) # set LED to WHITE
                time.sleep(SLEEP)

####################################################


bufferSize = 210 #chunk size being sent
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def sendNodeSender(): #main function for the transission between LoPy throught LoRa
    while True:

        filesName = []

        for file in os.listdir():
            if file.endswith(".txt"):
                filesName.append(file)

        if(len(filesName) != 0):
            for i in filesName:
                sendFileLoRa(i)
                os.remove(i)


def sendFileLoRa (fileName): #function to transmit any file through LoRa

    global bufferSize

    startingTime = time.time() #gets initial time

    print('Send file name ...')
    toSend = 'filename: ' + fileName
    sendLora (toSend) #sends the filename

    with open(fileName, 'r') as mFile: #reads content inside the file

        content = mFile.read() #reads all the content in the file

        for i in range(0, len(content), bufferSize): #for the length of the file

            print ('\n........')
            print ('\nsending... ' + str(time.time() - startingTime) + 's')
            print ('starting point: ' + str(i))

            toSend = content[i: i + bufferSize] #slipts in to chunks of the buffer sizer

            sendLora(toSend) #sends the buffer

    sendLora('Finish') #sends a 'finish' message when it sends everything

    print('***Done***')
    print('Transmission time for the ' + fileName + ' was ' + str(time.time() - startingTime) + 's')


def sendLora (toSend): #funtion that is resposible for the transmission of the data between LoRas

    global lora, s

    pycom.rgbled(0xFF0000) # set LED to RED

    toSend = str("{0:0=3d}".format(len(toSend)+ 3)) + toSend #adds in the beginning the length of the buffer

    while True:

        s.send(bytes(toSend, 'utf-8')) #sends the buffer coded in utf-8
        receivedMessage = ''

        while time.time() < time.time() + 0.2: #waits for 2 seconds for message back from LoPy
                receivedMessage = s.recv(216).decode('utf-8')

                if 'received' in receivedMessage:
                    break

        if 'received' in receivedMessage: #if is recieved, sends a new buffer
            print('\n***received!***')
            pycom.rgbled(0xFFFFFF) #set LED to WHITE
            break

        else: #sends the same buffer again
            print('sending again...')

'''
_thread.start_new_thread(UARTtransmission, ())
_thread.start_new_thread(sendNodeSender, ())
'''

#UARTtransmission()
sendNodeSender()
#sendFileLoRa('GOPR2049.txt')
