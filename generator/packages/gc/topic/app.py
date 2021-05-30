
import json
from charts.core import Core as Chart
from charts.rc import RC

def lambda_topic_handler(event, context):
    eventData = json.loads(event['body'])
    print(eventData)
    
    data = {}
    if(eventData and ('main_topic' in eventData.keys())):
        print('------- if --------')
        rcProcessor = RC(eventData)
        data = rcProcessor.getSubTopics()
    else:
        chartProcessor = Chart(eventData)
        chartProcessor.load()
        data = chartProcessor.get()
    
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Request-Method': '*',
            'Access-Control-Request-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "data": data
        })
    }


