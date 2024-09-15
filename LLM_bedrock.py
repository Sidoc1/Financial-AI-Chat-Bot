import json
import boto3
from Sec_Cik_Lookup import Lookup

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    try:
        # Define the bucket name and file key
        bucket_name = 'sec-edgar-json-files1'
        file_key = 'company_tickers_exchange.json'

        # Fetch the file from S3
        s3_response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = s3_response['Body'].read().decode('utf-8')  # Log file content
        
        # Initialize the Lookup object with the file content
        json_content = json.loads(file_content)


        lk = Lookup(json_content)
        
        

        request_type = event.get('request_type')
        company_name = event.get('company')
        year = event.get('year')

        company_cik = str(lk.name_to_cik(company_name)[0])
        document = ""

        if request_type == 'Annual':
            document = lk.annual_filing(company_cik, year)
        elif request_type == 'Quarter':
            quarter = event.get('quarter')
            if not quarter:
                return {
                    'statusCode': 400,
                    'body': json.dumps('Missing required parameter: quarter.')
                }
            document = lk.quater_filing(company_cik, year, quarter)  # Corrected typo here
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid request_type. Must be "Annual" or "Quarter".')
            }
       
        # Convert bytes to string if necessary
        if isinstance(document, bytes):
            document = document.decode('utf-8')
    
        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps(document)
        }

    except KeyError as e:
        return {
            'statusCode': 404,
            'body': json.dumps(f'Company not found: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }