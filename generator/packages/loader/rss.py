import json, datetime, re
from .core import Core
from .bbc import BBC
from .tpl import TPL
import sys

class RSS(Core):
    
    def __init__(self, path, type = "bbc"):
        super().__init__()
        self.directoryPath = path
        self.contentLoader = None
        if (type == "bbc"):
            self.contentLoader = BBC()
        if (type == "tpl" or type == "tpl_lc"):
            self.contentLoader = TPL(path)
        return
    
    def getDetails(self, item):
        if not self.contentLoader:
            return {}
        return self.contentLoader.fetchPage(item['link'])