import boto3
import json

def lambda_handler(event, context):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
                
    text = event['text']
    print('Calling DetectSentiment')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    print(json.dumps(response))
    
    response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    print(json.dumps(response))
    
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    print(json.dumps(response))
    
    response = comprehend.detect_dominant_language(Text=text)
    print(json.dumps(response))

    print('End of DetectSentiment\n')
