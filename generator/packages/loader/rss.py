import json, datetime, re
from .core import Core
from .bbc import BBC
import sys

class RSS(Core):
    
    def __init__(self, type = "bbc"):
        super().__init__()
        self.contentLoader = BBC() if (type == "bbc") else None
        return

    
    def getDetails(self, item):
        if not self.contentLoader:
            return {}
        return self.contentLoader.fetchPage(item['link'])