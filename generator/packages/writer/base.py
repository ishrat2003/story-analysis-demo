import os, datetime
from file.json import Json as JsonFile

class Base:

    def __init__(self, path):
        self.path = path
        self.file = JsonFile()
        return
    
    def getPath(self):
        return self.path
    
    def getFilePath(self, dirPath, filename):
        return os.path.join(dirPath, filename + '.json')
    
    def _strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def _getFormattedMonthOrDay(self, number):
        intNumber = int(number)
        if intNumber < 10:
            return '0' + str(intNumber)
        return number
        
