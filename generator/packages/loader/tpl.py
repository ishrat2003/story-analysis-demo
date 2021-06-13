import json, datetime, re, os
from .core import Core
import urllib.request as urllib
import socket
from bs4 import BeautifulSoup
import dateutil.parser as parser
import sys
from file.json import Json as JsonFile
from file.core import Core as File

class TPL(Core):
    
    def __init__(self, path, format = "json"):
        super().__init__()
        self.html = ''
        self.path = os.path.abspath(path + "/../documents/")
        self.file = JsonFile()
        return
    
    def getDate(self, item):
        if not item or 'pubDate' not in item.keys() or not item['pubDate']:
            return ''
        
        return parser.parse(item['pubDate'])
    
    def getContent(self, item):
        if (not item or ('content' not in item.keys())):
            return '';
        return item['name'] + '. ' + item['content']
    
    def getTitle(self, item):
        return item['name']
    
    def getShortDescription(self, item):
        return item['description']
    
    def fetchPage(self, link, item = None):
        filePath = self.path + '/' + re.sub(r'^.+\/([a-zA-Z0-9\-]+)$', r'\1', link) + '.json'
        
        data = self.file.read(filePath)
        content = data['content_html'] if 'content_html' in data.keys() else data['content']
        soup = BeautifulSoup(content, features="html.parser")
        item = {
            'title': data['name'],
            'description': data['description'],
            'pubDate': data['date'],
            'link': link,
            'content': self.getPageContent(soup),
            'content_html': data['content']
        }
        return item
    
    def getPageContent(self, soup):
        text = ''
        for item in soup.findChildren(recursive=False):
            if not self.shouldIncludeItem(item):
                continue
            text += self.getAndAppendValue(item)
    
        self.html = text    
        text = re.sub('<[^<]+?>', '', text)
        text = re.sub('\s+', ' ', text)
        return text
    
    def shouldIncludeItem(self, item):
        if item.name in ['img', 'iframe']:
            return False
        
        return True
        
    def getDivText(self, divs):
        text = ''
        for div in divs:
            for item in div.findChildren(recursive=False):
                text += self.getAndAppendValue(item)
        return text
    
    def getAndAppendValue(self, item):
        if item.name in ['img', 'iframe']:
            return '';
        value = ''
        if item.name in ['p', 'li']:
            value = self.cleanText(item.text.strip())
        elif item.findChildren():
            for childItem in item.findChildren(recursive=False):
                value += self.getAndAppendValue(childItem)
        else:
            value = self.cleanText(item.text)
            
        if value:
            value = '<' + item.name + '>' + value + ' </' + item.name + '>'
        return value
    
    def cleanText(self, text):
        return text

    
    