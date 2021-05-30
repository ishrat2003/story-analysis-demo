import os, datetime
from .topics import Topics
from .base import Base
from reader.analysis import Analysis

class Core(Base):
    
    def __init__(self, params):
        super().__init__(params)
        self.charts = {}
        self.storyAnalysis = Analysis()
        self.data = None
        self.subItemLimit = 20
        self.minimumCount = 3
        return
    
    def load(self):
        self.data = self.storyAnalysis.getTopics()
        self.charts = {}
        self.loadDataDates(self.data)
        self.setStart()
        self.setEnd()
        self.countTopics()
        countries = self.storyAnalysis.getCountries()
        if countries:
            self.charts['countries'] = self.infoPerDateRange(countries, self.dataDates['start'], self.dataDates['end'], 0)
        people = self.storyAnalysis.getPeople()
        if people:
            self.charts['people'] = self.infoPerDateRange(people, self.dataDates['start'], self.dataDates['end'], self.subItemLimit)
            
        organizations = self.storyAnalysis.getOrganizations()
        if people:
            self.charts['organizations'] = self.infoPerDateRange(organizations, self.dataDates['start'], self.dataDates['end'], self.subItemLimit)
        
        self.charts['summary'] = "In the selected time frame (" + self.dataDates['start'] 
        self.charts['summary'] += " to " + self.dataDates['end'] + "), the most highlighted " 
        
        keys = self.charts.keys()
        if 'topics' in keys:
            self.charts['summary'] += self.getHighlighted(self.charts['topics'], 'topics', '')
        if 'organizations' in keys:
            self.charts['summary'] += self.getHighlighted(self.charts['organizations'], 'organization', 'The most stated ')
        if 'individual' in keys:
            self.charts['summary'] += self.getHighlighted(self.charts['people'], 'individual', 'The most discussed ')
        if 'countries' in keys:
            self.charts['summary'] += self.getHighlighted(self.charts['countries'], 'country', 'The most reported ')
        return
    
    def getHighlighted(self, items, key, prefix):
        if not len(items):
            return key.title() + " topics are not found ."
        maxBlockAppearance = items[0]['total_block_count_in_range'];
        allowedRange = maxBlockAppearance / 2;
        
        highlights = []
        for item in items:
            if (maxBlockAppearance - item['total_block_count_in_range'] < allowedRange):
                highlights.append('"' + item['display'] + '"');
        
        if (not len(highlights)):
            return ''
             
        if (len(highlights) == 1):
            return prefix + key + ' is ' + highlights[0] + '. '
        
        if (key == 'topic'): key = 'topics';
        if (key == 'organization'): key = 'organizations';
        if (key == 'individual'): key = 'individuals';
        if (key == 'country'): key = 'countries';
        
        if (len(highlights) == 2):
            return prefix + key + ' are ' + highlights[0] + ' and ' + highlights[1] + '. '
        
        return prefix + key + ' are ' + ', '.join(highlights[0:-1]) + ' and ' + highlights[-1] + '. '
    
    def get(self):
        self.charts['dates'] = self.dataDates
        return self.charts
    
    def countTopics(self):
        topicsProcessor = Topics()
        self.charts['topics'] = topicsProcessor.count(self.dataDates['start'], self.dataDates['end'], self.data)
        return
    
    def infoPerDateRange(self, items, start, end, limit):
        if not items.keys():
            return []
        
        start = self.unformattedStrToDate(start)
        end = self.unformattedStrToDate(end)
        
        itemsInRange = {}
        
        for key in items.keys():
            keyCount = 0
            allCountPerDay = items[key]['count_per_day']
            items[key]['count_per_day'] = {}
            if len(allCountPerDay):
                for dateKey in allCountPerDay.keys():
                    itemDate = self.unformattedStrToDate(dateKey)
                    if (itemDate >= start) and (itemDate <= end):
                        keyCount += allCountPerDay[dateKey]
                        items[key]['count_per_day'][dateKey] =  allCountPerDay[dateKey]
                    
            if keyCount:
                itemsInRange[key] = items[key]
                itemsInRange[key]['total_block_count_in_range'] = keyCount
                
        if not itemsInRange.keys():
            return []
        
        sortedItems = self.sort(itemsInRange, 'total_block_count_in_range', True, self.minimumCount)
        totalItems = len(sortedItems)
        if limit and totalItems > limit:
            processedItems = sortedItems[0: limit]
            otherItems = sortedItems[limit:]
            totalOthers = 0
            
            for item in otherItems:
                totalOthers += item['total_block_count_in_range']
                
            processedItems.append({
                'display': 'Others',
                'count_per_day': {},
                'total_block_count_in_range': totalOthers
            });
            return processedItems
        
        return sortedItems
    
    