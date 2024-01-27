""" This module defines the pipeline stack. """
from typing import Optional
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_codestarconnections as codestar,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codebuild as codebuild,
)
from constructs import Construct


class PipelineStack(Stack):
    """
    This stack creates a pipeline that will build and dloy the CDK stack.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        repo_string: str,  # Format: "owner/repo"
        branch: str = "main",
        build_commands: Optional[list] = None,
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

        # Define the artifact representing the source code
        source_output = codepipeline.Artifact()
        # Define the artifact representing the synthesized CloudFormation template # noqa: E501
        cdk_output = codepipeline.Artifact()

        # Create a pipeline
        my_pipeline = codepipeline.Pipeline(
            self,
            "MyPipeline",
            pipeline_name="awsnap-pipeline",
            cross_account_keys=False,
            restart_execution_on_update=True
        )

        # Add source stage to pipeline
        my_pipeline.add_stage(
            stage_name="Source",
            actions=[
                cpactions.CodeStarConnectionsSourceAction(
                    action_name="CodeStar_Source",
                    owner=owner,
                    repo=repo,
                    branch=branch,
                    output=source_output,
                    connection_arn=connection.attr_connection_arn,
                )
            ],
        )

        # type IProject
        synth_project = codebuild.PipelineProject(
            self,
            "SynthProject",
            ssm_session_permissions=True,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5,  # noqa: E501
                privileged=True,
            ),
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "install": {
                            "commands": install_commands,
                        },
                        "build": {
                            "commands": build_commands,
                        },
                    },
                    "artifacts": {
                        "base-directory": "cdk.out",
                        "files": ["*"],
                    },
                }
            ),
        )

        # Add synth stage to pipeline
        my_pipeline.add_stage(
            stage_name="Build",
            actions=[
                cpactions.CodeBuildAction(
                    action_name="CDK_Synth",
                    project=synth_project,
                    input=source_output,
                    outputs=[cdk_output],
                ),
            ],
        )

        # Add deploy stage to pipeline
        my_pipeline.add_stage(
            stage_name="Deploy",
            actions=[
                cpactions.CloudFormationCreateUpdateStackAction(
                    action_name="CFN_Deploy",
                    template_path=cdk_output.at_path(
                        "hal9000-chatbot.template.json",
                    ),  # noqa: E501
                    stack_name="MyDeploymentStack",
                    admin_permissions=True,
                ),
            ],
        )

        # Add connection to pipeline
        my_pipeline.node.add_dependency(connection)

        CfnOutput(self, "PipelineStackOutput", value="PipelineStack")
