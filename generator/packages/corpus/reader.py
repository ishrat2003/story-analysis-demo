import os, datetime
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
from file.core import Core as File
from .topics import Topics
from store.local import Local
from .base import Base

class Reader(Base):
    
    def __init__(self, params):
        self.params = params
        path = params.source_directory
        self.store = Local()
        self.paths = {
            'gc': os.path.join(path, 'gc'),
            'words': os.path.join(path, 'words')
        }
        self.gcFileNames = [
            "topics",
            "person_topics",
            "organization_topics",
            "country_topics"
        ]
        return
    
    def getGcContentByDate(self, filename, start, end):
        topicsCollection = Topics(start, end)
        startYear, startMonth, startDay = [int(x) for x in start.split("-")]
        endYear, endMonth, endDay = [int(x) for x in end.split("-")]
        
        for year in list(range(startYear, endYear + 1)):
            if year < startYear or year > endYear:
                continue

            for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                if year == startYear and int(month) < startMonth:
                    continue
                if year == endYear and int(month) > endMonth:
                    continue
                allAll = (filename == 'country_topics')
                topics = self.getGcContent(filename, year, month)
                topicsCollection.append(topics, allAll)
                
        return topicsCollection
    
    def getGcContent(self, filename, year, month):
        if filename not in self.gcFileNames:
            return None
        
        filePath = self.paths['gc'] + '/' + str(year) + '/' + self._getFormattedMonthOrDay(month) + '/' + filename + '.json'
        return self.store.getContent(filePath)
    
    def getWordDetails(self, key):        
        filePath = self.paths['words'] + '/' + key + '/details.json'
        return self.store.getContent(filePath)
    
    
    def getAllDocumentsByWords(self, key, start = None, end = None):        
        directoryPath = self.paths['words'] + '/' + key
        wordDirectory = Directory(directoryPath)
        if not wordDirectory.exists():
            return None
        
        allDocs = []
        for year in wordDirectory.scan():                
            yearDirectoryPath = os.path.join(directoryPath, year)
            yearDirectory = Directory(yearDirectoryPath)
            for filename in yearDirectory.scan():
                filePath = yearDirectoryPath + '/' + filename
                fileContent = self.store.getContent(filePath)
                if fileContent:
                    for date in fileContent.keys():
                        if self.shouldValidDate(date, start, end):
                            allDocs += fileContent[date]

        return allDocs
