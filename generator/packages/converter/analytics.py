import json, datetime, re, os
import sys
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
import numpy as np

class Analytics(Base):
    
    def __init__(self, path):
        super().__init__(path)
        
        self.directoryPath = path
    
        self.file = JsonFile()
        self.sourceFileName = None
        self.data = {}
        self.__reset()
        return
    
    def setSourceFileName(self, name):
        self.sourceFileName = re.sub(r'\..+', r'', name)
        return
    
    def save(self, sourceData):
        if not len(sourceData):
            return
        
        self.data = {}
        for item in sourceData:
            userCode = re.sub(r'Terms Board -- ', r'', item['Event Category'])
            
            if userCode not in self.data.keys():
                self.data[userCode] = {
                    "reading" : {
                        "text": [],
                        "viz": [] 
                    },
                    "mind_map" : {
                        "text": {
                            "nodes": {}
                        },
                        "viz": {
                            "nodes": {}
                        } 
                    }
                }
            taskCondition = re.sub(r" --.+$", r'', item['Event Label'])
            
            if re.match(r"lc-reading --.+", item['Event Action']):
                self.setReadingInfo(item, userCode, taskCondition)
                                
                
        filePath = self.directoryPath + '/analytics.json'
        self.file.remove(filePath)
        self.file.write(filePath, self.data)
        return
    
    def setReadingInfo(self, item, userCode, taskCondition):
        documentKey = re.sub(r"lc-reading -- ", r'', item['Event Action'])
        self.data[userCode]["reading"][taskCondition].append(documentKey)
        parts = item['Event Label'].split('--')
        rootNode = parts[1].strip(' ')
                
        print("------------------------")
        print(item)
        print(userCode)
        print(taskCondition)
        print(rootNode)
        if (rootNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"].keys()):
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode] = {
                "key": rootNode,
                "children": {}
            }
                    
        cardNode = parts[2].strip(' ')
        if (cardNode and cardNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys()):
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode] = {
                "key": cardNode,
                "children": {}
            }
                        
        timeBasedNode = parts[3].strip(' ')
        if (timeBasedNode and timeBasedNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"].keys()):
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode] = {
                "key": timeBasedNode,
                "children": {
            }
        }
                            
        if documentKey:
            print(documentKey)
            if cardNode and timeBasedNode and documentKey not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"][documentKey] = {
                    "key": documentKey,
                    "size": item['Event Value']
                }
            elif documentKey not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][documentKey] = {
                    "key": documentKey,
                    "size": item['Event Value']
                }    
        return
                    
    
    def __reset(self):
        return
