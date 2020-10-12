# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import requests

from testrunner_tests.utils import utils
from testrunner_tests.tests import clients
from testrunner_tests.utils import constants
from botocore.stub import Stubber, ANY


def test_get_trace_header_for_webapp():
    response = requests.get('https://aws.amazon.com')
    response.headers.setdefault('X-Amzn-Trace-Id', 'Root=1-5f3d6b24-1d1951e44ae6e56716c1e675')
    trace_id = utils.get_trace_header_for_webapp(response)
    assert trace_id == '1-5f3d6b24-1d1951e44ae6e56716c1e675'


def test_no_trace_header_for_webapp():
    response = requests.get('https://aws.amazon.com')
    trace_id = utils.get_trace_header_for_webapp(response)
    assert trace_id is None


def test_get_trace_header_for_lambda():
    response = {
        'ResponseMetadata': {
            'HTTPHeaders': {
                'x-amzn-trace-id': 'Root=1-5f3d6b24-1d1951e44ae6e56716c1e675'
            }
        }
    }

    expected_params = {'FunctionName': ANY}
    with Stubber(clients.lambda_client) as stubber:
        stubber.add_response('invoke', response, expected_params)
        service_response = clients.lambda_client.invoke(
            FunctionName='test'
        )

    trace_id = utils.get_trace_header_for_lambda(service_response)
    assert trace_id == '1-5f3d6b24-1d1951e44ae6e56716c1e675'


def test_no_trace_header_for_lambda():
    response = {
        'ResponseMetadata': {
            'HTTPHeaders': {
                'x-amzn-trace-id': ''
            }
        }
    }

    expected_params = {'FunctionName': ANY}
    with Stubber(clients.lambda_client) as stubber:
        stubber.add_response('invoke', response, expected_params)
        service_response = clients.lambda_client.invoke(
            FunctionName='test'
        )

    trace_id = utils.get_trace_header_for_lambda(service_response)
    assert trace_id is None


def test_get_trace_id():
    headers = ['Root=1-5f3d6b24-1d1951e44ae6e56716c1e675=Sampled?0',
               'root=1-5f3d6b24-1d1951e44ae6e56716c1e675=Sampled?0',
               'Root=1-5f3d6b24-1d1951e44ae6e56716c1e675=Sampled=789',
               'root=1-5f3d6b24-1d1951e44ae6e56716c1e675=Sampled?0===;',
               'Root=1-5f3d6b24-1d1951e44ae6e56716c1e675=~!@', ]

    for header in headers:
        trace_id = utils.get_trace_id(header)
        assert trace_id == '1-5f3d6b24-1d1951e44ae6e56716c1e675'


def test_get_segment_data_from_response():
    traces = dummy_batch_get_trace_call()
    trace = traces[0]
    segment_data = json.loads(trace[constants.SEGMENTS][0][constants.DOCUMENT])

    assert segment_data['id'] == '11bd034123a84c96'
    assert segment_data['name'] == 'My Flask Web Application'
    assert segment_data['start_time'] == 1597860644.127966
    assert segment_data['trace_id'] == '1-5f3d6b24-1d1951e44ae6e56716c1e675'
    assert segment_data['end_time'] == 1597860644.4768958
    assert segment_data['in_progress'] == False


def dummy_batch_get_trace_call():
    document = {"id": "11bd034123a84c96", "name": "My Flask Web Application", "start_time": 1597860644.127966,
                "trace_id": "1-5f3d6b24-1d1951e44ae6e56716c1e675", "end_time": 1597860644.4768958, "in_progress": False,
                }

    document_string = json.dumps(document)

    response = {
        'Traces': [
            {
                "Duration": 0.349,
                "Id": "1-5f3d6b24-1d1951e44ae6e56716c1e675",
                "Segments": [
                    {
                        "Document": document_string

                    },

                ]
            }
        ]
    }

    expected_params = {'TraceIds': ANY}
    with Stubber(clients.xray_client) as stubber:
        stubber.add_response('batch_get_traces', response, expected_params)
        service_response = clients.xray_client.batch_get_traces(
            TraceIds=[
                '1-5f3d6b24-1d1951e44ae6e56716c1e675',
            ]
        )

    return service_response['Traces']
