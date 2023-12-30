import boto3
import json
import logging
from aws_cdk import App
import time
from botocore.exceptions import ClientError
from .synth import PipelineStack

logging.basicConfig(level=logging.INFO)


def create_pipeline(
    stack_name, repo_string, branch="main", build_commands=None, region=None
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

    # if --region provided in command line, use that. Otherwise, use the AWS_DEFAULT_REGION env var. Otherwise, use prompt the user for a region.  # noqa: E501
    if region:
        region = region
    else:
        region = boto3.session.Session().region_name
        if not region:
            region = input(
                "Enter the region to deploy the pipeline to: "
            ).strip()  # noqa: E501
            if not region:
                logging.error("Region not provided. Exiting.")
                return

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

    cloudformation_client = boto3.client(
        "cloudformation", region_name=region
    )  # noqa: E501

    try:
        cloudformation_client.delete_stack(StackName=stack_name)
        logging.info(f"Stack deletion initiated for {stack_name}")
        tail_cloudformation_logs(stack_name, region_name=region)
    except Exception as e:
        logging.error(f"Error deleting stack: {e}")


def tail_cloudformation_logs(stack_name, region_name):
    logging.info(f"Tailing logs for CloudFormation stack: {stack_name}")

    client = boto3.client("cloudformation", region_name=region_name)
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
                reason = event.get("ResourceStatusReason", "")
                logging.info(
                    f"{timestamp} - {resource_type} - {logical_id} - {status} - {reason}"  # noqa: E501
                )

        # Check if the stack creation or update is complete
        stack_description = client.describe_stacks(StackName=stack_name)
        stack_status = stack_description["Stacks"][0]["StackStatus"]
        if "COMPLETE" in stack_status or "FAILED" in stack_status:
            break

        # Sleep for some time before polling again
        time.sleep(10)

    logging.info(
        f"Finished tailing logs for CloudFormation stack: {stack_name}"
    )  # noqa: E501
