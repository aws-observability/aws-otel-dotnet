import json

from testrunner_tests.utils.utils import invoke_endpoint, get_segment_data_from_response
from testrunner_model.type import Type
from testrunner_tests.utils import constants
from testrunner_tests.tests import clients


def create_event(key, value):
    data = {key: value}
    json_data = json.dumps(data)
    return json_data


# general tests for sdk lambda apps
class TestLambdaApp:
    def test_lambda_segments(self, endpoint, metric):
        event = create_event("test", "segment")

        # invoke lambda function enabled x-ray tracing
        request_trace_id = invoke_endpoint(app_type=Type.LAMBDA.value, endpoint=endpoint, event=event,
                                           lambda_client=clients.lambda_client)

        # retrieve traces from x-ray service and load into dictionary
        segment_data, lambda_function_trace = get_segment_data_from_response(request_trace_id)

        assert lambda_function_trace[constants.ID] != ""
        assert lambda_function_trace[constants.DURATION] != ""
