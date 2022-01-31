from constructs import Construct
from random import randint, randrange
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_stepfunctions as _aws_stepfunctions,
    aws_stepfunctions_tasks as _aws_stepfunctions_tasks,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito
)


class SampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "api-gateway-upload-to-s3")
        endpoint = api.root.add_resource("bucket")
        endpoint.add_method("PUT")

        bucket = s3.Bucket(self, "videobucket-"+str(randint(100, 999)))

        submit_lambda = _lambda.Function(self, 'submitLambda',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         code=_lambda.Code.from_asset('lambdas/trigger_aws_rekognition'))

        status_lambda = _lambda.Function(self, 'statusLambda',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         code=_lambda.Code.from_asset('lambdas/check_rekognition_status'))


        submit_job = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Submit Rekognition Job",
            lambda_function=submit_lambda,
            output_path="$.Payload",
        )

        wait_job = _aws_stepfunctions.Wait(
            self, "Wait 45 Seconds",
            time=_aws_stepfunctions.WaitTime.duration(
                Duration.seconds(45))
        )

        status_job = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Get Status",
            lambda_function=status_lambda,
            output_path="$.Payload",
        )

        fail_job = _aws_stepfunctions.Fail(
            self, "Rekognition Fail",
            cause='Rekognition Job Failed',
            error='Rekognition returned FAILED'
        )

        submit_to_dynamo_lambda = _lambda.Function(self, 'rekogSuccessLambda',
                                                   handler='lambda_function.lambda_handler',
                                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                                   code=_lambda.Code.from_asset('lambdas/push_rekognition_results_to_dynamodb'))

        succeed_job = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Push rekognition to Dynamo Job",
            lambda_function=submit_to_dynamo_lambda,
            output_path="$.Payload",
        )

        # Create Chain

        definition = submit_job.next(wait_job) \
            .next(status_job) \
            .next(_aws_stepfunctions.Choice(self, 'Rekognition Job Complete?')
                  .when(_aws_stepfunctions.Condition.string_equals('$.status', 'FAILED'), fail_job)
                  .when(_aws_stepfunctions.Condition.string_equals('$.status', 'SUCCEEDED'), succeed_job)
                  .otherwise(wait_job))

        # Create state machine
        sm = _aws_stepfunctions.StateMachine(
            self, "StateMachine1",
            definition=definition,
            timeout=Duration.minutes(15),
        )

        ########
        submit_lambda_tran = _lambda.Function(self, 'submitLambdaTran',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         code=_lambda.Code.from_asset('lambdas/trigger_aws_transcribe'))

        status_lambda_tran = _lambda.Function(self, 'statusLambdaTran',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         code=_lambda.Code.from_asset('lambdas/check_transcribe_status'))

        # Step functions Definition

        submit_job_tran = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Submit Transcription Job",
            lambda_function=submit_lambda_tran,
            output_path="$.Payload",
        )

        wait_job_tran = _aws_stepfunctions.Wait(
            self, "Wait 30 Seconds",
            time=_aws_stepfunctions.WaitTime.duration(
                Duration.seconds(30))
        )

        status_job_tran = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Get Transcription Status",
            lambda_function=status_lambda_tran,
            output_path="$.Payload",
        )

        fail_job_tran = _aws_stepfunctions.Fail(
            self, "Transcribe Fail",
            cause='Transcription Job Failed',
            error='Transcription returned FAILED'
        )

        submit_to_dynamo_lambda_tran = _lambda.Function(self, 'TranscriptionSuccessLambda',
                                                   handler='lambda_function.lambda_handler',
                                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                                   code=_lambda.Code.from_asset(
                                                       'lambdas/trigger_aws_comprehend'))

        succeed_job_tran = _aws_stepfunctions_tasks.LambdaInvoke(
            self, "Push Transcription results to Dynamo Job",
            lambda_function=submit_to_dynamo_lambda_tran,
            output_path="$.Payload",
        )

        # Create Chain

        definition_tran = submit_job_tran.next(wait_job_tran) \
            .next(status_job_tran) \
            .next(_aws_stepfunctions.Choice(self, 'Transcribe Job Complete?')
                  .when(_aws_stepfunctions.Condition.string_equals('$.status', 'FAILED'), fail_job_tran)
                  .when(_aws_stepfunctions.Condition.string_equals('$.status', 'SUCCEEDED'), succeed_job_tran)
                  .otherwise(wait_job_tran))

        # Create state machine
        sm_tran = _aws_stepfunctions.StateMachine(
            self, "StateMachineTranscribe",
            definition=definition_tran,
            timeout=Duration.minutes(15),
        )

        table = dynamodb.Table(self, "media_store",
                               partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
                               )

        pool = cognito.UserPool(self, "userPool")
        pool.add_client("user-pool-app-client",
                        o_auth=cognito.OAuthSettings(
                            flows=cognito.OAuthFlows(
                                authorization_code_grant=True
                            ),
                            scopes=[cognito.OAuthScope.OPENID],
                            callback_urls=["https://domain.com/welcome"],
                            logout_urls=["https://domain.com/signin"]
                        )
                        )
