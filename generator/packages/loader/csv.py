class CSV:
    
    def __init__(self):
        self.headers = {}
        return
    
    def setHeaders(self, headers):
        index = 0
        for item in headers:
            self.headers[item] = index
            index += 1
        return

    def getDetails(self, fileContent):
        if not len(fileContent):
            return None

        processedLines = []
        for line in fileContent:
            processedLines.append(self.convert(line))
        return processedLines
    
    
    def convert(self, line):
        data = {}
        for item in self.headers.keys():
            data[item] = line[self.headers[item]]
        return data