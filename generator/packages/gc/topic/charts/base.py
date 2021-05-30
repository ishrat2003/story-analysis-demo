import datetime, operator

class Base:
    
    def __init__(self, params):
        self.dataDates = {
            'max': None,
            'min': None
        }
        self.params = params
        return
    
    def loadDataDates(self, data):
        print('----- load data dates')
        minYear, maxYear = self.getMaxMin(data.keys())

        minMonthOfMinYear, _ = self.getMaxMin(data[minYear].keys(), 'month')
        _, maxMonthOfMaxYear = self.getMaxMin(data[maxYear].keys(), 'month')
        formattedMinMonthOfMinYear = self.getFormattedMonthOrDay(minMonthOfMinYear)
        formattedMaxMonthOfMaxYear = self.getFormattedMonthOrDay(maxMonthOfMaxYear)

        minDayOfminMonthOfMinYear, _ = self.getMaxMin(data[minYear][minMonthOfMinYear].keys(), 'day')
        _, maxDayOfMaxMonthOfMaxYear = self.getMaxMin(data[maxYear][maxMonthOfMaxYear].keys(), 'day')
        formattedMaxDayOfMaxMonthOfMaxYear = self.getFormattedMonthOrDay(maxDayOfMaxMonthOfMaxYear)
        formattedMinDayOfminMonthOfMinYear = self.getFormattedMonthOrDay(minDayOfminMonthOfMinYear)

        self.dataDates = {
            'max': maxYear + '-' + formattedMinMonthOfMinYear + '-' + formattedMaxDayOfMaxMonthOfMaxYear,
            'min': minYear + '-' + formattedMaxMonthOfMaxYear + '-' + formattedMinDayOfminMonthOfMinYear
        }
        print('?????? dates', self.dataDates)
        return
    
    def setStart(self):
        print('params--', self.params)
        if (('start' not in self.params.keys()) 
            or not self.params['start'] 
            or (self.params['start'] != '' 
                and self.isLessThanMin(self.params['start']))
            ):
            self.dataDates['start'] = self.dataDates['min']
        else:
            self.dataDates['start'] = self.params['start']
        return
    
    def setEnd(self):
        if (('end' not in self.params.keys()) 
            or not self.params['end'] 
            or self.isGreaterThanMax(self.params['end'])):
            self.dataDates['end'] = self.dataDates['max']
        else:
            self.dataDates['end'] = self.params['end']
        return
    
    def isGreaterThanMax(self, date):
        date = self.strToDate(date)
        minDate = self.strToDate(self.dataDates['max'])
        return date > minDate
    
    def isLessThanMin(self, date):
        date = self.strToDate(date)
        maxDate = self.strToDate(self.dataDates['min'])
        return date < maxDate
    
    def strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def getFormattedMonthOrDay(self, number):
        number = int(number)
        if int(number) < 10:
            return '0' + str(number)
        return str(number)

    def getMaxMin(self, items, type = 'year'):
        now = datetime.datetime.now()
        if not items:
            items = [now[type]]
        listKeys = list(map(int, items))
        listKeys = sorted(listKeys)
        totalItems = len(listKeys)
        min = listKeys[0]
        max = listKeys[totalItems - 1]
        return str(min), str(max)
    
    def sort(self, items, attribute='total_block_count_in_range', reverse=True, minValue = 0):
        if not len(items.keys()):
            return []

        sortedTopics = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=reverse):
            if not isinstance(value[attribute], int) or (value[attribute] > minValue):
                sortedTopics.append(value)

        return sortedTopics
    
    def getSplited(self, date):
        return [int(x) for x in date.split("-")]
    
    def unformattedStrToDate(self, date):
        year, month, day = self.getSplited(date)
        return self.strToDate(str(year) + '-' + str(self.getFormattedMonthOrDay(month)) + '-' + str(self.getFormattedMonthOrDay(day)))
        
