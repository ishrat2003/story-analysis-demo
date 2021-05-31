import datetime
from story.lc_story import LCStory
from .base import Base

class Context(Base):
    
    def __init__(self, loader, writer, totalItems = 0):
        self.loader = loader
        self.writer = writer
        self.totalItems = int(totalItems)
        self.totalProcessed = 0
        self.lcStoryProcessor = LCStory()
        self.topicsPerDocument = 10
        return
    
    def process(self, fileContent):
        if self.totalItems and self.totalProcessed and (self.totalProcessed == self.totalItems):
            return False
        
        data = self.loader.load(fileContent)
        
        if not data:
            return False
        
        for item in data:
            self.appendToCorpus(item);
            self.totalProcessed += 1
            if self.totalItems and (self.totalProcessed == self.totalItems):
                return True

        return True
    
    def appendToCorpus(self, item):
        date = datetime.datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S GMT")
        if not self.writer.isNewDocument(item['link'], str(date.year), self._getFormattedMonthOrDay(date.month)):
            print('Already processed')
            return

        details = self.loader.getDetails(item)
        if not details or not details['content']:
            return

        self.writer.setItemDetails(item['link'], details['pubDate'])

        topics = self.__getTopTopics(details)
        if not len(topics):
            return

        self.writer.save(topics)
        return
    
    
    def __getTopTopics(self, item):
        concepts = self.lcStoryProcessor.getConcepts(item['content'], item['pubDate'])
        if not concepts['story_words']:
            return []
        return concepts['story_words'][0:self.topicsPerDocument]