import os, sys, logging, json, re
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
filePath = os.path.dirname(os.path.abspath(__file__))

packagesPath = os.path.join(filePath, "../packages")
sys.path.append(packagesPath)

envPath = os.path.join(filePath, "../.env")
load_dotenv(dotenv_path=envPath)

from params.converter import Converter as Params
from filesystem.directory import Directory
from file.csv import Csv
from file.core import Core as File

logging.info("# Starting converting participant details")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()
# lc.csv : "story_link","user_code","age_group","agreed","close_date_time","close_timestamp","created","department","disability","ease","environment","experiment_date_datepicker","gender","id","open_date_time","open_timestamp","story_date","story_source","story_title","summary","task_condition","task_key","task_level","time_taken_in_seconds","what","when_happened","where_location","who","why"
# review-lc.csv ID,Start time,Completion time,Email,Name,Reviewer code,User code,Story key,When,Who,What,Where,Why,Is summary true (i.e. stated in the main story),"Summary (5 = good, 1 = poor)",
# Story key2,When2,Who2,What2,Where2,Why2,Is summary true (i.e. stated in the main story)2,"Summary (5 = good, 1 = poor)2",
# Story key3,When3,Who3,What3,Where3,Why3,Is summary true (i.e. stated in the main story)3,"Summary (5 = good, 1 = poor)3",
# Story key4,When4,Who4,What4,Where4,Why4,Is summary true (i.e. stated in the main story)4,Summary (5 = good 1 = poor)
#
# interview.csv ID,Start time,Completion time,Email,Name,User code,
# LC-What is the main challenge of the tasks in the task set A and B?,TB-What is the main challenge of the tasks in the task set C and D?,LC-The LC visualisation along with the text is useful (5 = strongly agree  - 1 = disagree),LC-Have you used the LC visualisation for better interpretation in the multi-document task? (5 = only used visualisation  - moderately used visualisation - 1 = didn't used visualisation),"TB-It was easier to form a story plan with only a list of documents? (5 = strongly agree, 1 = disagree)","TB-It was easier to form a story plan  with the TB visualisation (5 = strongly agree, 1 = disagree)","TB-TB visualisation was easy to use (5 = strongly agree, 1 = disagree)",LC-Notes
#
lcfilePath = os.path.join(params.source_directory, 'lc.csv')
lcFile = File(lcfilePath)
lcLines = lcFile.read()
lcHeaders = lcFile.getHeaders()

participantDetails = {}

for line in lcLines:
    index = 0
    row = {}
    for column in lcHeaders:
        if column in ["user_code","age_group","department","disability", "gender"]:
            row[column] = line[index]
        index += 1
    if (row["user_code"] not in participantDetails.keys()) and (re.search("^GOLD_", row["user_code"]) and row["user_code"] != 'GOLD_10'):
        participantDetails[row["user_code"]] = row

interviewfilePath = os.path.join(params.source_directory, 'interview.csv')
interviewFile = File(interviewfilePath)
interviewLines = interviewFile.read()
interviewHeaders = interviewFile.getHeaders()

print(interviewHeaders)
for line in interviewLines:
    index = 0
    row = {}
    userCode = None
    for column in interviewHeaders:
        if (column == "User code"):
            userCode = line[index]
        if re.search('^LC-', column):
            row[column] = line[index]
            if column == "LC-Notes":
                row[column] = re.sub(r"GOLD_[0-9]+\s*\(Task set C and D\).+$", "", row[column])
        index += 1
    if (userCode in participantDetails.keys()) and (re.search("^GOLD_", userCode) and userCode != 'GOLD_10'):
        participantDetails[userCode] = {
            **participantDetails[userCode],
            **row
        }
        print(participantDetails[userCode])
        print('-----------------------')


#print(participantDetails)

participantFilePath = os.path.join(params.destination_directory, 'participants.csv')

writer = Csv()
writer.remove(participantFilePath)

writeHeader = True
for user in participantDetails:
    writer.append(participantFilePath, participantDetails[user], writeHeader)
    writeHeader = False


logging.info('Finished converting participant details')
logging.info("# ================================")


# python3 dataSetDetails.py --source_directory ../resources/story_analysis_experiment_2021/user_input --destination_directory ../resources/story_analysis_experiment_2021/processed