#!/usr/bin/env python3
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_codestarconnections as codestar,
    aws_codepipeline as codepipeline,
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from constructs import Construct


class PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        repo_string: str,  # Format: "owner/repo"
        branch: str = "main",
        build_commands: list = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        connection = codestar.CfnConnection(
            self,
            "Connection",
            connection_name="awsnap-connection",
            provider_type="GitHub",  # or "Bitbucket", "GitHubEnterpriseServer"
        )

        install_commands = [
            "npm install -g aws-cdk",
            "pip install -r requirements.txt",
        ]

        build_commands = build_commands or [
            "cdk synth",
        ]

        repo_string = repo_string.split(":")[1]
        owner, repo = repo_string.split("/")

        myPipeline = codepipeline.Pipeline(
            self,
            "MyPipeline",
            pipeline_name="awsnap-pipeline",
            cross_account_keys=False,
            restart_execution_on_update=True,
        )

        pipeline = CodePipeline(
            self,
            "Pipeline",
            synth=ShellStep(
                "Synth",
                install_commands=install_commands,
                input=CodePipelineSource.connection(
                    repo_string,
                    branch,
                    connection_arn=connection.attr_connection_arn,
                ),
                commands=build_commands,
            ),
            self_mutation=True,
            code_pipeline=myPipeline,
        )

        pipeline.node.add_dependency(connection)

        CfnOutput(self, "PipelineStackOutput", value="PipelineStack")
