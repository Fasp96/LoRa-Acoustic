from network import LoRa
import socket
import time
import pycom

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

print('Starting')

pycom.heartbeat(False)
pycom.rgbled(0xFFFFFF) #set LED to WHITE

data1 = ''
fileName = ''
send = ''
SLEEP = 0

while True:
    received = s.recv(216)
    if received:
        print(received)
        pycom.rgbled(0xFF0000) # set LED to RED
        data = received.decode('utf-8') # recieves data and decodes from utf-8
        if data != data1 and str(data[:3]) == str("{0:0=3d}".format(len(data))):

            if data[3:] == 'temp' : #send temperature
                while send == '' or send == None:
                    send = ds18B20_temp.read_temp_async()
                    ds18B20_temp.start_conversion()

            elif data[3:13] == 'filename: ': #new fileName
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

            if send == '' :
                s.send(bytes('received', 'utf-8')) #sends back a message to notify that was recieved
                print('recieved')
            else:
                s.send(bytes('Temp = ' + str(send), 'utf-8'))
                send = ''
            #time.sleep (SLEEP)
    else:
        pycom.rgbled(0xFFFFFF) # set LED to WHITE
        time.sleep(SLEEP)
