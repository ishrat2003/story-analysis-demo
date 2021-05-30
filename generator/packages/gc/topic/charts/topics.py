import operator
from .base import Base

class Topics(Base):
    
    def __init__(self):
        self.limit = 50
        self.subItemLimit = 5
        self.topics = {}
        return
    
    def getPeople(self):
        return self.getCategoryTopics('People')
    
    def getOrganizations(self):
        return self.getCategoryTopics('Organization')
    
    def getCategoryTopics(self, category):
        if not len(self.topics.keys()):
            return []
        items = {}
        for topic in self.topics.keys():
            if self.topics[topic]['category'] == category:
                items[topic] = self.topics[topic]
                
        if not len(items.keys()):
            return []
        sortedItems = self.sort(items)
        return sortedItems[0: self.subItemLimit]
    
    def count(self, start, end, data):
        startYear, _, _ = self.getSplited(start)
        endYear, _, _ = self.getSplited(end)
        self.topics = {}
        
        for year in self.getRangeToList(startYear, endYear):
            months = self.getMonthsForYear(year, start, end)
            print('year: ', year)
            print('months: ', months)
            if len(months):
                for month in months:
                    days = self.getDayOfMonthForYear(year, month, start, end)
                    print('days: ', days)
                    if len(days):
                        for day in days:
                            self.processDay(data, year, month, day)
                            
        sortedTopics = self.sort(self.topics)
        return sortedTopics[0: self.limit]
    
    def processDay(self, data, year, month, day):
        year = str(year)
        month = str(month)
        day = str(day)
        fullDateKey = year + '-' + month + '-' + day
        
        if year not in data.keys():
            return
        
        if month not in data[year].keys():
            return
        
        if day not in data[year][month].keys():
            return
        
        if not len(data[year][month][day].keys()):
            return
        
        # print('-----------------')
        # print(fullDateKey)
        # print('-----------------')
        for topic in data[year][month][day].keys():
            if topic not in self.topics.keys():
                self.topics[topic] =  data[year][month][day][topic]
                self.topics[topic]['key'] = topic
                self.topics[topic]['total_block_count_in_range'] = 0
                self.topics[topic]['linegraph'] = []
            self.topics[topic]['total_block_count_in_range'] += data[year][month][day][topic]['block_count']
            
            # print(topic , '-' ,data[year][month][day][topic]['block_count'], '=',  self.topics[topic]['total_block_count_in_range'])
            self.topics[topic]['linegraph'].append({
                'date': fullDateKey,
                'block_count': data[year][month][day][topic]['block_count']
            })
        return
    
    def getDayOfMonthForYear(self, year, month, start, end):
        days = [31, 29, 31, 30, 31,30, 31, 31, 30, 31, 30, 31]
        startYear, startMonth, startDay = self.getSplited(start)
        endYear, endMonth, endDay = self.getSplited(end)
        
        if month != startMonth and month != endMonth:
            return self.getRangeToList(1, days[month - 1])
        
        if month == startMonth and month == endMonth:
            return self.getRangeToList(startDay, endDay)
        
        if month == startMonth and month != endMonth:
            return self.getRangeToList(startDay, days[month - 1])
                         
        if month != startMonth and month == endMonth:
            return self.getRangeToList(1, endDay)
        
        return []
    
    def getMonthsForYear(self, year, start, end):
        startYear, startMonth, _ = self.getSplited(start)
        endYear, endMonth, _ = self.getSplited(end)
        
        if year < startYear or year > endYear:
            return []
        
        if year > startYear and year < endYear:
            return self.getRangeToList(1, 12)
        
        if year == startYear and year == endYear:
            return self.getRangeToList(startMonth, endMonth)
        
        if year == startYear and year < endYear:
            return self.getRangeToList(startMonth, 12)
        
        if year > startYear and year == endYear:
            return self.getRangeToList(1, endMonth)
        
        return []
        
    def getRangeToList(self, start, end):
        return[ x for x in range(int(start), int(end) + 1)]

