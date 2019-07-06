import os
import time
import datetime
#from PIL import Image

def compressFile(fileDir, compressDir, doneDir):

        fileName = fileDir.split('/')
        fileName = fileName[-1]

        if fileName[-4:] == '.JPG' or fileName[-4:] == '.wav':

                if fileName[-4:] == '.JPG':

                        # Reduce photo size
                        foo = Image.open(fileDir)
                        (4000,3000) # Original image resolution

		        # Downsize the image with an ANTIALIAS filter (gives the highest quality)
                        foo = foo.resize((500,375),Image.ANTIALIAS)

                        # Saving photo
                        foo.save(compressDir + fileName, quality=95)

                if fileName[-4:] == '.wav':

                        #converts the .wav file to a .mp3 file and saves
	                os.system( 'ffmpeg -i ' + fileDir + ' -vn -ar 48000 -ac 2 -b:a 192k ' + compressDir + fileName[:-4] + '.mp3')

                #moves to a different folder as backup
                os.rename(fileDir, doneDir + fileName)

                return (fileName[:-4] + '.mp3')

        else:
                print('*****Can\'t Convert The File*****\n')

#compressFile('Captured/Sounds/Recorded/2019-07-04_12-44.wav', 'Compressed/Sounds/', 'Captured/Sounds/Backup/')
