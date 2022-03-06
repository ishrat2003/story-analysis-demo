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
from file.json import Json as JsonFile


logging.info("# Starting converting participant details")
logging.info("# ================================")

scriptParams = Params()
params = scriptParams.get()

#######
# 5 folders: all, 1 per task_key
# 2 colums per task_condition
# ease, time_taken_in_seconds
##
#
#######
# lc.csv : "story_link","user_code","ease"","task_condition","task_key","task_level","time_taken_in_seconds","what","when_happened","where_location","who","why"
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

data = {}

for line in lcLines:
    index = 0
    row = {}
    taskKey = None
    userCode = None
    for column in lcHeaders:
        if column in ["ease","time_taken_in_seconds", "user_code", "task_condition", "task_key"]:
            row[column] = line[index]
        if column == 'task_key':
            taskKey = line[index].strip()
        if column == 'user_code':
            userCode = line[index].strip()
        index += 1
    if (taskKey not in data.keys()):
        data[taskKey] = {}
              
    if (re.search("^GOLD_", userCode) and userCode != 'GOLD_10'):
        data[taskKey][userCode] = row

reviewfilePath = os.path.join(params.source_directory, 'review_lc.csv')
reviewFile = File(reviewfilePath)
reviewFileLines = reviewFile.read()
reviewFileHeaders = reviewFile.getHeaders()

for line in reviewFileLines:
    index = 0
    taskKey = None
    reviews = {}
    reviewerCode = None
    userCode = None
    storyKey = None
    for storyKeySuffix in ["", "2", "3", "4"]:
        review = {}
        index = 0
        for column in reviewFileHeaders:
            if column == 'Reviewer code':
                reviewerCode = line[index].strip()
            elif column == 'User code':
                userCode = line[index].strip()
            elif column == 'Story key' + storyKeySuffix:
                storyKey = line[index].strip()
            
            keys = [
                "When" + storyKeySuffix,
                "Who" + storyKeySuffix,
                "What" + storyKeySuffix,
                "Where" + storyKeySuffix,
                "Why" + storyKeySuffix,
                "Is summary true (i.e. stated in the main story)" + storyKeySuffix,
                "Summary (5 = good, 1 = poor)" + storyKeySuffix
            ]
            if column in keys:
                fieldKey = re.sub(r"[0-9]+$", "", column)
                review[fieldKey] = line[index]
                
            index += 1
        
        
        if (re.search("^GOLD_", userCode) and userCode != 'GOLD_10'):
            if 'review' not in data[storyKey][userCode].keys():
                data[storyKey][userCode]['review'] = {}
            data[storyKey][userCode]['review'][reviewerCode] = review
        
        
rawFilePath = os.path.join(params.destination_directory, 'summary.json')
file = JsonFile()
file.write(rawFilePath, data)

# Preparing ease

fields = [
    {
        "fieldName": 'ease',
        "directoryName": 'ease',
        "in_review": False
    },
    {
        "fieldName": 'time_taken_in_seconds',
        "directoryName": 'time_taken_in_seconds',
        "in_review": False
    },
    {
        "fieldName": 'When',
        "directoryName": 'when',
        "in_review": True,
        "values": {
            "Valid": 1,
            "Invalid": 0
        },
        "operation": "most"
    },
    {
        "fieldName": 'Who',
        "directoryName": 'who',
        "in_review": True,
        "values": {
            "Wrong identification": 0,
            "Some main characters are present": 1,
            "All main characters identified": 2
        },
        "operation": "most"
    },
    {
        "fieldName": 'What',
        "directoryName": 'what',
        "in_review": True,
        "values": {
            "Wrong identification": 0,
            "Some main topics are present": 1,
            "All main topics identified": 2
        },
        "operation": "most"
    },
    {
        "fieldName": 'Where',
        "directoryName": 'where',
        "in_review": True,
        "values": {
            "Wrong identification": 0,
            "Some main location are present": 1,
            "All main locations identified": 2
        },
        "operation": "most"
    },
    {
        "fieldName": 'Why',
        "directoryName": 'why',
        "in_review": True,
        "values": {
            "Wrong identification": 0,
            "Some main reasons are present": 1,
            "All main reasons identified": 2
        },
        "operation": "most"
    },
    {
        "fieldName": 'Is summary true (i.e. stated in the main story)',
        "directoryName": 'is_summary_true',
        "in_review": True,
        "values": {
            "True": 1,
            "Partially true": 0.5,
            "Not true": 0
        },
        "operation": "most"
    },
    {
        "fieldName": 'Is summary true (i.e. stated in the main story)',
        "directoryName": 'is_summary_true',
        "in_review": True,
        "values": {
            "True": 1,
            "Partially true": 0.5,
            "Not true": 0
        },
        "operation": "most"
    },
    {
        "fieldName": 'Summary (5 = good, 1 = poor)',
        "directoryName": 'summary',
        "in_review": True,
        "operation": "avg"
    }
]

for field in fields:
    fieldName = field["fieldName"]
    directoryName = field["directoryName"]
    
    all = { "text": [], "viz": []}
    for storyKey in data.keys():
        print('storyKey: ', storyKey)
        print('total items: ', len(data[storyKey].keys()))
        dataPoints = {}
        for userCode in data[storyKey].keys():
            taskCondition = data[storyKey][userCode]["task_condition"]
            if taskCondition not in dataPoints.keys():
                dataPoints[taskCondition] = []
            
            fieldValue = None
            if field["in_review"]:
                reviews = data[storyKey][userCode]["review"]

                if field["operation"] == "most":
                    values = {}
                    for reviewer in reviews:
                        review = reviews[reviewer]
                        if review[fieldName] not in values.keys():
                            values[review[fieldName]] = 0
                        values[review[fieldName]] += 1
                    
                    currentCount = 0
                    for value in values.keys():
                        if values[value] > currentCount:
                            fieldValue = field["values"][value]
                            currentCount = values[value]
                elif field["operation"] == "avg":
                    fieldValue = 0
                    count = 0
                    for reviewer in reviews.keys():
                        review = reviews[reviewer]
                        fieldValue += review[fieldName]
                        count += 1

                    if count:
                        fieldValue = fieldValue / count
            else:
               fieldValue = data[storyKey][userCode][fieldName]
            dataPoints[taskCondition].append(fieldValue)
            all[taskCondition].append(fieldValue)
            
        fileItems = []
        print('text total: ', len(dataPoints["text"]))
        print('viz total: ', len(dataPoints["viz"]))
        for i in range(0, 16):
            row = {
                "text": dataPoints["text"][i] if i < len(dataPoints["text"]) else '_',
                "viz": dataPoints["viz"][i] if i < len(dataPoints["viz"]) else '_'
            }
            fileItems.append(row)

        testFilePath = os.path.join(params.destination_directory, directoryName, storyKey + '.csv');
        writer = Csv()
        writer.remove(testFilePath)

        writeHeader = True
        for row in fileItems:
            writer.append(testFilePath, row, writeHeader)
            writeHeader = False
            
    allFilePath = os.path.join(params.destination_directory, directoryName, fieldName + '_all.csv');
    allWriter = Csv()
    allWriter.remove(allFilePath)
    allWriteHeader = True
    
    for i in range(0, len(all["text"])):
        row = {
            "text": all["text"][i],
            "viz": all["viz"][i]
        }
        allWriter.append(allFilePath, row, allWriteHeader)
        allWriteHeader = False

    



logging.info('Finished converting participant details')
logging.info("# ================================")


# python3 testDetails.py --source_directory ../resources/story_analysis_experiment_2021/user_input --destination_directory ../resources/story_analysis_experiment_2021/reviewed