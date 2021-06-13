import os, sys, logging, json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
filePath = os.path.dirname(os.path.abspath(__file__))

packagesPath = os.path.join(filePath, "../packages")
sys.path.append(packagesPath)

envPath = os.path.join(filePath, "../.env")
load_dotenv(dotenv_path=envPath)

from params.core import Core as Params
from filesystem.directory import Directory
from loader.rss import RSS
from corpus.writer import Writer
from corpus.context import Context

logging.info("# Starting building corpus collections")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()
loader = RSS(params.source_directory, params.source)

writer = Writer(params.destination_directory)
processor = Context(loader, writer, params.total_items)

sourceDirectory = Directory(params.source_directory)
sourceDirectory.process(processor, params.total_items)

logging.info('Finished building corpus collection')
logging.info("# ================================")