#!/usr/bin/env python3
from aws_cdk import Stack, CfnOutput
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

        build_commands = build_commands or [
            "npm install",
            "npm run build",
            "cdk synth",
        ]  # noqa: E501

        owner, repo = repo_string.split("/")

        CodePipeline(
            self,
            "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    repo_string,
                    branch,
                    connection_arn=f"arn:aws:codestar-connections:{self.region}:{self.account}:connection/ea715684-208a-4756-ac77-b1ab5acd5dfe",  # noqa: E501
                ),
                commands=build_commands,
            ),
            self_mutation=True,
        )

        CfnOutput(self, "PipelineStackOutput", value="PipelineStack")
