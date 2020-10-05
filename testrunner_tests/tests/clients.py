import boto3
import os

region = os.environ.get('AWS_REGION')


# returns the client of different aws services
def get_xray_client():
    return boto3.client('xray', region_name=region)


def get_lambda_client():
    return boto3.client('lambda', region_name=region)


def get_cloudwatch_client():
    return boto3.client('cloudwatch', region_name=region)


# aws clients creation
xray_client = get_xray_client()
lambda_client = get_lambda_client()
cloudwatch_client = get_cloudwatch_client()
