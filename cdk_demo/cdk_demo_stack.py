from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
Stage,
Environment,
pipelines,
aws_codepipeline as codepipeline
)
from constructs import Construct
from resource_stack.resource_stack import Resource_Stack

class DeployStage(Stage):
    def __init__(self, scope:Construct, id:str,env: Environment, **kwargs ) -> None:
        super().__init__(scope,id,env=env,**kwargs)
        Resource_Stack(self, "Resource_Stack", env=env, stack_name="resource-stack-deploy")


class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_input=pipelines.CodePipelineSource.connection(
            repo_string="SRKKakarla/CDK_demo",
            branch="main",
            connection_arn="arn:aws:codeconnections:us-east-1:211125447900:connection/0e9933cd-59f0-4f53-8c2b-98c74dafbadd"
        )

        code_pipeline=codepipeline.Pipeline(
            self,"Pipeline",
            pipeline_name="new-pipeline",
            cross_account_keys=False
        )

        synth_step=pipelines.ShellStep(
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        pipeline= pipelines.CodePipeline(
            self, 'CodePipeline',
            self_mutation=True,
            code_pipeline=code_pipeline,
            synth=synth_step
        )

        deployment_wave=pipeline.add_wave("DeploymentWave")

        deployment_wave.add_stage(DeployStage(
            self, 'DeployStage',
            env=(Environment(account='211125447900', region='us-east-1'))
        ))







        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkDemoQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
