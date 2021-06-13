class Processor:
    
    def __init__(self, loader, writer, totalItems = 0):
        self.loader = loader
        self.writer = writer
        self.totalItems = int(totalItems)
        self.totalProcessed = 0
        return
    
    def setHeaders(self, headers):
        self.loader.setHeaders(headers)
        return
    
    def setSourceFileName(self, name):
        self.writer.setSourceFileName(name)
        return
    
    def process(self, fileContent):
        loadedContent = self.loader.getDetails(fileContent)
        
        if not loadedContent:
            return False
        
        loadedContent = loadedContent[0: self.totalItems] if self.totalItems else loadedContent
        self.writer.save(loadedContent)
        return True
