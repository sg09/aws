import boto3
import uuid

rekognition_client = boto3.client('rekognition')

def lambda_handler(event, context):
    #Retrieve the state information
    step_state = event['Input']
    s3_bucket = step_state['s3_bucket']
    s3_key = step_state['s3_video_key']

    #Start the  job
    response = rekognition_client.start_celebrity_recognition(
    Video={
        'S3Object': {
            'Bucket': s3_bucket,
            'Name': s3_key
            }
    },
    NotificationChannel={
        'SNSTopicArn': 'arn:aws:sns:us-east-1:xxxx:AmazonRekognitionTopic',
        'RoleArn': 'arn:aws:iam::xxxx:role/AmazonRekognitionServiceRole'
    },)

    
    step_state['rekognitionJobName'] = response['JobId']
    print(response['JobId'])
    return step_state

