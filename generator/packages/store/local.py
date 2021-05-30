from file.json import Json as JsonFile

class Local:
    
    def getContent(self, filePath):
        file = JsonFile()
        try:
            return file.read(filePath)
        except:
            return None
        
        

