import os, sys, logging, json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
filePath = os.path.dirname(os.path.abspath(__file__))

packagesPath = os.path.join(filePath, "../packages")
sys.path.append(packagesPath)

envPath = os.path.join(filePath, "../.env")
load_dotenv(dotenv_path=envPath)

from display.params import Params
from filesystem.directory import Directory
from display.writer import Writer
from corpus.reader import Reader
from display.generator import Generator
from loader.bbc import BBC
from loader.tpl import TPL

logging.info("# Starting building json files for visualization")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()


print(params)
loader = BBC() if params.source == 'bbc' else TPL(params.source_directory + '/' + params.source)
writer = Writer(params.destination_directory, params)
reader = Reader(params)
generatorProcessor = Generator(params, reader, writer, loader)
generatorProcessor.process()

logging.info('Finished building json files for visualization')
logging.info("# ================================")