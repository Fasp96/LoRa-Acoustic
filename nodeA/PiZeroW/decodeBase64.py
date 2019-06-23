import base64

def decodeBase64(fileDir, dirSave):

        with open(fileDir, 'rb') as fileRead:
                str = base64.b64decode(fileRead.read()) # Converts in to .mp3 file

                #gets fileName
                fileName = fileDir.split('/')
                fileName = fileName[-1]

                fileName = fileName[:-4] + '.mp3'

                dirSave += fileName 
                
                fileWrite = open(dirSave, 'wb') #  Opens to write inside
                fileWrite.write(str) # Writes inside the string
                fileWrite.close() # Closes file

        return fileName

#decodeBase64('Base64/Sounds/2019-05-29_11:02.txt', 'Base64/Sounds/')
