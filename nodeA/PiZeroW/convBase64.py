import base64

def convBase64(fileDir, dirSave):

        with open(fileDir, 'rb') as fileRead:
                str = base64.b64encode(fileRead.read()) # Converts in to base64 character

                #gets fileName
                fileName = fileDir.split('/')
                fileName = fileName[-1]

                fileName = fileName[:-4] + '.txt'

                dirSave += fileName 
                
                fileWrite = open(dirSave, 'wb') #  Opens to write inside
                fileWrite.write(str) # Writes inside the string
                fileWrite.close() # Closes file

        return fileName

#convBase64('../Compressed/Sounds/2019-05-29_11:02.mp3', '../Base64/Sounds/')
