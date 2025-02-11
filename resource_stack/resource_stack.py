from aws_cdk import (
Stack,
aws_sqs as sqs,
Duration,
aws_lambda as my_lambda,
aws_s3 as s3
)

from constructs import Construct

class Resource_Stack(Stack):
    def __inti__(self, scope: Construct, construct_id:str, **kwargs) -> None:
        super().__init__(scope,construct_id,**kwargs)
        queue =sqs.Queue(
            self, "AWSCDKCodeDemoQueue",
            visibility_timeout=Duration.seconds(300),
            queue_name="demo_queue"
        )

        function = my_lambda.Function(self,
                                      "DemoCDKLambda",
                                      runtime=my_lambda.Runtime.PYTHON_3_9,
                                      code= my_lambda.Code.from_asset('./lambda_code_demo'),
                                      handler="demo_lambda.lambda_handler")

        bucket=s3.Bucket(self, "MyFirstBucket", versioned=True,
                         bucket_name="demo_bucket",
                         block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
