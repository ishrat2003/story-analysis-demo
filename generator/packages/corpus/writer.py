import os, datetime
from writer.base import Base
from filesystem.directory import Directory
from file.json import Json as JsonFile
from file.core import Core as File
from nltk.stem.porter import PorterStemmer

class Writer(Base):
    
    def __init__(self, path):
        super().__init__(path)
        self.stemmer = PorterStemmer()
        
        resourcePath = os.path.abspath(__file__ + "/../../../resources/")
        self.gcPath = os.path.join(path, 'gc')
        self.wordsPath = os.path.join(path, 'words')
        self.mapsDirectoryPath = File.join(resourcePath, "maps")
        self.categoryDirectoryPath = File.join(resourcePath, 'categories')
        self.file = JsonFile()
        self.__reset()
        return
    
    def setItemDetails(self, link, date):
        print(link)
        self.link = link
        self.year = date[0:4]
        self.month = date[5:7]
        self.day = date[8:10]
        self.date = date[0:10]
        self.storyWords = {}
        self.isNew = False
        self.__setGCFilePaths()
        self.__loadTopics()
        self.__loadCountries()
        self.__loadPerson()
        self.__loadOrganization()
        return
    
    def save(self, topics):
        if not self.isNew:
            return

        for topic in topics:
            if self.__saveWordDetails(topic):
                self.__updateGCDetails(topic)
                self.__updateCommon()
        return
    
    def isNewDocument(self, link):
        filePath = self.gcPath + '/documents/' + self.year + '_' + self.month + '.json'
        documents = self.file.read(filePath)
        if not documents:
            documents = []
        if link not in documents:
            documents.append(link)
            self.isNew = True
            self.file.write(filePath, documents)
        return self.isNew
    
    def __updateGCDetails(self, topic):
        self.__addToCorpus(topic)
        self.file.write(self.topicsFilePath, self.topics)
        self.file.write(self.countryFilePath, self.countries)
        self.file.write(self.personFilePath, self.person)
        self.file.write(self.organizationFilePath, self.organization)
        self.file.write(self.commonDataFilePath, self.common)
        return
    
    def __saveWordDetails(self, word):
        wordDirectoryPath = self.__getWordDirectory(word['stemmed_word'])
        
        # Save word-document association
        monthPath = os.path.join(wordDirectoryPath, self.year, self.month + '.json')
        monthDetails = self.file.read(monthPath)
        if not monthDetails:
            monthDetails = {}
            
        key = self.year + '-' + self.month + '-' + self.day
        if key not in monthDetails.keys():
            monthDetails[key] = []
            
        if self.link in monthDetails[key]:
            return False
        
        monthDetails[key].append(self.link)
        self.file.write(monthPath, monthDetails)
        
        # Save word details
        detailsPath = os.path.join(wordDirectoryPath, 'details.json')
        currentDetails = self.file.read(detailsPath)
        
        if not currentDetails:
          currentDetails = {
            'type': word['type'], 
            'pure_word': word['pure_word'], 
            'stemmed_word': word['stemmed_word'], 
            'category': word['category'], 
            'sentiment': word['sentiment'],
            'count': 0, 
            'tooltip': word['tooltip'], 
            'color_group': word['color_group']
        }
          
        currentDetails['count'] += 1
        self.file.write(detailsPath, currentDetails)
        return True
    
    def __addToCorpus(self, word):
        self.__saveCategories(word['category'],  word['pure_word'])
        
        wordKey = word['pure_word'].lower().strip().replace(' ', '_')
        if word['type'] in ['NNP', 'NNPS']:
            countryName = self.__getCountyName(word['pure_word'])
            if countryName:
                wordKey = countryName.lower()
                self.countries[wordKey] =  self.__getTopicEntry(word, self.countries, wordKey)
            elif (word['category'] == 'Person'):
                self.person[wordKey] =  self.__getTopicEntry(word, self.person, wordKey)
            elif (word['category'] == 'Organization'):
                self.organization[wordKey] =  self.__getTopicEntry(word, self.organization, wordKey)    
            
        self.topics[wordKey] =  self.__getTopicEntry(word, self.topics, wordKey)
        return
    
    def __getTopicEntry(self, word, items, wordKey):
        wordKey = wordKey.lower().strip()
        processedWord = None
        if wordKey not in items.keys():
            processedWord = {
                'display': word['pure_word'],
                'total_block_count': 0,
                'count_per_day': {},
                'key': word['stemmed_word'],
                'category': word['category'], 
                'tooltip': word['tooltip'],
                'sentiment': word['sentiment']
            }
        else:
            processedWord = items[wordKey]
            
        fullDateKey = self.year + '-' + self.__getFormattedMonthOrDay(self.month) + '-' + self.__getFormattedMonthOrDay(self.day)
        if fullDateKey not in processedWord['count_per_day'].keys():
            processedWord['count_per_day'][fullDateKey] = 0

        processedWord['count_per_day'][fullDateKey] += 1 
        processedWord['total_block_count'] += 1
        return processedWord

    def __saveCategories(self, category, pureWord):
        specificCategoryDirectoryPath = File.join(self.categoryDirectoryPath, 'category' + '.json')
        
        items = self.file.read(specificCategoryDirectoryPath)
        if not items:
            items = [] 
        if pureWord not in items:
            items.append(pureWord)

        self.file.write(specificCategoryDirectoryPath, items)
        return
    
    def __setGCFilePaths(self):
        documentsDirectoryPath = os.path.join(self.gcPath, 'documents')
        documentsDirectoryPath = Directory(documentsDirectoryPath)
        documentsDirectoryPath.create()
        
        yearDirectoryPath = os.path.join(self.gcPath, self.year)
        yearDirectory = Directory(yearDirectoryPath)
        yearDirectory.create()
        
        monthDirectoryPath = os.path.join(yearDirectoryPath, self.month)
        monthDirectory = Directory(monthDirectoryPath)
        monthDirectory.create()
        
        self.topicsFilePath = os.path.join(monthDirectoryPath, 'topics.json')
        self.countryFilePath = os.path.join(monthDirectoryPath, 'country_topics.json')
        self.personFilePath = os.path.join(monthDirectoryPath, 'person_topics.json')
        self.organizationFilePath = os.path.join(monthDirectoryPath, 'organization_topics.json')
        return
        
    def __getWordDirectory(self, wordKey):
        wordsDirectory = Directory(self.wordsPath)
        wordsDirectory.create()
        
        wordDirectoryPath = os.path.join(self.wordsPath, wordKey)
        wordDirectory = Directory(wordDirectoryPath)
        wordDirectory.create()
        
        yearDirectoryPath = os.path.join(wordDirectoryPath, self.year)
        yearDirectory = Directory(yearDirectoryPath)
        yearDirectory.create()
        return wordDirectoryPath
    
    def __reset(self):
        self.date = None
        self.link = None
        self.year = None
        self.month = None
        self.day = None
        self.common = {}
        self.topicsFilePath = None
        self.countryFilePath = None
        self.personFilePath = None
        self.organizationFilePath = None
        self.commonDataFilePath = os.path.join(self.gcPath, 'common.json')
        self.__loadCommonData()
        self.__loadShortCountryNames()
        return
    
    def __loadCommonData(self):
        self.common = self.file.read(self.commonDataFilePath)
        if self.common and len(self.common.keys()):
            return
        self.common = {
            'total': 0,
            'max_date': '',
            'min_date': '',
        }
        return
    
    def __loadPerson(self):
        self.person = self.file.read(self.personFilePath)
        if not self.person:
            self.person = {}
        return
    
    def __loadTopics(self):
        self.topics = self.file.read(self.topicsFilePath)
        if not self.topics:
            self.topics = {}
        return
    
    def __loadOrganization(self):
        self.organization = self.file.read(self.organizationFilePath)
        if not self.organization:
            self.organization = {}
        return
    
    def __loadCountries(self):
        self.countries = self.file.read(self.countryFilePath)

        if self.countries and len(self.countries.keys()):
            return

        filePath = os.path.join(self.mapsDirectoryPath, 'countries.json')
        items = self.file.read(filePath)

        self.countries = {}
        for item in items:
            self.countries[item['name'].lower()] = {
                'id': item['id'],
                'display': item['name'],
                'total_block_count': 0,
                'key': self.__getKey(item['name']),
                'count_per_day': {}
            }
        return

    def __loadShortCountryNames(self):
        shortfilePath = os.path.join(self.mapsDirectoryPath, 'short_name_countries.json')
        self.shortCountryNames = self.file.read(shortfilePath)
        return

    def __getKey(self, word):
        keys = word.split(' ')
        key = keys[-1]
        return self.stemmer.stem(key.lower())
    
    def __getCountyName(self, name):
        name = name.lower()
        if name in self.countries.keys():
            return name
        if name in self.shortCountryNames.keys():
            return self.shortCountryNames[name]
        return None
    
    def __updateCommon(self):
        if self.isNew:
            self.common['total'] += 1
            if self.year not in self.common.keys():
                self.common[self.year] = {}
            if self.month not in self.common[self.year].keys():
                self.common[self.year][self.month] = 0
            self.common[self.year][self.month] += 1
        if self.__shouldResetMaxDate():
            self.common['max_date'] = self.date

        if self.__shouldResetMinDate():
            self.common['min_date'] = self.date
            
        return
    
    def __isGreaterThanMin(self):
        date = self.__strToDate(self.date)
        minDate = self.__strToDate(self.dataDates['min'])
        return date > minDate
    
    def __shouldResetMaxDate(self):
        if not self.common['max_date']:
            return True
        date = self.__strToDate(self.date)
        maxDate = self.__strToDate(self.common['max_date'])
        return maxDate < date

    def __shouldResetMinDate(self):
        if not self.common['min_date']:
            return True
        date = self.__strToDate(self.date)
        minDate = self.__strToDate(self.common['min_date'])
        return minDate > date

    def __strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def __getFormattedMonthOrDay(self, number):
        if int(number) < 10:
            return '0' + number
        return number



