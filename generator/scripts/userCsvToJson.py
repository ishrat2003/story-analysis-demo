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
from converter.user import User as Writer
from converter.processor import Processor

logging.info("# Starting converting csv to collections")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()

loader = CSV()
writer = Writer(os.path.abspath(params.destination_directory))
processor = Processor(loader, writer)


sourceDirectory = Directory(os.path.abspath(params.source_directory))
sourceDirectory.process(processor)
writer.saveUsers();

logging.info('Finished converting csv to collections')
logging.info("# ================================")

# python3 userCsvToJson.py --source_directory ../resources/story_analysis_experiment_2021/user_input --destination_directory ../resources/story_analysis_experiment_2021/processed