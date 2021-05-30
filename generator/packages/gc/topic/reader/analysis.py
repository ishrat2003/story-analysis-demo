import json
from .s3 import S3    

class Analysis(S3):
    
    def getTopics(self):
        return self.getGcFileContent('topics')
    
    def getCountries(self):
        return self.getGcFileContent('country_topics')
    
    def getPeople(self):
        return self.getGcFileContent('person_topics')
    
    def getOrganizations(self):
        return self.getGcFileContent('organization_topics')
    
    def getGcFileContent(self, key):
        content = self.getContent('gc/' + key + '.json')
        if content:
            content = json.load(content['Body'])
            return content
        return None
    
    def getWordFileContent(self, key):
        content = self.getContent('words/' + key + '.json')
        if content:
            content = json.load(content['Body'])
            return content
        return None
        


