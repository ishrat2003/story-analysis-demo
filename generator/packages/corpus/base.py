import datetime

class Base:
    
    def shouldValidDate(self, date, start, end):
        if not date:
            return False
        
        if not start and not end:
            return True
        
        date = self._strToDate(date)
        
        if start:
            start = self._strToDate(start)
            if date < start:
                return False
        
        if end:
            end = self._strToDate(end)
            if date > end:
                return False
        return True
    
    def _strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def _getFormattedMonthOrDay(self, number):
        intNumber = int(number)
        if intNumber < 10:
            return '0' + str(intNumber)
        return number

