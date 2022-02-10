import json, datetime, re, os
import sys
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
import numpy as np

class User(Base):
    
    def __init__(self, path):
        super().__init__(path)
        
        self.documentsDirectoryPath = path
    
        self.file = JsonFile()
        self.sourceFileName = None
        self.list = {}
        self.__reset()
        return
    
    def setSourceFileName(self, name):
        self.sourceFileName = re.sub(r'\..+', r'', name)
        return
    
    def save(self, data):
        if not len(data):
            return
        
        for item in data:
            key = 'others'
            if 'story_link' in item.keys():
                key = re.sub(r'https://www.thepharmaletter.com/article/', r'', item['story_link'])
            elif 'story_term' in item.keys():
                key = item['story_term']
            if item['user_code'] not in self.list.keys():
                self.list[item['user_code']] = {
                    'lc': {},
                    'tb': {}
                }
            self.list[item['user_code']][self.sourceFileName][key] = item

            # filePath = self.documentPath + '/' + listItem['filename']
            # self.file.write(filePath, item)
            
        # filePath = self.listPath + '/' + self.sourceFileName + '.json'
        # self.file.write(filePath, lists)
        return
    
    def saveUsers(self):
        print('-----------------saving ussers')
        if not self.list:
            return
        for user in self.list.keys():
            print(user)
            filePath = self.documentsDirectoryPath + '/' + str(user) + '.json'
            print(filePath)
            self.file.write(filePath, self.list[user])
        return
    
    def __reset(self):
        return
