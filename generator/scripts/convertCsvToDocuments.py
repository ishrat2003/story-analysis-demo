import os, sys, logging, json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
filePath = os.path.dirname(os.path.abspath(__file__))

packagesPath = os.path.join(filePath, "../packages")
sys.path.append(packagesPath)

envPath = os.path.join(filePath, "../.env")
load_dotenv(dotenv_path=envPath)

from params.converter import Converter as Params
from filesystem.directory import Directory
from loader.csv import CSV
from converter.list import List as Writer
from converter.processor import Processor

logging.info("# Starting converting csv to collections")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()

loader = CSV()
writer = Writer(params.destination_directory)
processor = Processor(loader, writer, params.total_items)

sourceDirectory = Directory(params.source_directory)
sourceDirectory.process(processor, params.total_files)

logging.info('Finished converting csv to collections')
logging.info("# ================================")