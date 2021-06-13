import argparse
import os
import logging
import json

class Params:

  def __init__(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument('--source')
    self.parser.add_argument('--source_directory')
    self.parser.add_argument('--destination_directory')
    self.parser.add_argument('--store', default='local', help = "Type of store. Ex: local")
    self.parser.add_argument('--start', default='2021-05-24', help = "Inclusive strat day (dd). Ex: 01")
    self.parser.add_argument('--end', default='2021-05-30', help = "Inclusive end day (dd). Ex: 31")
    return

  def get(self):
    return self.parser.parse_args()