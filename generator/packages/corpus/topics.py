from .base import Base
import operator

class Topics(Base):
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.filteredTopics = {}
        return
    
    def get(self, raw = False, top = 0, includeOthers = False):
        if not len(self.filteredTopics.keys()):
            return {}
        
        if raw:
            return self.filteredTopics
        
        sortedTopics = self.sort()
        if not top or not sortedTopics or (len(sortedTopics) <= top):
            return sortedTopics
        
        topTopics = sortedTopics[0: top]
        if not includeOthers:
            return topTopics
        
        otherTopics = topTopics[top:]
        totalOthers = 0
        for item in otherTopics:
            totalOthers += item['total_block_count']
                
        topTopics.append({
            'display': 'Others',
            'count_per_day': {},
            'total_block_count': totalOthers
        });
        
        return topTopics
    
    def append(self, topics, addAll = False):
        if not topics or not topics.keys():
            return []
        
        startYear, startMonth, startDay = [int(x) for x in self.start.split("-")]
        endYear, endMonth, endDay = [int(x) for x in self.end.split("-")]
        
        for topic in topics.keys():
            if (not addAll and (('category' not in topics[topic].keys()) or (topics[topic]['category'] == 'Verb'))):
                continue
            count = 0
            linegraph = []
            for date in topics[topic]["count_per_day"].keys():
                if self.shouldValidDate(date, self.start, self.end):
                    count += topics[topic]["count_per_day"][date]
                    linegraph.append({
                        'date': date,
                        'value': topics[topic]["count_per_day"][date]
                    })
            if count or addAll:
                if topic not in self.filteredTopics.keys():
                    self.filteredTopics[topic] = topics[topic]
                    self.filteredTopics[topic]['total_block_count'] = 0
                    self.filteredTopics[topic]['linegraph'] = []
                    del self.filteredTopics[topic]["count_per_day"]
                if count:
                    self.filteredTopics[topic]['total_block_count'] += count
                    self.filteredTopics[topic]['linegraph'] = linegraph
        return
    
    def sort(self, attribute='total_block_count', reverse=True, minValue = 0):
        if not len(self.filteredTopics.keys()):
            return []

        sortedTopics = []
        contributors = self.filteredTopics.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=reverse):
            if not isinstance(value[attribute], int) or (value[attribute] > minValue):
                sortedTopics.append(value)

        return sortedTopics