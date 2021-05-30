import boto3
import logging
from botocore.exceptions import ClientError
import os

logging.getLogger().setLevel(logging.INFO)
clouformation_client = boto3.client('cloudformation')

def create_stack(stack_name, template_body, **kwargs):
    clouformation_client.create_stack(
        StackName = stack_name,
        TemplateBody = template_body,
        Capabilities = ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        TimeoutInMinutes = 30,
        OnFalures = 'ROLLBACK'
    )

    clouformation_client.get_waiter('stack_create_complete').wait(
        StackName = stack_name,
        WaiterConfig = {'Delay': 5, 'MaxAttempts': 600}
    )

    clouformation_client.get_waiter('stack_exists').wait(StackName = stack_name)