import datetime
from utility.date import Date

class Base:
    
    def shouldValidDate(self, date, start, end):
        # if not date:
        #     return False
        
        # if not start and not end:
        #     return True
        
        # date = self._strToDate(date)
        
        # if start:
        #     start = self._strToDate(start)
        #     if date < start:
        #         return False
        
        # if end:
        #     end = self._strToDate(end)
        #     if date > end:
        #         return False
        # return True
        return Date.dateInRange(date, start, end)
    
    def _strToDate(self, date):
        return Date.strToDate(date)
    
    def _getFormattedMonthOrDay(self, number):
        return Date.getFormattedMonthOrDay(number)

