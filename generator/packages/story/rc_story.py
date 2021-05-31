from .scanner import Scanner
from utility.date import Date
import sys

class RCStory:
    
    def __init__(self):
        self.__reset()
        self.minDate = None
        self.maxDate = None
        self.maxWeight = None
        self.minWeight = None
        self.allowedWeight = None
        self.scanner = Scanner()
        self.split = 5
        self.scanRelatedTerms = 3
        return
    
    def addStory(self, data):
        if not data:
            return
        
        self.minDate, self.maxDate = Date.getMinMax(data['pubDate'], self.minDate, self.maxDate)
        
        self.__setWeights(data['concepts']['story_words'])
        
        storyDate = Date.strToDate(data['pubDate'])
        dateKey = str(storyDate.year) + '-' + Date.getFormattedMonthOrDay(storyDate.month) + '-' + Date.getFormattedMonthOrDay(storyDate.day)
        
        urlParts = data['link'].split('/')
        documentKey = urlParts.pop()
        for word in data['concepts']['story_words']:
            self.__appendWord(word, dateKey, data['content'], documentKey)
            self.__appendDocument(data, documentKey)
        return

    def __appendDocument(self, data, documentKey):
        if documentKey in self.documents.keys():
            return
            
        self.documents[documentKey] = {
            'title': data['title'],
            'link': data['link'],
            'description': data['description'],
            'date': dateKey
        }
        return 
    
    def __appendWord(self, word, dateKey, text, documentKey):
        typeKey = self.__getType(word)
        if ((typeKey not in ['positive', 'negative']) and (word['score'] < self.allowedMinWeight)):
            return
        
        wordKey = word['stemmed_word']
        if wordKey not in self.words[typeKey].keys():
            self.words[typeKey][wordKey] = {
                'pure_word': word['pure_word'],
                'stemmed_word': wordKey,
                'category': word['category'],
                'block_count': 0,
                'dated_count': {},
                'tooltip': word['tooltip'],
                'relations': {}
            }
            
        if dateKey not in self.words[typeKey][wordKey]['dated_count'].keys():
            self.words[typeKey][wordKey]['dated_count'][dateKey] = 0
            
        self.words[typeKey][wordKey]['block_count'] += 1
        self.words[typeKey][wordKey]['dated_count'][dateKey] += 1
        
        relations = self.scanner.scan(text, wordKey, self.scanRelatedTerms)
        if relations:
            for relation in relations:
                relationKey = relation['stemmed_word']
                if relationKey not in self.words[typeKey][wordKey]['relations'].keys():
                    self.words[typeKey][wordKey]['relations'][relationKey] = {
                        'display': relation['display'],
                        'block_count': 0,
                        'documents': []
                    }
                self.words[typeKey][wordKey]['relations'][relationKey]['block_count'] += 1
                self.words[typeKey][wordKey]['relations'][relationKey]['documents'].append(documentKey)
        print(self.words[typeKey][wordKey])
        sys.exit()
        return
    
    def __setWeights(self, story):
        self.maxWeight = story[0]['score']
        self.minWeight = story[len(story) - 1]['score']
        self.allowedMinWeight = self.minWeight + ((self.maxWeight - self.minWeight) / self.split) * (self.split - 1)
        return

    def __getType(self, word):
        if word['category'] == 'Verb':
            return 'actions'
        if word['sentiment'] == 'positive':
            return 'positive'
        if word['sentiment'] == 'negative':
            return 'negative'
        return 'topics'
    
    def __reset(self):
        self.words = {
           'topics': {},
           'actions': {},
           'positive': {},
           'negative': {}
        }
        self.documents = {}
        return