#!/usr/bin/env python3
from aws_cdk import Stack, CfnOutput, aws_codestarconnections as codestar
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

        build_commands = build_commands or [
            "npm install",
            "npm run build",
            "cdk synth",
        ]  # noqa: E501

        repo_string = repo_string.split(":")[1]
        owner, repo = repo_string.split("/")

        CodePipeline(
            self,
            "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    repo_string,
                    branch,
                    connection_arn=connection.attr_connection_arn,
                ),
                commands=build_commands,
            ),
            self_mutation=True,
        )

        CfnOutput(self, "PipelineStackOutput", value="PipelineStack")
