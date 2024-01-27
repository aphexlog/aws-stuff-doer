import boto3
import json
from aws_cdk import App
import time
from botocore.exceptions import ClientError
from .synth import PipelineStack
import logging

def prompt_for_region():
    region = boto3.Session().region_name
    if not region:
        region = input(
            "Enter the region to deploy the pipeline to: "
        ).strip()  # noqa: E501
        if not region:
            logging.error("Region not provided. Exiting.")
            return
    return region


def create_pipeline(
    stack_name, repo_string, branch, build_commands, region=None
):  # noqa: E501
    logging.info(
        f"Starting pipeline creation: {repo_string}, {branch}, {build_commands}"  # noqa: E501
    )

    app = App()
    stack = PipelineStack(
        app,
        "PipelineStack",
        stack_name=stack_name,
        repo_string=repo_string,
        branch=branch,
        build_commands=build_commands,
    )

    # Synthesize the CloudFormation template
    app.synth()
    cfn_template = app.synth().get_stack_by_name(stack.stack_name).template

    # Convert the template to JSON
    template_body = json.dumps(cfn_template)

    # Use boto3 to deploy the template
    cloudformation_client = boto3.client(
        "cloudformation", region_name=region
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
        tail_cloudformation_logs(stack.stack_name, region)

        codestar_client = boto3.client(
            "codestar-connections", region_name=region
        )  # noqa: E501
        connection_status = codestar_client.get_connection(
            ConnectionArn="arn:aws:codestar-connections:us-east-1:764114738171:connection/20b3b732-da2f-4c37-a2e1-4528eea4ab90"  # noqa: E501
        )
        if connection_status["Connection"]["ConnectionStatus"] == "PENDING":
            print_activation_instructions(
                "awsnap-connection",
                "arn:aws:codestar-connections:us-east-1:764114738171:connection/20b3b732-da2f-4c37-a2e1-4528eea4ab90",  # noqa: E501
            )

    except cloudformation_client.exceptions.AlreadyExistsException:
        # If the stack already exists, update it
        cloudformation_client.update_stack(
            StackName=stack.stack_name,
            TemplateBody=template_body,
            Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            # Include any other parameters required for stack update
        )
        logging.info(f"Stack update initiated for {stack.stack_name}")
        tail_cloudformation_logs(stack.stack_name, region)
    except Exception as e:
        logging.error(f"Error deploying stack: {e}")


def delete_pipeline(stack_name, region=None):
    logging.info(f"Starting pipeline deletion: {stack_name}")

    # Prompt for region if not provided
    region = region or prompt_for_region()
    if not region:
        return  # Exit if no region is provided

    cloudformation_client = boto3.client(
        "cloudformation", region_name=region
    )  # noqa: E501

    try:
        cloudformation_client.delete_stack(StackName=stack_name)
        logging.info(f"Stack deletion initiated for {stack_name}")
        tail_cloudformation_logs(stack_name, region=region)
    except Exception as e:
        logging.error(f"Error deleting stack: {e}")


def tail_cloudformation_logs(stack_name, region=None):
    logging.info(f"Tailing logs for CloudFormation stack: {stack_name}")

    client = boto3.client("cloudformation", region_name=region)
    seen_events = set()

    while True:
        try:
            # Get the stack events
            response = client.describe_stack_events(StackName=stack_name)
            events = response["StackEvents"]
        except ClientError as e:
            # If the stack no longer exists, break from the loop
            if "does not exist" in e.response["Error"]["Message"]:
                logging.info(f"Stack {stack_name} no longer exists.")
                break
            else:
                raise

        # Display events in reverse order (newest first) and skip seen events
        for event in reversed(events):
            event_id = event["EventId"]
            if event_id not in seen_events:
                # Add event to the seen set
                seen_events.add(event_id)
                # Print the event details you're interested in
                timestamp = event["Timestamp"]
                resource_type = event["ResourceType"]
                logical_id = event["LogicalResourceId"]
                status = event["ResourceStatus"]
                reason = (
                    f" - Reason: {event['ResourceStatusReason']}"
                    if "ResourceStatusReason" in event
                    else ""
                )  # noqa: E501
                logging.info(
                    f"{timestamp} - {resource_type} - {logical_id} - {status}{reason}"  # noqa: E501
                )

        # Check if the stack creation or update is complete
        stack_description = client.describe_stacks(StackName=stack_name)
        stack_status = stack_description["Stacks"][0]["StackStatus"]
        if "COMPLETE" in stack_status or "FAILED" in stack_status:
            print_activation_instructions(
                "awsnap-connection",
                "arn:aws:codestar-connections:us-east-1:764114738171:connection/20b3b732-da2f-4c37-a2e1-4528eea4ab90",  # noqa: E501
                region=region,
            )
            break

        # Sleep for some time before polling again
        time.sleep(10)

    logging.info(
        f"Finished tailing logs for CloudFormation stack: {stack_name}"
    )  # noqa: E501


def print_activation_instructions(
    connection_name, connection_arn, region=None
):  # noqa: E501
    console_url = (
        # "https://console.aws.amazon.com/codesuite/settings/connections"  # noqa: E501
        f"https://{region}.console.aws.amazon.com/codesuite/settings/connections"  # noqa: E501
    )
    instructions = (
        f"To activate the CodeStar connection, please follow these steps:\n"
        f"1. Visit the AWS CodeStar Connections page: {console_url}\n"
        f"2. Find the connection named '{connection_name}' or use this ARN: {connection_arn}\n"  # noqa: E501
        f"3. Click on the connection to open its details.\n"
        f"4. Click the 'Connect' button and follow the prompts to complete the GitHub OAuth flow."  # noqa: E501
    )
    print(instructions)
