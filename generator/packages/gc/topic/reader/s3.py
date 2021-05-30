import boto3
import os

class S3():
    
    def __init__(self):
        self.client =  boto3.client( 's3',
            region_name = os.environ['REGION'],
            endpoint_url= os.environ['S3_ENDPOINT']
        );
        self.bucket = 'story-analysis-rc'
        return
    
    def getContent(self, key):
        try:
            return self.client.get_object(Bucket = self.bucket, Key = key)
        except:
            return None
        

