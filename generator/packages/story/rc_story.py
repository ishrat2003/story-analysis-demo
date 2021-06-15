import os, operator
from .scanner import Scanner
from utility.date import Date
from file.json import Json as JsonFile
from file.core import Core as File

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
        self.totalDaysBetweenMaxMin = 0
        self.total = 0
        self.usedTerms = []
        self.topicNames = []
        self.__loadSamples()
        return
    
    def getDocuments(self):
        sorted =  self.__sort(self.documents, 'date', True) 
        return sorted
    
    def get(self, topicWords):
        self.topicNames = []
        for word in topicWords:
            self.topicNames.append(word['pure_word'])
        data = {}
        data['main_topic'] = topicWords[0]
        data['documents'] = self.getDocuments()
        data['date_range'] = {
            'min': Date.dateToStr(self.minDate),
            'max': Date.dateToStr(self.maxDate)
        }
        data['total'] = self.total
        data['description'] = self.__getBoardDescription()
        
        wordKey = topicWords[0]['stemmed_word']
        typeKey = 'what'
        if wordKey in self.words['who'].keys():
            typeKey = 'who'
        elif wordKey in self.words['where'].keys():
            typeKey = 'where'
        if wordKey in self.words[typeKey].keys():
            data['when'] = self.__getBarChart(self.words[typeKey][wordKey]['dated_count'])
        else:
            data['when'] = []
        data['board'] = self.__getBoard()
        return data
            
    def calculateScores(self):
        self.totalDaysBetweenMaxMin = Date.daysBetween(self.maxDate, self.minDate)
        typeKeys = self.words.keys()
        for typeKey in typeKeys:
            self.__scoreType(typeKey)
        return
    
    def addStory(self, data):
        if not data:
            return
        
        self.minDate, self.maxDate = Date.getMinMax(Date.strToDate(data['pubDate']), self.minDate, self.maxDate)
        
        self.__setWeights(data['concepts']['story_words'])
        
        storyDate = Date.strToDate(data['pubDate'])
        dateKey = str(storyDate.year) + '-' + Date.getFormattedMonthOrDay(storyDate.month) + '-' + Date.getFormattedMonthOrDay(storyDate.day)
        
        urlParts = data['link'].split('/')
        documentKey = urlParts.pop()
        self.__appendDocument(data, dateKey, documentKey)
        
        for word in data['concepts']['story_words']:
            self.__appendWord(word, dateKey, data['content'], documentKey)
            
        return

    def __scoreType(self, typeKey):
        if not len(self.words[typeKey]):
            return
        for wordKey in self.words[typeKey].keys():
            self.words[typeKey][wordKey]['old_to_new'] = self.__getOldToNewScore(self.words[typeKey][wordKey]['dated_count'])
            self.words[typeKey][wordKey]['new_to_old'] = self.__getNewToOldScore(self.words[typeKey][wordKey]['dated_count'])
            self.words[typeKey][wordKey]['consistent'] = (self.words[typeKey][wordKey]['old_to_new'] + self.words[typeKey][wordKey]['new_to_old']) / 2
            
        return
    
    def __appendDocument(self, data, dateKey, documentKey):
        if documentKey in self.documents.keys():
            return
            
        self.documents[documentKey] = {
            'title': data['title'],
            'link': data['link'],
            'description': data['description'],
            'date': dateKey
        }
        
        self.total += 1
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
        return
    
    def __setWeights(self, story):
        self.maxWeight = story[0]['score']
        self.minWeight = story[len(story) - 1]['score']
        self.allowedMinWeight = self.minWeight + ((self.maxWeight - self.minWeight) / self.split) * (self.split - 1)
        return

    def __getType(self, word):
        if word['category'] == 'Verb':
            return 'action'
        if (word['category'] in ['Person', 'Organization']) or (word['pure_word'] in self.whoSamples):
            return 'who'
        if (word['category'] in ['Location']) or (word['pure_word'] in self.whereSamples):
            return 'where'
        if word['sentiment'] == 'positive':
            return 'positive'
        if word['sentiment'] == 'negative':
            return 'negative'
        if word['pure_word'] in self.whoSamples:
            return 
        return 'what'
    
    def __reset(self):
        self.words = {
           'who': {},
           'where': {},
           'what': {},
           'action': {},
           'positive': {},
           'negative': {}
        }
        self.documents = {}
        return
    
    def __loadSamples(self):
        file = JsonFile()
        path = File.join(os.path.abspath(__file__ + "/../../../resources/"), "samples/Where.json")
        self.whereSamples = file.read(path)
        path = File.join(os.path.abspath(__file__ + "/../../../resources/"), "samples/Who.json")
        self.whoSamples = file.read(path)
        return
    
    def __getOldToNewScore(self, dates):
        score = 0
        for date in dates.keys():
            score += (self.totalDaysBetweenMaxMin - Date.daysBetween(Date.strToDate(date), self.minDate)) * dates[date]
        return score
    
    def __getNewToOldScore(self, dates):
        score = 0
        for date in dates.keys():
            score += (self.totalDaysBetweenMaxMin - Date.daysBetween(self.maxDate, Date.strToDate(date))) * dates[date]
        return score
    
    def __sort(self, items, attribute='block_count', reverse=True):
        if not len(items.keys()):
            return []

        sortedTopics = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=reverse):
            sortedTopics.append(value)

        return sortedTopics
    
    def __getRelations(self, relations, source, excludedTargets):
        processedRelations = []
        if not relations:
            return
        
        filteredRelation = {} if len(excludedTargets) else relations
        
        if excludedTargets:
            # Blocking infinite relation 
            for relationKey in relations:
                if relationKey not in excludedTargets:
                    filteredRelation[relationKey] = relations[relationKey]
        
        sortedRelations = self.__sort(filteredRelation, 'block_count', True) 
        sortedRelations = sortedRelations[0:self.scanRelatedTerms]
        
        for relation in sortedRelations:
            documents = []
            for documentKey in relation['documents']:
                documents.append(self.documents[documentKey])
                
            processedRelations.append({
                'source': source,
                'target': relation['display'],
                'size': relation['block_count'],
                'documents': documents
            })
        return processedRelations
    
    def __getBarChart(self, datedCounts):
        bars = {}
        for date in datedCounts.keys():
            bars[date] = {
            'date': date,
            'value': datedCounts[date]
            }
            
        sortedBars = self.__sort(bars, 'date', False) 
        return sortedBars

    def __getBoard(self):
        data = {
        'who': self.__getCard('who'),
        'where': self.__getCard('where'),
        'what_topic': self.__getCard('what'),
        'what_action': self.__getCard('action'),
        'why_positive': self.__getCard('positive'),
        'why_negative': self.__getCard('negative')
        }
        return data
    
    def __getCard(self, typeKey, limit = 3):
        return {
            'consistent': self.__getWordsByScoreType(typeKey, 'consistent', limit),
            'old_to_new': self.__getWordsByScoreType(typeKey, 'old_to_new', limit),
            'new_to_old': self.__getWordsByScoreType(typeKey, 'new_to_old', limit)
        }
        
    def __getWordsByScoreType(self, type, scoreType, limit = 3):
        sorted =  self.__sort(self.words[type], scoreType, True) 
        items = []
        targets = []
        for word in sorted:
            if word['stemmed_word'] in self.usedTerms:
                continue
            name = word['pure_word'][0].upper() + word['pure_word'][1:]
            items.append({
                'name': name,
                'key': word['stemmed_word'],
                'size': word['block_count'],
                'old_to_new': word['old_to_new'],
                'new_to_old': word['new_to_old'],
                'consistent': word['consistent'],
                'tooltip': word['tooltip'],
                'relations': word['relations'],
                'dated_bars': self.__getBarChart(word['dated_count']) 
            })
            targets.append(word['stemmed_word']);
            self.usedTerms.append(word['stemmed_word'])
            if len(items) == limit:
                break
        if len(items):
            index = 0
            for item in items:
                items[index]['relations'] = self.__getRelations(item['relations'], item['name'], targets)
                index += 1
                
            
        return items
    
    def __getBoardDescription(self):
        text = 'Displaying ' + str(self.total) + ' news from ' + Date.dateToStr(self.minDate) + ' to ' + Date.dateToStr(self.maxDate) + ' about '
        totalNames = len(self.topicNames)
        processed = 0
        divider = ''
        for name in self.topicNames:
            if processed <= totalNames - 1:
                text += divider + '"' + name + '"'
                processed += 1
            divider = ' and ' if processed == totalNames - 1 else ', '
            
        return text
    
    