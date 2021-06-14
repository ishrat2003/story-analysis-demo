from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import regex as re
import operator
import sys

class Scanner:
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        return
    
    def scan(self, text, wordKey, limit = 3):
        self.sentenceWords = {}
        self.loadRelationsMatchingSentences(text, wordKey)
        sortedWords = self.sort()
        return sortedWords[0:limit] if sortedWords else []
    
    def loadRelationsMatchingSentences(self, text, wordKey):
        items = re.finditer('[^!\?\.\n]*' + wordKey + '[^!\?\.\n]*[!\.\?\n]', text.lower())
        for item in items:
            self.loadSecondaryLevelWords(item.group(0), wordKey)
        return items
    
    
    def loadSecondaryLevelWords(self, sentence, currentWordKey):
        allowedPOSTypes = ['NN', 'NNS', 'NNP', 'NNPS']
        sentence = re.sub(r'\'[a-z]{1,2}\s', r' ', sentence)
        sentence = re.sub(r'[^0-9a-zA-Z\-\s]+', r' ', sentence)
        sentence = re.sub(r'\s+', r' ', sentence)
        words = pos_tag(word_tokenize(sentence))
        
        for word in words:
            (wordDisplay, type) = word
            wordKey = self.stemmer.stem(wordDisplay)
            if (type not in allowedPOSTypes) or (wordKey == currentWordKey):
                continue
            
            if wordKey not in self.sentenceWords.keys() and len(wordKey) >= 2:
                self.sentenceWords[wordKey] = {
                    'display': wordDisplay[0].upper() + wordDisplay[1:],
                    'stemmed_word': wordKey,
                    'count': 0
                }
            self.sentenceWords[wordKey]['count'] += 1

        return
    
    def sort(self, attribute='count'):
        if not len(self.sentenceWords):
            return

        sortedWords = []
        contributors = self.sentenceWords.values()

        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=True):
            sortedWords.append(value)

        return sortedWords