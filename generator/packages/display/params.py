import argparse
import os
import logging
import json

class Parser:

  def __init__(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument('--source_directory')
    self.parser.add_argument('--destination_directory')
    self.parser.add_argument('--total_topics', default=0, help = "Total top topics to be displayed in GC")
    self.parser.add_argument('--year', default='2021', help = "Year(YYYY) to process. Ex: 2021")
    self.parser.add_argument('--month', default='05', help = "Month(mm) to process. Ex: 05")
    return

  def get(self):
    return self.parser.parse_args()
