import operator, math, datetime
import os, sys
from .base import Base
from reader.analysis import Analysis

class RC(Base):
    
    def __init__(self, params):
        super().__init__(params)
        self.storyAnalysis = Analysis()
        self.start = self.strToDate(self.params['start']) if self.params['start'] else None
        self.end = self.strToDate(self.params['end']) if self.params['end'] else None
        self.subTopics = {}
        self.documents = []
        self.pureWords = {}
        self.blockCounts = {}
        self.wordDocuments = {}
        self.filteredWords = {}
        self.linegraph = {}
        self.totalInRange = 0
        self.grandTotal = 0;
        self.allowedMinimum = 2
        self.subTopicLimit = 30
        return
    
    def getSubTopics(self):
        if (not self.params or ('main_topic' not in self.params.keys())):
            return self.subTopics
        
        print('sub topics ----', self.subTopics)
        print('main topic: ', self.params['main_topic']);
        data = self.storyAnalysis.getWordFileContent(self.params['main_topic'])

        if (not data or ('documents' not in data.keys())):
            return self.subTopics
        print(data.keys())
        self.loadDataDates(data['documents'])
        self.setStart()
        self.setEnd()
        
        self.loadDocuments(data['documents'])
        self.loadFilteredWords()

        rows = {}
        if len(self.linegraph.keys()):
            for date in self.linegraph.keys():
                rows[date] = {
                    'date': date,
                    'value': self.linegraph[date]
                }   
            rows = self.sort(rows, 'date', False)
            
        return {
            'main_topic': data['pure_word'],
            'dates': self.dataDates,
            'grand_total': self.grandTotal,
            'total_in_range': self.totalInRange,
            'linegraph': rows,
            'sub_topics': self.filteredWords[0:self.subTopicLimit]
        }
    
    def loadFilteredWords(self):
        if not self.totalInRange:
            return
        
        words = self.blockCounts.keys()
        for word in words:
            if self.blockCounts[word] >= self.allowedMinimum :
                self.filteredWords[word] = {
                    'display': self.getDisplayName(word),
                    'size': self.blockCounts[word],
                    'key': word
                }
                
        if len(self.filteredWords.keys()):
            self.filteredWords = self.sort(self.filteredWords, 'size')
        return
    
    def getDisplayName(self, word):
        if word in self.pureWords.keys():
            return self.pureWords[word][0].upper() + self.pureWords[word][1:]
        return word
    
    def loadDocuments(self, documents):
        for year in documents.keys():
            for month in documents[year].keys():
                for day in documents[year][month].keys():
                    for link in documents[year][month][day].keys():
                        fullDate = str(year) + '-' + self.getFormattedMonthOrDay(int(month)) + '-' + self.getFormattedMonthOrDay(int(day))
                        
                        if self.isTotalInRange(self.strToDate(fullDate)):
                            if fullDate not in self.linegraph.keys():
                                self.linegraph[fullDate] = 0
                            self.linegraph[fullDate] += 1
                            self.addDocument(documents[year][month][day][link])
                            
                        self.grandTotal += 1
                        
        return
                 
    def isTotalInRange(self, fullDate):
        if not self.start and not self.end:
            self.totalInRange += 1
            return True
        if (fullDate >=  self.start) and (not self.end or (fullDate <= self.end)):
            self.totalInRange += 1
            return True
        return False
                   
    def addDocument(self, document):
        if 'topics' not in document.keys():
            return
        wordKeys = []
        for word in document['topics']:
            wordKeys.append(word)
            if word not in self.pureWords.keys():
                self.pureWords[word] = document['topics'][word]['pure_word']
                self.blockCounts[word] = 0
                self.wordDocuments[word] = []
            self.blockCounts[word] += 1
            self.wordDocuments[word].append(document['url'])
        
        if len(wordKeys):
            self.documents.append(wordKeys)
        return 
