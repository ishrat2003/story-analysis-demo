import json, datetime, re, os
import sys
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
import numpy as np
from file.csv import Csv

class Analytics(Base):
    
    def __init__(self, path):
        super().__init__(path)
        
        self.directoryPath = path
    
        self.file = JsonFile()
        self.sourceFileName = None
        self.data = {}
        self.sizeUnit = 2
        self.maxSize = 30
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
                                
            if re.match(r"termsboard-modal-open --.+", item['Event Action']):
                self.setModalInfo(item, userCode, taskCondition)
                
            if re.match(r"termsboard-tems-display --.+", item['Event Action']):
                self.setModalInfo(item, userCode, taskCondition)
            
            if re.match(r"termsboard-related-document-display --.+", item['Event Action']):
                self.setModalInfo(item, userCode, taskCondition)
                 
            
        filePath = self.directoryPath + '/analytics.json'
        self.file.remove(filePath)
        self.file.write(filePath, self.data)
        
        countFilePath = self.directoryPath + '/tb_doc_count.csv'
        countWriter = Csv()
        countWriter.remove(countFilePath)
        allWriteHeader = True
        graph = {}
        
        for userCode in self.data.keys():
            print(userCode)
            textNodeKeys = list(self.data[userCode]["mind_map"]["text"]["nodes"].keys())
            vizNodeKeys = list(self.data[userCode]["mind_map"]["viz"]["nodes"].keys())
            graph[userCode] = {
                "text": self.getGraph(self.data[userCode]["mind_map"]["text"]["nodes"][textNodeKeys[0]], [], []) if textNodeKeys else {},
                "viz": self.getGraph(self.data[userCode]["mind_map"]["viz"]["nodes"][vizNodeKeys[0]], [], []) if vizNodeKeys else {}
            }      
            row = {
                "userCode": userCode,
                "viz": len(self.data[userCode]["reading"]["viz"]),
                "text": len(self.data[userCode]["reading"]["text"])
            }
            print(row)
            countWriter.append(countFilePath, row, allWriteHeader)
            allWriteHeader = False
            
        filePath = self.directoryPath + '/analytics_graph.json'
        self.file.remove(filePath)
        self.file.write(filePath, graph)
        
        return
    
    def getGraph(self, tree, nodes, links):
        if not tree:
            return {}
        
        print('-----------------------')
        print(tree)
        nodes.append({
            "id": tree["key"], 
            "group": self.getGroupName(tree["key"]), 
            "size": tree["size"]
        })
        if "children" in tree.keys():
            for childKey in tree["children"].keys():
                links.append({
                    "source": tree["key"], 
                    "target": childKey, 
                    "value": 1
                })
                    
                result = self.getGraph(tree["children"][childKey], nodes, links)
                if result['nodes']:
                    nodes = result['nodes']
                    
                if result['links']:
                    links = result['links']
                
        return {
            "nodes": nodes,
            "links": links
        }
    
    
    def getGroupName(self, key):
        if key in ['pfizer', 'astrazeneca']:
            return 'task'
        
        if re.search("^.+Box$", key):
            return 'card'
        
        if key in ['consistent', 'new_to_old', 'old_to_new']:
            return 'timeline'
        
        return 'document'
    
    def setModalInfo(self, item, userCode, taskCondition):
        parts = item['Event Label'].split('--')
        rootNode = parts[1].strip(' ')
        
        actionParts = item['Event Action'].split('--')
        
        # print("------------------------")
        # print(item)
        # print(userCode)
        # print(taskCondition)
        # print(rootNode)
        # print(actionParts)
        cardNode = actionParts[1].strip(' ')
        timeBasedNode = actionParts[2].strip(' ')
        
        if (rootNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"].keys()):
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode] = {
                "key": rootNode,
                "children": {},
                "size": self.sizeUnit
            }
        else:
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["size"] += self.sizeUnit
                     
        if cardNode:
            if cardNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode] = {
                    "key": cardNode,
                    "children": {},
                    "size": self.sizeUnit
                }
            else:
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["size"] += self.sizeUnit
                        
        if timeBasedNode:
            if timeBasedNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode] = {
                    "key": timeBasedNode,
                    "children": {},
                    "size": item['Total Events'] if item['Total Events'] < self.maxSize else self.maxSize
                }
            else:
                newSize = self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["size"] + item['Total Events']
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["size"] = newSize if newSize < self.maxSize else self.maxSize
            
        return
    
    def setReadingInfo(self, item, userCode, taskCondition):
        documentKey = re.sub(r"lc-reading -- ", r'', item['Event Action'])
        self.data[userCode]["reading"][taskCondition].append(documentKey)
        parts = item['Event Label'].split('--')
        rootNode = parts[1].strip(' ')
                
        if (rootNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"].keys()):
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode] = {
                "key": rootNode,
                "children": {},
                "size": self.sizeUnit
            }
        else:
            self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["size"] += self.sizeUnit
                    
        cardNode = parts[2].strip(' ')
        if cardNode:
            if cardNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode] = {
                    "key": cardNode,
                    "children": {},
                    "size": self.sizeUnit
                }
            else:
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["size"] += self.sizeUnit
                                        
        timeBasedNode = parts[3].strip(' ')
        if timeBasedNode:
            if timeBasedNode not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode] = {
                    "key": timeBasedNode,
                    "children": {},
                    "size": self.sizeUnit
                }
            else:
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["size"] += self.sizeUnit
                            
        if documentKey:
            if cardNode and timeBasedNode and documentKey not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"][documentKey] = {
                    "key": documentKey,
                    "size": item['Event Value'] if item['Total Events'] < self.maxSize else self.maxSize
                }
            elif documentKey not in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][documentKey] = {
                    "key": documentKey,
                    "size": item['Total Events'] if item['Total Events'] < self.maxSize else self.maxSize
                }
            elif cardNode and timeBasedNode and documentKey in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][cardNode]["children"][timeBasedNode]["children"][documentKey]["size"] += item['Event Value']
            elif documentKey in self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"].keys():
                self.data[userCode]["mind_map"][taskCondition]["nodes"][rootNode]["children"][documentKey]["size"] += item['Total Events']
            
        return
                    
    
    def __reset(self):
        return
