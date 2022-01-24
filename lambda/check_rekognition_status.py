import boto3

rekognition_client = boto3.client('rekognition')

def lambda_handler(event, context):
    step_state = event['Input']['Payload']
    rekognitionJobName = step_state['rekognitionJobName']
    
    response = rekognition_client.get_celebrity_recognition(JobId=rekognitionJobName)   
    step_state['rekognitionJobStatus'] = response['JobStatus']

    return step_state

