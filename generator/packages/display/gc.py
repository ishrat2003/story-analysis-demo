class GC:
    
    def __init__(self, params, reader):
        self.params = params
        self.reader = reader
        self.start = params.start
        self.end = params.end
        self.keys = []
        return
    
    def getUsedKeys(self):
        return self.keys
    
    def get(self):
        self.keys = []
        data = {
            'dates': {
                'start': self.start,
                'end': self.end
            }
        }
        
        rc = self.reader.getGcContentByDate('topics', self.start, self.end)
        data['topics'] = rc.get(False, 25, False)
        self._appendKeys(data['topics'])
        
        rc = self.reader.getGcContentByDate('person_topics', self.start, self.end)
        data['people'] = rc.get(False, 10, True)
        self._appendKeys(data['people'])
        
        rc = self.reader.getGcContentByDate('organization_topics', self.start, self.end)
        data['organizations'] = rc.get(False, 10, True)
        self._appendKeys(data['organizations'])
        
        rc = self.reader.getGcContentByDate('country_topics', self.start, self.end)
        data['countries'] = rc.get(True, 0, False)
        
        data['sorted_countries'] = rc.get(False, 0, False)
        self._appendKeys(data['sorted_countries'])
        data['summary'] = self.getSummary(data)
        return data
    
    def getSummary(self, data):
        summary = "In the selected time frame (" + self.start
        summary += " to " + self.end + "), the most highlighted " 
        
        keys = data.keys()
        if 'topics' in keys:
            summary += self.getHighlighted(data['topics'], 'topics', '')
        if 'organizations' in keys:
            summary += self.getHighlighted(data['organizations'], 'organization', 'The most stated ')
        if 'people' in keys:
            summary += self.getHighlighted(data['people'], 'individual', 'The most discussed ')
        if 'sorted_countries' in keys:
            summary += self.getHighlighted(data['sorted_countries'], 'country', 'The most reported ')
        
        return summary

    def getHighlighted(self, items, key, prefix):
        if not len(items):
            return key.title() + " topics are not found ."

        maxBlockAppearance = items[0]['total_block_count'];
        allowedRange = maxBlockAppearance / 2;
        
        highlights = []
        for item in items:
            if (maxBlockAppearance - item['total_block_count'] < allowedRange):
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
    
    def _appendKeys(self, items):
        if not len(items):
            return
        
        for item in items:
            if (('key' not in item.keys()) or (item['key'] in self.keys)):
                continue
            self.keys.append(item['key'])
        return
