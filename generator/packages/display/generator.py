from display.gc import GC as GCDisplay
from story.lc_story import LCStory
from story.rc_story import RCStory
import sys

class Generator:
    
    def __init__(self, params, reader, writer, loader):
        self.params = params
        self.reader = reader
        self.writer = writer
        self.loader = loader
        self.lcStoryProcessor = LCStory()
        self.rcStoryProcessor = RCStory()
        return
    
    def process(self):
        processor = GCDisplay(self.params, self.reader)
        data = processor.get()
        self.writer.save(data, 'gc')
        keys = processor.getUsedKeys()
        
        if not len(keys):
            return
        print('total keys: ', len(keys))
        for key in keys:
            documents = self.reader.getAllDocumentsByWords(key)
            if not len(documents):
                continue
            wordDetails = self.reader.getWordDetails(key)
            rcStoryProcessor = RCStory()

            for document in documents:
                story = self.prcessDocumentDetails(document)
                if (('story_words' not in story['concepts'].keys()) or not len(story['concepts']['story_words_keys'])):
                    continue
                rcStoryProcessor.addStory(story)
            
            rcStoryProcessor.calculateScores()
                
            termsboard = rcStoryProcessor.get([wordDetails])
            
            self.writer.save(termsboard, 'termsboard')
            
            print('---------------- TB stored ---------------')
            
        return data
    
    def prcessDocumentDetails(self, link):
        data = {
            'link': link
        }
        filePath = self.writer.getFilePath(data, 'lc')

        processedData = self.reader.getStoryDetails(filePath)
        if processedData:
            return processedData
        
        details = self.loader.fetchPage(link)
        if not details or not details['content']:
            return

        details['concepts'] = self.lcStoryProcessor.getConcepts(details['content'], details['pubDate'])
        self.writer.save(details, 'lc')
        
        return details
