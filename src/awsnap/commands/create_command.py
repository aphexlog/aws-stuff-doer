import boto3
import json
import logging
from aws_cdk import App
from .pipeline_stack import PipelineStack

logging.basicConfig(level=logging.INFO)


def create_pipeline(repo_string, branch="main", build_commands=None):
    logging.info(
        f"Starting pipeline creation: {repo_string}, {branch}, {build_commands}"  # noqa: E501
    )

    app = App()
    stack = PipelineStack(
        app,
        "MyPipelineStack",
        repo_string=repo_string,
        branch=branch,
        build_commands=build_commands,
    )

    # Synthesize the CloudFormation template
    cfn_template = app.synth().get_stack_by_name(stack.stack_name).template

    # Convert the template to JSON
    template_body = json.dumps(cfn_template)

    # Use boto3 to deploy the template
    cloudformation_client = boto3.client(
        "cloudformation", region_name="us-east-1"
    )  # noqa: E501

    try:
        # Try to create the stack
        cloudformation_client.create_stack(
            StackName=stack.stack_name,
            TemplateBody=template_body,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            # Include any other parameters required for stack creation
        )
        logging.info(f"Stack creation initiated for {stack.stack_name}")
    except cloudformation_client.exceptions.AlreadyExistsException:
        # If the stack already exists, update it
        cloudformation_client.update_stack(
            StackName=stack.stack_name,
            TemplateBody=template_body,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            # Include any other parameters required for stack update
        )
        logging.info(f"Stack update initiated for {stack.stack_name}")
    except Exception as e:
        logging.error(f"Error deploying stack: {e}")
