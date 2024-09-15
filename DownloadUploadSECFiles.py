import boto3
import json
from urllib import request
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    url = "https://www.sec.gov/files/company_tickers_exchange.json"  # replace with the actual URL
    
    try:
        # Create a request with custom headers if needed
        req = request.Request(url, headers={'User-Agent': 'sadaq abdulle abdulle4@augsburg.edu'})

        # Make the HTTP request using urllib
        with request.urlopen(req) as response:
            data = response.read()
            
            # Upload the data to S3
            s3.put_object(Bucket='sec-edgar-json-files1', Key='company_tickers_exchange.json', Body=data)
        
        return {
            'statusCode': 200,
            'body': json.dumps('File successfully uploaded to S3')
        }
    
    except Exception as e:
        # Handle exceptions and errors
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {e}")
        }