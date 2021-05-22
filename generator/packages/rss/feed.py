
import traceback, json
import urllib3,  urllib
import xmltodict
from collections import OrderedDict
import sys, re
import os.path
from bs4 import BeautifulSoup
from datetime import date
from file.json import Json as JsonFile

class Feed:
    def __init__(self, feedPath, destinationPath):
        file = JsonFile()
        self.urls = file.read(feedPath)
        self.destinationPath = destinationPath
        self.today = date.today();
        return
    
    def process(self):
        if not self.urls:
            return
        
        for url in self.urls:
            print('Processing ' + url)
            self.__saveXmlToJson(url)
        return
    
    def __saveXmlToJson(self, url):
        response = self.__getResponse(url)
        try:
            data = xmltodict.parse(response.data)
            filePath = os.path.join(self.destinationPath, self.__getFeedName(url)) 
            self.__saveJsonFile(data['rss']['channel']['item'], filePath)
        except:
            print("Failed to parse xml from response (%s)" % traceback.format_exc())
        
        return
    
    def __getFeedName(self, url):
        name = url.replace('http://', '')
        name = name.replace('https://', '')
        name = re.sub(r'[^a-zA-Z0-9]+', '', name)
        name = self.today.strftime("%Y%m%d-") + name + '.json'
        return name
    
    def __saveJsonFile(self, content, filePath):
        with open(filePath, 'w') as f:
            json.dump(content, f)
        return
    
    def __getResponse(self, url):
        http = urllib3.PoolManager()
        return http.request('GET', url)


