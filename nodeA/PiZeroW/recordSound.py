import os
import time
import datetime

# function to record sound
def recordSound(recDir, seconds):
	try:
		dt = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
		os.system( 'arecord ' + recDir + str(dt) + '.wav -D sysdefault:CARD=1 -f dat -v -d ' + str(seconds))
	except RuntimeError:
		print('Error')

	return (dt + '.wav')

#function to compress sound files
def compressSound(recDir, compressDir, doneDir):
	#gets fileName
	fileName = recDir.split('/')
	fileName = fileName[-1]

	#converts the .wav file to a .mp3 file and saves
	os.system( 'ffmpeg -i ' + recDir + fileName + ' -vn -ar 48000 -ac 2 -b:a 192k ' + compressDir + fileName[:-4]+ '.mp3')
	#moves to a different folder as backup
	os.rename(recDir + fileName, doneDir + fileName)


# Testing
#recordSound('../Captured/Sounds/Recorded/', 300)
#compressSound('../Captured/Sounds/Recorded/2019-05-29_12:49.wav', '../Compressed/Sounds/', '../Captured/Sounds/Backup/')
