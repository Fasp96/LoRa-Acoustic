import multiprocessing
import time
from recordSound import recordSound
from compressFile import compressFile
from convBase64 import convBase64
from sendLoPy import sendSerial

secRec = 3 #files size
recDir = 'Captured/Sounds/Recorded/' # directory to folder to save sound files
doneDir = 'Captured/Sounds/Backup/' # directory to folder save sound files for backup
compressDir = 'Compressed/Sounds/' # directory to folder to save compressed sound files
base64Dir = 'Base64/Sounds/' #directory to save base64 files

def soundCompiler():
        fileRec = recordSound(recDir, secRec)
        print('**Sound recorded: ' + fileRec)
        fileCompress = compressFile(recDir + fileRec, compressDir, doneDir)
        print('**Sound compressed: ' + fileCompress)
        base64File = convBase64(compressDir + fileCompress, base64Dir)
        print('**Sound Converted to Base64: ' + base64File)

sC = multiprocessing.Process(target = soundCompiler)
Sc = multiprocessing.Process(target = sendSerial, args =(base64Dir,))

#sC.start()
Sc.start()
