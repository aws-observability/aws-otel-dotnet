import json
import requests
import time
import logging

from testrunner_model.type import Type
from testrunner_tests.utils import constants
from testrunner_tests.tests import clients


# invokes webapp or lambda app endpoint
def invoke_endpoint(app_type, endpoint, event=None, lambda_client=None):
    if app_type == Type.WEBAPP.value:
        return invoke_and_get_traces_for_webapp(endpoint)
    elif app_type == Type.LAMBDA.value:
        return invoke_and_get_traces_for_lambda(endpoint, event, lambda_client)


# invokes web application endpoint and get traces
def invoke_and_get_traces_for_webapp(endpoint):
    """
    Invoke web app endpoint and get trace
    """

    for retry in range(constants.RETRIES):
        time.sleep(0.1)
        try:
            response = make_request(endpoint)
            if not response:
                raise Exception('Error while curling webapp endpoint')
            else:
                trace_header = get_trace_header_for_webapp(response)
                return trace_header

        except Exception as e:
            logging.exception(f'Exception : {e}')
            raise


def get_trace_header_for_webapp(response):
    trace_header = response.headers.get(constants.AMAZON_TRACE_HEADER_ID)

    if trace_header:
        return get_trace_id(trace_header)
    else:
        logging.error(f'Amazon trace header is missing')
        return


def invoke_and_get_traces_for_lambda(function_name, event, lambda_client):
    """
    Invokes lambda function and get trace
    """

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=event,
        )
        if not response:
            raise Exception(f'Error while invoking lambda function')
        else:
            trace_header = get_trace_header_for_lambda(response)
            return trace_header

    except Exception as e:
        logging.exception(f'Exception : {e}')
        raise


def get_trace_header_for_lambda(response):
    """
    Retrieve trace header from response object
    """

    trace_header = response['ResponseMetadata']['HTTPHeaders'][constants.LAMBDA_AMAZON_TRACE_HEADER_ID_KEY]

    if trace_header:
        return get_trace_id(trace_header)
    else:
        logging.error(f'Amazon trace header is missing')
        return


def make_request(url):
    try:
        return requests.get(url)

    except Exception as e:
        logging.exception(f'Exception while curling url: {e}')
        raise


# returns trace id from trace header
def get_trace_id(header):
    """
    Retrieve trace id from header
    """

    if not header:
        return

    try:
        params = header.strip().split(';')
        header_dict = {}
        for param in params:
            entry = param.split('=')
            key = entry[0]

            if key.lower() in (constants.ROOT, 'parent', 'sampled') and entry[1] != 'Self':
                header_dict[key.lower()] = entry[1]

        return header_dict[constants.ROOT]

    except Exception as e:
        logging.exception(f'Malformed tracing header: {header},\n exception: {e} \n')
        raise


def get_trace_from_xray(trace_id, xray_client):
    """
    Get traces from x-ray service using batch get trace API call for a given trace id
    """

    response = None

    if not trace_id:
        logging.error(f'trace id retrieval is none from x-ray')
        return

    for retry in range(constants.RETRIES):
        time.sleep(2)
        try:
            response = xray_client.batch_get_traces(
                TraceIds=[
                    trace_id,
                ]
            )

            if response['Traces']:
                return response['Traces']

        except Exception as e:
            logging.exception(f'Exception while doing batch_get_trace API call: {e} ')
            raise

    return response


def get_segment_data_from_response(request_trace_id):
    """
    Get traces from x-ray service and load into dictionary
    """
    traces = get_trace_from_xray(request_trace_id, clients.xray_client)
    trace = traces[0]
    segment_data = json.loads(trace[constants.SEGMENTS][0][constants.DOCUMENT])

    try:
        if constants.SUBSEGMENTS not in segment_data.keys():
            raise Exception('Web application path must have one one downstream call')

    except Exception as e:
        logging.exception(f'Exception : {e}')
        raise

    return segment_data, trace
