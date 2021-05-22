import os, sys, logging, json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
filePath = os.path.dirname(os.path.abspath(__file__))

packagesPath = os.path.join(filePath, "../packages")
sys.path.append(packagesPath)

envPath = os.path.join(filePath, "../.env")
load_dotenv(dotenv_path=envPath)

from rss.feed import Feed

logging.info("# Starting fetching rss feeds")
logging.info("# ================================")

feedPath = os.path.join(filePath, "../resources/rss/bbc.json");
destinationPath = os.path.join(filePath, "../../feed");
feedProcessor = Feed(feedPath, destinationPath)
feedProcessor.process()

logging.info('Finished fetching rss feeds')
logging.info("# ================================")