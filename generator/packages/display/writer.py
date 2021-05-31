import os, datetime
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
from file.core import Core as File

class Writer(Base):
    
    def __init__(self, path, params):
        super().__init__(path)
        self.params = params
        self.paths = {
            'gc': os.path.join(path, 'gc'),
            'termsboard': os.path.join(path, 'termsboard'),
            'lc': os.path.join(path, 'lc')
        }
        self.termsboardPath = os.path.join(path, 'termsboard')
        self.lcPath = File.join(path, "lc")
        self.file = JsonFile()
        return
    
    def save(self, data, type):
        if not data or type not in self.paths.keys():
            return
        
        filePath = self.getFilePath(data, type)
        self.file.remove(filePath)
        self.file.write(filePath, data)
        return
    
    def getFilePath(self, data, type):
        path = self.paths[type]
        filename = self.__getFilename(type, data)
        return path + '/' + filename
    
    def __getDocumentKey(self, link):
        urlParts = link.split('/')
        return urlParts.pop()
    
    def __getFilename(self, type, data):
        if type == 'gc':
            return str(self.params.start) + '_' + str(self.params.end) + '.json'
        if type == 'lc':
            return self.__getDocumentKey(data['link']) + '.json'
        if type == 'termsboard':
            return data['main_topic']['stemmed_word'] + '.json'
        return ''

