import boto3

rekognition_client = boto3.client('rekognition')


def lambda_handler(event, context):
    step_state = event['Input']['Payload']
    rekognitionJobName = step_state['rekognitionJobName']
    
    response = rekognition_client.get_celebrity_recognition(JobId=rekognitionJobName)   
    celebs = response['Celebrities']
 
    list = []
    for celeb in celebs:
        list.append(celeb['Celebrity']['Name'])
        
    list= sorted(set(list))
    step_state['rekognitionJobStatus'] = response['JobStatus']

    table = boto3.resource('dynamodb').Table('media_store')
    wtable = boto3.resource('dynamodb').Table('celebs')
    
    celebStr = ', '.join(list)
    s3_key = step_state['s3_video_key']
    response = table.update_item(
        Key={
            'filename': s3_key.split('/')[-1].split('-')[0]
        },
        UpdateExpression="set celebrities=:t",
        ExpressionAttributeValues={
            ':t': celebStr
        },
        ReturnValues="UPDATED_NEW"
    )
    
    for w in list:
        wtable.put_item(Item= {'celeb': w})
    
    return step_state

