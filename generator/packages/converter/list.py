import json, datetime, re, os
import sys
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile

class List(Base):
    
    def __init__(self, path):
        super().__init__(path)
        
        self.documentPath = os.path.join(path, 'documents')
        documentsDirectoryPath = Directory(self.documentPath)
        documentsDirectoryPath.create()
        
        self.listPath = os.path.join(path, 'lists')
        listDirectoryPath = Directory(self.listPath)
        listDirectoryPath.create()
        
        self.file = JsonFile()
        self.sourceFileName = None
        self.__reset()
        return
    
    def setSourceFileName(self, name):
        self.sourceFileName = re.sub(r'\..+', r'', name)
        return
    
    def save(self, data):
        if not len(data):
            return
        
        lists = []
        for item in data:
            listItem = {
                'filename': re.sub(r'^.+\/([a-zA-Z0-9\-]+)$', r'\1', item['url']) + '.json',
                'title': item['name'],
                'description': item['meta_description'],
                'link': item['url'],
                'pubDate': item['date']
            }
            item['pubDate'] = item['date']
            lists.append(listItem)

            filePath = self.documentPath + '/' + listItem['filename']
            self.file.write(filePath, item)
            
        filePath = self.listPath + '/' + self.sourceFileName + '.json'
        self.file.write(filePath, lists)
        return

    
    def __reset(self):
        return
