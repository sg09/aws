import boto3
import uuid

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    step_state = event['Input']
    s3_bucket = step_state['s3_bucket']
    s3_video_key = step_state['s3_video_key']

    #Prepare the parameters needed for the Transcribe job
    video_URI = f's3://{s3_bucket}/{s3_video_key}'
    jobName = f'{s3_video_key}-{str(uuid.uuid4())}'.replace('/','-')
    transcript_key = f'transcripts/{s3_video_key}-transcript.json'

    #Start the transcription job
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='en-US',
        Media={'MediaFileUri': video_URI},
        OutputBucketName=s3_bucket,
        OutputKey=transcript_key
    )

    #Add the transcript key and Transcribe job name to the state
    step_state['transcript_key'] = transcript_key
    step_state['TranscriptionJobName'] = response['TranscriptionJob']['TranscriptionJobName']

    return step_state

