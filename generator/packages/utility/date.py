import datetime

class Date:

    """ return date object from string """
    @staticmethod
    def strToDate(date):
        return datetime.datetime.strptime(date[0:10], '%Y-%m-%d')
    
    """ return formatted month or day in 2 digits """
    @staticmethod
    def getFormattedMonthOrDay(number):
        intNumber = int(number)
        if intNumber < 10:
            return '0' + str(intNumber)
        return str(number)
    
    """ return if date in range """
    @staticmethod
    def dateInRange(date, start, end):
        if not date:
            return False

        if not start and not end:
            return True

        date = Date.strToDate(date)

        if start:
            start = Date.strToDate(start)
            
        if date < start:
            return False

        if end:
            end = Date.strToDate(end)
            
        if date > end:
            return False
        return True
    
    """ return date to string """
    @staticmethod
    def dateToString(date):
        return str(date.year) + Date.getFormattedMonthOrDay(date.month) + Date.getFormattedMonthOrDay(date.day)
    
    """ return date to string """
    @staticmethod
    def getMinMax(date, min = None, max = None):
        if not min or min > date:
            min = date
        if not max or max < date:
            max = date
        return min, max
    







