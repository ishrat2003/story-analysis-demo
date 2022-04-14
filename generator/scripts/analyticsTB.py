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
from converter.analytics import Analytics as Writer
from converter.processor import Processor
from file.core import Core as File

logging.info("# Starting converting csv to collections")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()

loader = CSV()
writer = Writer(os.path.abspath(params.destination_directory))
processor = Processor(loader, writer)

filename = 'analytics_tb.csv'
filePath = os.path.join(os.path.abspath(params.source_directory), filename)
itemFile = File(filePath)
fileContent = itemFile.read() 
processor.setSourceFileName(filename)
processor.setHeaders(itemFile.getHeaders())
processor.process(fileContent)


# writer.saveItems();

logging.info('Finished converting csv to collections')
logging.info("# ================================")

# python3 analyticsTB.py --source_directory ../resources/story_analysis_experiment_2021/user_input --destination_directory ../resources/story_analysis_experiment_2021/processed