#from receiveLoPy import receiveLoPy
from decodeBase64 import decodeBase64
import multiprocessing
import os

receivedDir = "Received/" #directory to folder to save received sounds
soundClipDir = "Sounds/" #directory to save sound clips in base64

def decBase64():

    if(len(os.listdir(receivedDir))!= 0):
        for f in os.listdir(receivedDir):
            
            decodeBase64(receivedDir + f, soundClipDir)
            os.remove(receivedDir + f)

#rL = multiprocessing.Process(target = receiveLoPy)
dB = multiprocessing.Process(target = decBase64)

#rL.start()
dB.start()
