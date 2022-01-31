import boto3
import json
import os
import uuid
from datetime import date

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    #Retrieve the state information
    step_state = event['Input']['Payload']

    #Get the S3 information for the file and transcript
    s3_bucket = step_state['s3_bucket']
    s3_video_key = step_state['s3_video_key']
    s3_transcript_key = step_state['transcript_key']

    base_video_key = os.path.basename(s3_video_key)
    base_transcript_key = os.path.basename(s3_transcript_key)

    #Retrieve the transcript from S3
    download_path = f'/tmp/{base_transcript_key}-{uuid.uuid4()}'
    s3_client.download_file(s3_bucket, s3_transcript_key, download_path)
    with open(download_path,'r') as local_transcript:
        transcribe_result = json.loads(local_transcript.read())
    transcripts = transcribe_result['results']['transcripts']

   
    #Date should be in YYYY/MM/DD format.
    output_date = date.today().strftime('%Y/%m/%d')
    output_folder = 'processed'

    output_loc = f'{output_folder}/{output_date}'

    #Move the video and transcript. This requires a copy then a delete.
    s3_client.copy_object(Bucket=s3_bucket,
    Key=f'{output_loc}/{base_video_key}',
    CopySource={'Bucket': s3_bucket, 'Key': s3_video_key})
    
    s3_client.copy_object(Bucket=s3_bucket,
    Key=f'{output_loc}/{base_transcript_key}',
    CopySource={'Bucket': s3_bucket, 'Key': s3_transcript_key})
    
    deletes = {'Objects': [{'Key': s3_video_key}, {'Key': s3_transcript_key}]}

    s3_client.delete_objects(Bucket=s3_bucket, Delete=deletes)
    step_state['output_folder'] = output_folder
    step_state['s3_processed_transcript_key'] = f'{output_loc}/{base_transcript_key}'

    return step_state
